#!/usr/bin/env python3
"""Run the local MiniMax H3 Ref2VA image-reference workflow."""

from __future__ import annotations

import argparse
import json
import secrets
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


HOLO = Path(__file__).resolve().parent
INPUT_DIR = HOLO / "input"
DEFAULT_PROMPT = HOLO / "user/default/workflows/r2v_style_collision_prompt.txt"


def request_json(url: str, data: dict | None = None) -> dict:
    request = urllib.request.Request(
        url,
        data=None if data is None else json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def input_name(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(INPUT_DIR.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"reference images must be inside {INPUT_DIR}: {resolved}") from error


def build_graph(prompt: str, args: argparse.Namespace) -> dict:
    graph = {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "minimax_h3_ref2va_pruned_int8_convrot.safetensors",
                "weight_dtype": "default",
            },
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
                "type": "minimax",
                "device": "default",
            },
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"},
        },
        "4": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"},
        },
        "5": {
            "class_type": "MiniMaxH3ReferenceToVideo",
            "inputs": {
                "clip": ["2", 0],
                "vae": ["3", 0],
                "audio_vae": ["4", 0],
                "prompt": prompt,
                "width": args.width,
                "height": args.height,
                "length": args.length,
                "ref_image_size": args.ref_image_size,
            },
        },
        "6": {
            "class_type": "BasicScheduler",
            "inputs": {
                "model": ["1", 0],
                "scheduler": args.scheduler,
                "steps": args.steps,
                "denoise": 1.0,
            },
        },
        "7": {
            "class_type": "KSamplerSelect",
            "inputs": {"sampler_name": "res_multistep"},
        },
        "8": {
            "class_type": "RandomNoise",
            "inputs": {"noise_seed": args.seed},
        },
        "9": {
            "class_type": "SpectrumApplyMiniMaxH3",
            "inputs": {
                "model": ["1", 0],
                "enabled": args.spectrum,
                "blend_weight": 0.5,
                "degree": 4,
                "ridge_lambda": 0.1,
                "window_size": 2.0,
                "flex_window": 0.75,
                "warmup_steps": 5,
                "tail_actual_steps": 1,
                "max_history": 8,
                "debug": False,
                "history_storage": "system_ram",
            },
        },
        "10": {
            "class_type": "BasicGuider",
            "inputs": {"model": ["18", 0], "conditioning": ["5", 0]},
        },
        "11": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["8", 0],
                "guider": ["10", 0],
                "sampler": ["7", 0],
                "sigmas": ["6", 0],
                "latent_image": ["5", 1],
            },
        },
        "12": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["11", 0], "vae": ["3", 0]},
        },
        "13": {
            "class_type": "VAEDecodeAudio",
            "inputs": {"samples": ["11", 0], "vae": ["4", 0]},
        },
        "14": {
            "class_type": "CreateVideo",
            "inputs": {
                "images": ["12", 0],
                "fps": 24.0,
                "audio": ["13", 0],
                "bit_depth": 8,
            },
        },
        "15": {
            "class_type": "SaveVideo",
            "inputs": {
                "video": ["14", 0],
                "filename_prefix": args.output_prefix,
                "format": "mp4",
                "codec": "h264",
            },
        },
        "18": {
            "class_type": "SpectrumMiniMaxH3ResidualCache",
            "inputs": {
                "model": ["9", 0],
                "enabled": args.cache,
                "reuse_threshold": args.cache_threshold,
                "start_percent": args.cache_start,
                "end_percent": args.cache_end,
                "max_steps": args.cache_max_steps,
                "storage": args.cache_storage,
                "verbose": args.cache_verbose,
            },
        },
    }

    if args.crf is not None:
        graph["15"]["inputs"]["codec.encoding"] = "re-encode"
        graph["15"]["inputs"]["codec.encoding.crf"] = float(args.crf)

    if not 1 <= len(args.ref_image) <= 9:
        raise ValueError("Ref2VA accepts between 1 and 9 reference images")
    for index, image_path in enumerate(args.ref_image):
        node_id = str(20 + index)
        graph[node_id] = {
            "class_type": "LoadImage",
            "inputs": {"image": input_name(image_path)},
        }
        graph["5"]["inputs"][f"ref_images.ref_image_{index}"] = [node_id, 0]
    return graph


def output_paths(history: dict) -> list[Path]:
    paths = []
    for output in history.get("outputs", {}).values():
        for values in output.values():
            if not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, dict) or "filename" not in value:
                    continue
                folder = HOLO / "output"
                if value.get("subfolder"):
                    folder /= value["subfolder"]
                paths.append(folder / value["filename"])
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", default="http://127.0.0.1:8189")
    parser.add_argument("--prompt-file", type=Path, default=DEFAULT_PROMPT)
    parser.add_argument("--ref-image", type=Path, action="append", required=True)
    parser.add_argument("--ref-image-size", choices=("match", "max"), default="match")
    parser.add_argument("--width", type=int, default=864)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--length", type=int, default=243)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--scheduler", choices=("beta", "normal", "simple"), default="beta")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--spectrum", action="store_true")
    parser.add_argument("--cache", action="store_true")
    parser.add_argument("--cache-threshold", type=float, default=0.05)
    parser.add_argument("--cache-start", type=float, default=0.15)
    parser.add_argument("--cache-end", type=float, default=0.90)
    parser.add_argument("--cache-max-steps", type=int, default=2)
    parser.add_argument("--cache-storage", choices=("auto", "cpu"), default="auto")
    parser.add_argument("--cache-verbose", action="store_true")
    parser.add_argument("--crf", type=int, choices=range(52), default=17)
    parser.add_argument("--output-prefix", default="video/MiniMax_H3_R2V_Style_Collision")
    parser.add_argument("--timeout", type=int, default=7200)
    args = parser.parse_args()

    if args.spectrum and args.cache:
        parser.error("--spectrum and --cache are alternative approximate accelerators; choose one")

    args.seed = args.seed if args.seed is not None else secrets.randbelow(2**63)
    prompt = args.prompt_file.expanduser().read_text().strip()
    queued = request_json(
        f"{args.server}/prompt",
        {"prompt": build_graph(prompt, args), "client_id": str(uuid.uuid4())},
    )
    prompt_id = queued["prompt_id"]
    print(f"queued prompt_id={prompt_id} seed={args.seed}", flush=True)

    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        history = request_json(f"{args.server}/history/{prompt_id}").get(prompt_id)
        if history:
            status = history.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status, indent=2))
            paths = output_paths(history)
            if paths:
                for path in paths:
                    print(path, flush=True)
                return
        time.sleep(5)
    raise TimeoutError(f"generation did not finish within {args.timeout} seconds")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        print(error.read().decode(errors="replace"))
        raise

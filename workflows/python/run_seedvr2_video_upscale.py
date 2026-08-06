#!/usr/bin/env python3
"""Run the native ComfyUI SeedVR2 temporal-chunk video upscaler."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


HOLO = Path(__file__).resolve().parent
INPUT_DIR = HOLO / "input"
OUTPUT_DIR = HOLO / "output"


def request_json(url: str, data: dict | None = None) -> dict:
    request = urllib.request.Request(
        url,
        data=None if data is None else json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def input_name(path: Path) -> str:
    resolved = path.expanduser().resolve()
    return resolved.relative_to(INPUT_DIR.resolve()).as_posix()


def build_graph(args: argparse.Namespace) -> dict:
    return {
        "1": {
            "class_type": "LoadVideo",
            "inputs": {"file": input_name(args.input)},
        },
        "2": {
            "class_type": "GetVideoComponents",
            "inputs": {"video": ["1", 0]},
        },
        "3": {
            "class_type": "ResizeImageMaskNode",
            "inputs": {
                "input": ["2", 0],
                "resize_type": "scale by multiplier",
                "resize_type.multiplier": args.scale,
                "scale_method": "lanczos",
            },
        },
        "4": {
            "class_type": "SeedVR2Preprocess",
            "inputs": {"resized_images": ["3", 0]},
        },
        "5": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": args.vae},
        },
        "6": {
            "class_type": "VAEEncodeTiled",
            "inputs": {
                "pixels": ["4", 0],
                "vae": ["5", 0],
                "tile_size": args.tile_size,
                "overlap": args.tile_overlap,
                "temporal_size": args.vae_temporal_size,
                "temporal_overlap": args.vae_temporal_overlap,
            },
        },
        "7": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": args.unet,
                "weight_dtype": args.weight_dtype,
            },
        },
        "8": {
            "class_type": "SeedVR2TemporalChunk",
            "inputs": {
                "latent": ["6", 0],
                "temporal_overlap": args.chunk_overlap,
                "chunking_mode": "auto",
            },
        },
        "9": {
            "class_type": "SeedVR2Conditioning",
            "inputs": {"model": ["7", 0], "vae_conditioning": ["8", 0]},
        },
        "10": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["7", 0],
                "positive": ["9", 0],
                "negative": ["9", 1],
                "latent_image": ["8", 0],
                "seed": args.seed,
                "steps": 1,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "11": {
            "class_type": "SeedVR2TemporalMerge",
            "inputs": {"latents": ["10", 0], "temporal_overlap": ["8", 1]},
        },
        "12": {
            "class_type": "VAEDecodeTiled",
            "inputs": {
                "samples": ["11", 0],
                "vae": ["5", 0],
                "tile_size": args.tile_size,
                "overlap": args.tile_overlap,
                "temporal_size": args.vae_temporal_size,
                "temporal_overlap": args.vae_temporal_overlap,
            },
        },
        "13": {
            "class_type": "SeedVR2PostProcessing",
            "inputs": {
                "images": ["12", 0],
                "original_resized_images": ["3", 0],
                "color_correction_method": args.color_correction,
            },
        },
        "14": {
            "class_type": "CreateVideo",
            "inputs": {
                "images": ["13", 0],
                "audio": ["2", 1],
                "fps": ["2", 2],
                "bit_depth": args.bit_depth,
            },
        },
        "15": {
            "class_type": "SaveVideo",
            "inputs": {
                "video": ["14", 0],
                "filename_prefix": args.output_prefix,
                "format": "mp4",
                "codec": "h264",
                "codec.encoding": "re-encode",
                "codec.encoding.crf": float(args.crf),
            },
        },
    }


def output_paths(history: dict) -> list[Path]:
    paths: list[Path] = []
    for output in history.get("outputs", {}).values():
        for values in output.values():
            if not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, dict) or "filename" not in value:
                    continue
                folder = OUTPUT_DIR
                if value.get("subfolder"):
                    folder /= value["subfolder"]
                paths.append(folder / value["filename"])
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server", default="http://127.0.0.1:8189")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--scale", type=float, default=1.5)
    parser.add_argument("--unet", default="seedvr2_3b_int8_convrot.safetensors")
    parser.add_argument("--vae", default="seedvr2_ema_vae_fp16.safetensors")
    parser.add_argument("--weight-dtype", default="default")
    parser.add_argument("--seed", type=int, default=8675309)
    parser.add_argument("--chunk-overlap", type=int, default=4)
    parser.add_argument("--tile-size", type=int, default=512)
    parser.add_argument("--tile-overlap", type=int, default=128)
    parser.add_argument("--vae-temporal-size", type=int, default=64)
    parser.add_argument("--vae-temporal-overlap", type=int, default=8)
    parser.add_argument(
        "--color-correction", choices=("lab", "wavelet", "adain", "none"), default="lab"
    )
    parser.add_argument("--bit-depth", type=int, choices=(8, 10), default=8)
    parser.add_argument("--crf", type=int, choices=range(52), default=12)
    parser.add_argument(
        "--output-prefix", default="video/SeedVR2/Upscaled_SeedVR2"
    )
    parser.add_argument("--timeout", type=int, default=14400)
    args = parser.parse_args()

    queued = request_json(
        f"{args.server}/prompt",
        {"prompt": build_graph(args), "client_id": str(uuid.uuid4())},
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

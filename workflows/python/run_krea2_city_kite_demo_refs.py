#!/usr/bin/env python3
"""Generate Krea 2 references for a single H3 city kite-running demo."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

from run_krea2_desert_vignette_stills import request_json


HOLO = Path(__file__).resolve().parent
OUTPUT_PREFIX = "City_Kite_Demo_Krea_Refs"
MANIFEST = HOLO / "output" / OUTPUT_PREFIX / "manifest.json"
WIDTH = 720
HEIGHT = 1280
STYLE_LORA_STRENGTH = 0.4

ASSETS = [
    {
        "slug": "01_hana_character",
        "seed": 21137,
        "prompt": (
            "A polished vertical HoloSomnia-style cel-shaded anime character reference "
            "illustration of one full-body figure. Hana is an eleven-year-old East Asian "
            "girl with a chin-length black bob, warm dark-brown eyes, and natural child "
            "proportions. She wears a straw sunhat with an indigo band, a cream short-sleeve "
            "collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. "
            "She stands in a relaxed three-quarter profile facing toward the right, both "
            "arms resting naturally at her sides and every garment fully visible. Her "
            "expression is gentle, alert, and quietly determined. The uncluttered background "
            "is a pale lavender-to-pink studio gradient with a soft oval ground shadow. "
            "Clean sculpted forms, precise cel shading, subtle iridescent rim light, and a "
            "pristine animation-model-sheet finish define the image."
        ),
    },
    {
        "slug": "02_white_kite",
        "seed": 42281,
        "prompt": (
            "A polished vertical HoloSomnia-style cel-shaded prop reference illustration "
            "showing one centered plain white diamond kite from the front. Its smooth white "
            "paper face is completely unmarked, stretched into a clean symmetrical diamond "
            "with a fine warm-grey perimeter and a simple pale bamboo cross visible beneath "
            "the paper. Two narrow white ribbon tails extend separately from the bottom point "
            "and curve gently downward, both fully visible. A single thin cream string leads "
            "from the kite to a small dark-wood spool arranged neatly near the lower edge. "
            "The object is isolated against a luminous cobalt-to-lavender sky gradient with "
            "soft pink reflected light, crisp silhouette separation, and restrained shadows."
        ),
    },
    {
        "slug": "03_city_start",
        "seed": 67309,
        "prompt": (
            "A dynamic vertical HoloSomnia-style cel-shaded anime starting frame in a bright "
            "Japanese hillside city at golden hour. Hana, one eleven-year-old East Asian girl "
            "with a chin-length black bob and warm dark-brown eyes, runs toward screen-right "
            "through the right half of a broad pedestrian street. She wears a straw sunhat "
            "with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, "
            "white ankle socks, and red canvas shoes, and holds a small dark-wood spool. A "
            "plain unmarked white diamond kite with two narrow white ribbon tails flies behind "
            "her in the upper-left, connected by one taut cream string that forms a clean "
            "backward diagonal. Colorful mid-rise buildings, elevated walkways, glass awnings, "
            "balconies, trees, and abstract glowing shop panels create layered urban depth "
            "while the street remains open around her. Strong golden sunbeams stream between "
            "soaring bright pink and purple clouds and reflect in gold, magenta, and lavender "
            "across the rain-polished pavement. The low three-quarter camera gives Hana and "
            "the trailing kite clear, separate silhouettes and a strong forward path."
        ),
    },
]


def graph(asset: dict) -> dict:
    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "krea2/Krea2_Raw_convrot_int8mixed.safetensors",
                "weight_dtype": "default",
            },
        },
        "2": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["1", 0],
                "lora_name": "krea2/krea2_raw_to_turbo_r256_comfy.safetensors",
                "strength_model": 1.0,
            },
        },
        "3": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["2", 0],
                "lora_name": "krea2/holosomnia-krea2-style-v3-full.safetensors",
                "strength_model": STYLE_LORA_STRENGTH,
            },
        },
        "4": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen3vl_4b_fp8_scaled.safetensors",
                "type": "krea2",
                "device": "default",
            },
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["4", 0], "text": asset["prompt"]},
        },
        "6": {
            "class_type": "ConditioningZeroOut",
            "inputs": {"conditioning": ["5", 0]},
        },
        "7": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1},
        },
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["3", 0],
                "positive": ["5", 0],
                "negative": ["6", 0],
                "latent_image": ["7", 0],
                "seed": asset["seed"],
                "steps": 8,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "9": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": "qwen_image_vae.safetensors"},
        },
        "10": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["8", 0], "vae": ["9", 0]},
        },
        "11": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["10", 0],
                "filename_prefix": f"{OUTPUT_PREFIX}/{asset['slug']}",
            },
        },
    }


def main() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    client_id = str(uuid4())
    queued: dict[str, dict] = {}
    manifest = {
        "width": WIDTH,
        "height": HEIGHT,
        "model": "krea2/Krea2_Raw_convrot_int8mixed.safetensors",
        "turbo_lora_strength": 1.0,
        "style_lora": "krea2/holosomnia-krea2-style-v3-full.safetensors",
        "style_lora_strength": STYLE_LORA_STRENGTH,
        "assets": [],
    }

    for asset in ASSETS:
        response = request_json(
            "/prompt", {"prompt": graph(asset), "client_id": client_id}
        )
        prompt_id = response["prompt_id"]
        job = {**asset, "prompt_id": prompt_id}
        queued[prompt_id] = job
        manifest["assets"].append(job)
        print(f"queued {asset['slug']} prompt_id={prompt_id}", flush=True)

    deadline = time.monotonic() + 1800
    pending = set(queued)
    while pending:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"timed out waiting for {len(pending)} references")
        for prompt_id in list(pending):
            record = request_json(f"/history/{prompt_id}").get(prompt_id)
            if not record:
                continue
            if record.get("status", {}).get("status_str") == "error":
                raise RuntimeError(f"generation failed: {record}")
            outputs = record.get("outputs", {}).get("11", {}).get("images", [])
            if outputs:
                queued[prompt_id]["output"] = outputs[0]
                print(
                    f"complete {queued[prompt_id]['slug']} output={outputs[0]}",
                    flush=True,
                )
                pending.remove(prompt_id)
        if pending:
            time.sleep(2)

    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()

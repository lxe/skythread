#!/usr/bin/env python3
"""Generate the empty Krea environment reference for the cabin-porch H3 demo."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

import run_krea2_city_kite_demo_refs as base
from run_krea2_desert_vignette_stills import request_json


OUTPUT_PREFIX = "Cabin_Porch_Demo_Krea_Scene"
base.OUTPUT_PREFIX = OUTPUT_PREFIX
MANIFEST = Path(__file__).resolve().parent / "output" / OUTPUT_PREFIX / "manifest.json"

SCENE = {
    "slug": "01_cabin_porch_environment",
    "seed": 73147,
    "prompt": (
        "A polished vertical HoloSomnia-style cel-shaded anime environment plate of a "
        "rustic cedar cabin porch overlooking an extraordinarily beautiful mountain "
        "landscape at golden hour. Broad rain-polished wooden boards fill the open lower "
        "half of the composition and run toward screen-right, creating a clear path for "
        "movement. The cabin wall, dark timber posts, an open doorway, and a small glass "
        "wind chime frame the left edge; a low railing and three shallow steps frame the "
        "right edge without blocking the deck. Beyond the porch, wildflower meadows descend "
        "toward a luminous winding lake, layered pine ridges, and distant blue mountains. "
        "The porch center is empty, uncluttered, and fully visible. A vast bright sky is "
        "filled with soaring pink and purple clouds, while strong golden sunbeams stream "
        "through their gaps and reflect in gold, magenta, and lavender across the wet wood, "
        "lake, and glass. Clean sculpted forms, deep atmospheric layers, crisp cel shading, "
        "iridescent cloud light, and serene cinematic depth define the image."
    ),
}


def main() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    prompt_id = request_json(
        "/prompt",
        {"prompt": base.graph(SCENE), "client_id": str(uuid4())},
    )["prompt_id"]
    print(f"queued {SCENE['slug']} prompt_id={prompt_id}", flush=True)

    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        record = request_json(f"/history/{prompt_id}").get(prompt_id)
        if record:
            if record.get("status", {}).get("status_str") == "error":
                raise RuntimeError(f"generation failed: {record}")
            outputs = record.get("outputs", {}).get("11", {}).get("images", [])
            if outputs:
                manifest = {
                    "width": base.WIDTH,
                    "height": base.HEIGHT,
                    "seed": SCENE["seed"],
                    "style_lora_strength": base.STYLE_LORA_STRENGTH,
                    "scene": {**SCENE, "prompt_id": prompt_id, "output": outputs[0]},
                }
                MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
                print(f"complete output={outputs[0]}", flush=True)
                print(f"manifest={MANIFEST}")
                return
        time.sleep(2)
    raise TimeoutError("timed out waiting for cabin porch scene")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate three Krea2 + HoloSomnia storyboard references for Skythread inserts."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

import run_krea2_skythread_v3_stills as base
from run_krea2_desert_vignette_stills import request_json


HOLO = Path(__file__).resolve().parent
OUTPUT_PREFIX = "Skythread_Insert_Refs_V1"
base.OUTPUT_PREFIX = OUTPUT_PREFIX
MANIFEST = HOLO / "output" / OUTPUT_PREFIX / "manifest.json"

HANA = (
    "exactly one Hana, an eleven-year-old East Asian girl with a chin-length black bob, "
    "warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve "
    "collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes"
)

KITE = (
    "exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, "
    "a simple pale bamboo cross, exactly two narrow white ribbon tails, one thin cream "
    "string, and one small dark-wood spool"
)

STYLE = (
    "Polished vertical HoloSomnia-style hand-painted cel animation, crisp stable inked "
    "contours, flat two-tone cel shading, matte gouache and watercolor texture, clean "
    "sculpted forms, deep layered atmospheric perspective, and controlled 2D multiplane "
    "depth. Bright golden-hour sunlight pours through immense pink, purple, peach, pale-cyan, "
    "and cobalt clouds, creating visible stable rays and reflected bands of gold, magenta, "
    "and lavender. Keep the white kite crisp and plain against the saturated landscape."
)

SCENES = [
    {
        "slug": "01_bunny_field_start",
        "seed": 95113,
        "prompt": (
            "A low animal-eye-level lateral wide shot across a gently sloping summer field "
            "in the same Japanese mountain valley. The composition has three clean depth "
            "layers. In the immediate lower foreground, exactly four natural wild rabbits, "
            "two adults and two smaller kits, gather beside one low weathered wooden water "
            "trough filled with clear water and one compact rectangular golden hay bale. "
            "All four rabbits have turned their ears and faces toward the background runner; "
            "their bodies are separate, anatomically correct, and poised to spring in "
            "different directions, but none has moved yet. In the unobstructed middle "
            "background, "
            + HANA
            + " runs naturally from screen-left toward screen-right along one horizontal "
            "field path, small enough to remain clearly behind the rabbits. She holds the "
            "dark-wood spool in her right hand. "
            + KITE.capitalize()
            + " flies high behind Hana in the upper-left, well separated from her, with one "
            "long taut cream line connected directly to the spool. The kite trails behind "
            "her travel direction and never appears in her hand. Wind-shaped grasses, sparse "
            "blue and yellow wildflowers, a distant cedar fence, irregular paddies, pine "
            "ridges, and a luminous lake create an open rightward movement corridor. Exactly "
            "one girl, four rabbits, one trough, one hay bale, and one kite; no other people "
            "or animals. "
            + STYLE
        ),
    },
    {
        "slug": "02_topdown_kite_birds_start",
        "seed": 95267,
        "prompt": (
            "The camera points exactly perpendicular to the earth in a strict ninety-degree "
            "straight-down aerial view with no horizon and no oblique perspective. Far below, "
            "organic asymmetrical rice paddies, a narrow blue-green irrigation channel, "
            "rounded meadow edges, scattered stones, and small pine clusters form flowing "
            "map-like shapes. At the exact visual center flies "
            + KITE
            + ", seen cleanly from above with its complete diamond silhouette, bamboo cross, "
            "and two separate tails readable. Its single cream string continues straight "
            "through the bottom edge toward unseen Hana. Exactly three small barn swallows "
            "fly around the kite at different distances in one loose clockwise arc: one near "
            "upper-left, one at frame-right, and one lower-right. Each bird is a separate "
            "clean dark-and-cream silhouette with two wings, one head, and a forked tail; no "
            "overlap, flock clump, or extra birds. Reflected pink-purple clouds and long gold "
            "sunbeams shimmer in the irrigation water while soft cloud shadows cross the "
            "fields. The graphic composition is spacious and calm, designed for the birds "
            "to circle and peel away from the kite. "
            + STYLE
        ),
    },
    {
        "slug": "03_train_tracking_start",
        "seed": 95419,
        "prompt": (
            "A stabilized low lateral wide composition beside a rural railway in the same "
            "Japanese mountain valley after rain. The foreground contains one broad safe "
            "footpath running horizontally from screen-left to screen-right, separated from "
            "the railway by one simple cedar fence. "
            + HANA.capitalize()
            + " runs left-to-right in a lively balanced stride on the foreground path, shown "
            "full-body in three-quarter side profile with generous open lead room ahead. She "
            "holds the small dark-wood spool in her right hand. "
            + KITE.capitalize()
            + " remains high and behind her in the upper-left, connected to the spool by one "
            "long taut cream line and trailing clearly opposite her direction of travel. In "
            "the middle distance, exactly one cream-and-vermilion local electric train passes "
            "left-to-right on one straight horizontal track parallel to Hana. Its scale, "
            "windows, doors, wheels, and carriage geometry remain coherent and clearly behind "
            "the fence. The train and Hana travel in the same direction on separate depth "
            "planes, suitable for a smooth lateral tracking camera. Wet grasses, blue "
            "hydrangeas, curved rice fields, cedar houses, and pine-covered hills recede "
            "beneath bright multicolored clouds. Crisp frozen storyboard moment with no motion "
            "blur, Dutch angle, vibration, crossing collision, duplicate train, duplicate "
            "girl, or extra kite. "
            + STYLE
        ),
    },
]


def main() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    client_id = str(uuid4())
    queued: dict[str, dict] = {}
    manifest = {
        "width": base.WIDTH,
        "height": base.HEIGHT,
        "model": "krea2/Krea2_Raw_convrot_int8mixed.safetensors",
        "turbo_lora_strength": 1.0,
        "style_lora": "krea2/holosomnia-krea2-style-v3-full.safetensors",
        "style_lora_strength": base.STYLE_LORA_STRENGTH,
        "scenes": [],
    }

    for scene in SCENES:
        response = request_json(
            "/prompt", {"prompt": base.graph(scene), "client_id": client_id}
        )
        prompt_id = response["prompt_id"]
        job = {**scene, "prompt_id": prompt_id}
        queued[prompt_id] = job
        manifest["scenes"].append(job)
        print(f"queued {scene['slug']} prompt_id={prompt_id}", flush=True)

    deadline = time.monotonic() + 2400
    pending = set(queued)
    while pending:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"timed out waiting for {len(pending)} reference stills")
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

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"manifest={MANIFEST}", flush=True)


if __name__ == "__main__":
    main()

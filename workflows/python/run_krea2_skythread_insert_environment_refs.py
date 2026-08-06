#!/usr/bin/env python3
"""Generate environment-first Krea2 references for Skythread bunny and train inserts."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

import run_krea2_skythread_v3_stills as base
from run_krea2_desert_vignette_stills import request_json


HOLO = Path(__file__).resolve().parent
OUTPUT_PREFIX = "Skythread_Insert_Environment_Refs_V2"
base.OUTPUT_PREFIX = OUTPUT_PREFIX
MANIFEST = HOLO / "output" / OUTPUT_PREFIX / "manifest.json"

STYLE = (
    "The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate "
    "with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, "
    "and a pristine cinematic finish. Bright golden-hour light pours through soaring pink "
    "and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and "
    "lavender across the landscape."
)

SCENES = [
    {
        "slug": "01_bunny_field_environment",
        "seed": 96121,
        "prompt": (
            "A low animal-eye-level lateral environment view across a gently sloping summer "
            "field in the same Japanese mountain valley. In the immediate lower foreground, "
            "exactly four natural wild rabbits, two adults and two smaller kits, gather beside "
            "one low weathered rectangular wooden water trough filled with clear water and one "
            "compact rectangular golden hay bale. Each rabbit has a separate readable body, "
            "correct anatomy, upright alert ears, and a distinct position around the trough. "
            "All four have turned their heads toward the open left side of the background and "
            "are poised to spring in different directions. Across the unobstructed middle "
            "background, one broad dry field path runs continuously from screen-left to "
            "screen-right with generous empty space for a distant runner to be added later. "
            "Wind-shaped grasses, sparse blue and yellow wildflowers, a cedar fence, irregular "
            "curved paddies, pine ridges, and a luminous lake create three clean depth layers. "
            "The entire upper sky remains open for a distant flying object to be added later. "
            "No people, no kite, no string, no spool, no other animals, no duplicate trough, "
            "and no duplicate hay bale. "
            + STYLE
        ),
    },
    {
        "slug": "02_train_tracking_environment",
        "seed": 96307,
        "prompt": (
            "A stabilized low lateral wide environment view beside a rural railway in the "
            "same Japanese mountain valley after rain. One broad safe packed-earth footpath "
            "runs horizontally from screen-left to screen-right across the open lower "
            "foreground, leaving a long unobstructed movement corridor. One simple cedar "
            "fence separates the path from one straight horizontal railway track in the "
            "middle distance. Exactly one coherent cream-and-vermilion two-car local electric "
            "train is seen in clean side elevation on that track, oriented left-to-right, "
            "with consistent windows, doors, roof equipment, wheel spacing, and carriage "
            "scale. Preserve generous open lead room at screen-right and clear separation "
            "between foreground path, fence, and train for a smooth lateral tracking shot. "
            "Wet grasses, blue hydrangeas, organic curved rice fields, sparse cedar houses, "
            "and pine-covered hills recede into the valley. The sky is broad and unobstructed. "
            "No people, no kite, no string, no spool, no second train, no crossing collision, "
            "no Dutch angle, and no motion blur. "
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
            raise TimeoutError(f"timed out waiting for {len(pending)} environment refs")
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

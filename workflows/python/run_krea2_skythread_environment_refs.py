#!/usr/bin/env python3
"""Generate six empty Krea environment plates for the remaining Skythread scenes."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

import run_krea2_city_kite_demo_refs as base
from run_krea2_desert_vignette_stills import request_json


HOLO = Path(__file__).resolve().parent
OUTPUT_PREFIX = "Skythread_Environment_Refs_V1"
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
        "slug": "01_mountain_path",
        "seed": 74101,
        "prompt": (
            "A child-height medium-wide view along a broad mountain footpath just beyond a "
            "rustic cedar cabin. The dry earth-and-stone path enters from the lower-left, "
            "curves smoothly toward screen-right through an open foreground, then descends "
            "toward a distant Japanese hillside village. Low split-cedar fences, sparse blue "
            "and yellow wildflowers, mossy stones, and wind-bent grasses frame the route "
            "without obstructing it. Organic mountain contours, pine groves, a winding lake, "
            "and layered blue ridges connect this place to the cabin landscape. The path is "
            "empty, uncluttered, and clearly readable as one continuous rightward movement "
            "corridor. "
            + STYLE
        ),
    },
    {
        "slug": "02_rice_fields",
        "seed": 74237,
        "prompt": (
            "A low lateral medium-wide view across beautiful hand-built rice terraces in the "
            "same Japanese mountain valley. A dry raised footpath runs continuously from "
            "screen-left to screen-right through the lower-middle of the composition, with a "
            "broad unobstructed surface and sparse wildflowers along its edges. The paddies "
            "follow the natural contours in large flowing curves, with irregular grassy "
            "banks, varied widths, asymmetrical shapes, and gently winding irrigation water. "
            "Dark cedar farmhouses sit far apart among pine-covered slopes, while a luminous "
            "lake and distant blue mountains deepen the view. The environment is serene and "
            "open, designed around a clear lateral movement path. "
            + STYLE
        ),
    },
    {
        "slug": "03_aerial_path_mountains",
        "seed": 74381,
        "prompt": (
            "An exact bird's-eye environment view looking straight down over the folded "
            "terrain of the same mountain valley. A pale winding footpath begins at the "
            "bottom edge and snakes upward through irregular terraced slopes, patches of "
            "pine forest, rounded rocky outcrops, wildflower meadows, and a narrow blue stream. "
            "The mountain ridges read as broad organic contour shapes rather than geometric "
            "grids, and the trail remains visible as one continuous ribbon across the entire "
            "frame. Warm low sunlight strikes the higher ridges and casts long violet shadows, "
            "while water and pale stone carry reflected pink, purple, magenta, and gold from "
            "the surrounding golden-hour atmosphere. The map-like vertical composition is "
            "empty, flowing, and richly layered. The rendering is polished HoloSomnia-style "
            "cel-shaded anime with sculpted terrain, luminous color separation, and crisp "
            "organic detail."
        ),
    },
    {
        "slug": "04_train_crossing",
        "seed": 74503,
        "prompt": (
            "A low wide environment view at a quiet rural railway crossing in the same "
            "Japanese mountain valley after rain. A broad paved footpath runs left-to-right "
            "through the open lower foreground and meets a lowered black-and-amber crossing "
            "gate at a safe waiting area. Two polished rails cut diagonally through the "
            "middle distance and curve away between organic rice fields, cedar houses, and "
            "pine-covered hills. Blue hydrangeas, wet grasses, small signal lights, and a "
            "simple wooden crossing hut frame the edges while leaving the foreground and sky "
            "clearly visible. Violet storm depth gathers over the left ridge and radiant warm "
            "light opens on the right, creating a dramatic but welcoming transition. "
            + STYLE
        ),
    },
    {
        "slug": "05_soaring_skies",
        "seed": 74629,
        "prompt": (
            "A vast upward-looking environment view inside an immense soaring cloud corridor "
            "above the same Japanese mountain valley. Sculpted banks of brilliant pink, "
            "purple, violet, cobalt, peach, and pale cyan clouds curl along the left and right "
            "edges, forming a broad diagonal passage from the lower-left toward a radiant "
            "opening in the upper-right. Powerful golden-hour sunbeams fan through the gap, "
            "strike the luminous cloud faces, and create transparent shafts of gold, magenta, "
            "and lavender light. Far below at the bottom edge, organic curved rice terraces, "
            "pine ridges, and a threadlike lake recede through blue atmospheric depth. The "
            "central sky route is open, grand, and clearly readable for continuous flight. "
            + STYLE
        ),
    },
    {
        "slug": "06_mountain_shrine",
        "seed": 74771,
        "prompt": (
            "A calm medium-wide environment view across a weathered mountaintop shrine terrace "
            "in the same Japanese mountain valley. A tall vermilion torii frames the center "
            "without blocking a broad stone-and-earth path that enters from the lower-left, "
            "passes beneath the gate, and continues toward screen-right. A small cedar shrine "
            "building sits along the left edge, while one bronze bell, white prayer streamers, "
            "mossy lanterns, and wind-shaped grasses provide restrained detail around the open "
            "terrace. Far below, organic curved rice terraces, tiny cedar roofs, a thin railway, "
            "and the winding lake settle into layered blue-green shadow. Immense pink and "
            "purple clouds open around the low sun beyond the ridge, creating a quiet, powerful, "
            "and resolved landscape. "
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
            raise TimeoutError(f"timed out waiting for {len(pending)} environment plates")
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

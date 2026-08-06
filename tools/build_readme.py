#!/usr/bin/env python3
"""Build README.md from the checked-in prompt and seed manifests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FINAL_H3 = [
    ("1", "Cabin start", "01_cabin_porch.txt", 88143, 243, 240),
    ("2", "Path energy", "02_mountain_path_v3_proposed.txt", 88402, 209, 206),
    ("3", "Mountain path", "02_mountain_path_v4_uphill_crane.txt", 92731, 158, 155),
    ("4", "Train", "09_train_wide_plate_v3_720p.txt", 97019, 124, 121),
    ("5", "Bunnies", "08_bunny_field_scatter_720p.txt", 96541, 124, 121),
    ("6", "Soaring clouds", "06_soaring_skies_v4_fast_kite_720p.txt", 94783, 158, 155),
    ("7", "Shrine", "07_mountain_shrine_v4_walk_reel_close_720p.txt", 94931, 243, 240),
]

SUNO_PROMPT = (
    "Instrumental countryside adventure film score; one seamless through-composed 52s cue, "
    "84 BPM, flowing 6/8, G major with brief E minor. 0-10s: immediately state a memorable "
    "rising theme in felt piano and lyrical flute over harp harmonics and thin luminous strings; "
    "warm exposition. 10-25s: gain joyful forward motion with restrained pizzicato, cello "
    "ostinato, oboe countermelody and widening chamber strings. 25-35s: playful elegant momentum "
    "for train and bunnies, agile woodwinds and soft orchestral percussion. 35-42s: fast airborne "
    "lift with harp sweeps and soaring strings as the kite climbs. 42-52s: breathe and broaden for "
    "the shrine; warm horns and full luminous strings state the theme calmly and powerfully over a "
    "low G-D pedal. Complete an authentic G-major cadence by 49s, then piano resolution, harp "
    "resonance, decrescendo and a natural concert-hall tail fully complete at 52s. Acoustic "
    "orchestra, crisp detail, wide dynamics, seamless across cuts."
)

SUNO_EXCLUDE = (
    "vocals, singing, choir, spoken word, pop song, J-pop, EDM, synthesizer lead, electronic "
    "drums, drum kit, electric guitar, distorted guitar, trap, trailer braams, heavy percussion, "
    "comedy music, ambient drone intro, abrupt ending, false ending, unresolved cadence, silence "
    "gap, hard reset, loop, sudden stop, clipped reverb tail"
)


def manifest_records(data: dict) -> list[dict]:
    if isinstance(data.get("assets"), list):
        return data["assets"]
    if isinstance(data.get("scenes"), list):
        return data["scenes"]
    if isinstance(data.get("scene"), dict):
        return [data["scene"]]
    return []


def resolve_seed(data: dict, record: dict) -> str:
    if record.get("seed") is not None:
        return str(record["seed"])
    slug = record.get("slug", "")
    if isinstance(data.get("seeds"), dict) and slug in data["seeds"]:
        return str(data["seeds"][slug])
    if data.get("seed") is not None:
        return str(data["seed"])
    return "not recorded"


def clean_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.rstrip().splitlines())


def append_krea_ledger(lines: list[str]) -> None:
    lines.extend([
        "## Complete Krea prompt and seed ledger",
        "",
        "Every checked-in Krea PNG is under `assets/krea/`. The PNGs retain ComfyUI metadata; "
        "the JSON manifests are also retained under `manifests/krea/`. The following ledger is "
        "generated directly from those manifests so the README and machine-readable records stay aligned.",
        "",
    ])
    for manifest in sorted((ROOT / "manifests/krea").glob("*/manifest.json")):
        data = json.loads(manifest.read_text())
        rel = manifest.relative_to(ROOT).as_posix()
        lines.extend([
            f"### {manifest.parent.name}",
            "",
            f"Manifest: [`{rel}`]({rel})",
            "",
        ])
        for record in manifest_records(data):
            slug = record.get("slug", "unnamed")
            seed = resolve_seed(data, record)
            prompt = clean_text(record.get("prompt", ""))
            lines.extend([
                "<details>",
                f"<summary><code>{slug}</code> - seed <code>{seed}</code></summary>",
                "",
                "```text",
                prompt,
                "```",
                "",
                "</details>",
                "",
            ])


def append_h3_archive(lines: list[str]) -> None:
    final_by_file = {row[2]: row[3] for row in FINAL_H3}
    lines.extend([
        "## Complete H3 prompt archive",
        "",
        "All retained H3 prompt iterations are reproduced below. A seed is shown where that exact "
        "prompt was used by a selected final render; exploratory prompts without a selected output "
        "are labeled accordingly rather than inventing a seed.",
        "",
    ])
    for prompt_file in sorted((ROOT / "prompts/h3").glob("*.txt")):
        rel = prompt_file.relative_to(ROOT).as_posix()
        seed = final_by_file.get(prompt_file.name)
        seed_label = f"final render seed `{seed}`" if seed is not None else "exploration prompt; no selected-render seed"
        lines.extend([
            "<details>",
            f"<summary><code>{prompt_file.name}</code> - {seed_label}</summary>",
            "",
            f"Source: [`{rel}`]({rel})",
            "",
            "```text",
            clean_text(prompt_file.read_text()),
            "```",
            "",
            "</details>",
            "",
        ])


def build() -> str:
    lines = [
        "# Skythread",
        "",
        "A reproducible reference-to-video workflow for a short vertical animated film: generate "
        "separate character, object, and environment references with Krea 2; animate one H3 R2V "
        "generation per scene; lock picture; then compose and conform a Suno score to the final cut.",
        "",
        "![Skythread Krea reference contact sheet](assets/krea/Skythread_Environment_Refs_V1/contact_sheet.png)",
        "",
        "## Attribution",
        "",
        "The H3 R2V reference-ordering and structured-prompt approach was adapted from "
        "[u/Time-Ad-7720's Reddit post, *Assemble The Multiverse | Minimax H3 R2V is awesome!*]"
        "(https://www.reddit.com/r/StableDiffusion/comments/1vgf6qx/assemble_the_multiverse_minimax_h3_r2v_is_awesome/). "
        "The included base H3 workflow is Comfy-Org's "
        "[official MiniMax H3 R2V template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json).",
        "",
        "## Process brief",
        "",
        "1. **Build clean references.** Generate Hana as a single character sheet, the kite as a "
        "single plain-white object sheet, and each location as an empty environment plate. Krea 2 "
        "uses a different seed for every requested asset and the HoloSomnia style LoRA at `0.4`.",
        "2. **Assign reference authority.** H3 receives Picture 1 = Hana, Picture 2 = kite, Picture 3 "
        "= environment. The prompt explicitly says what identity, geometry, style, and composition "
        "each picture controls, and what must not leak between them.",
        "3. **Animate one scene per generation.** Write timed action beats, screen direction, subject "
        "scale, camera path, background wind/light motion, topology constraints, and soundscape. "
        "Scene durations vary with the action rather than using a shared fixed duration.",
        "4. **Lock picture once.** The selected order is cabin, path-energy, mountain, train, bunnies, "
        "soaring clouds, shrine. Exactly the last three frames of each raw clip were omitted in the "
        "picture-locked assembly; no mid-clip trimming was used.",
        "5. **Score after picture lock.** Generate one through-composed Suno instrumental against the "
        "known cut map, then minimally conform it to the exact runtime and retain low-level H3 ambience.",
        "6. **Finish without aspect distortion.** To remove the model's right-edge band, take an exact "
        "`675x1200` 9:16 crop (`x=0`, `y=40`), scale proportionally to `720x1280`, process frame-exact "
        "scene chunks through SeedVR2 at `1.5x`, concatenate every frame, and remux the untouched mix "
        "audio for a final `1080x1920` master.",
        "",
        "## Repository map",
        "",
        "- `workflows/comfyui/`: loadable Krea 2, official MiniMax H3 R2V, and native/legacy SeedVR2 video workflow JSON.",
        "- `workflows/python/`: API runners used for Krea references, H3 clips, and SeedVR2 finishing.",
        "- `assets/krea/`: generated PNGs and contact sheets with embedded ComfyUI metadata.",
        "- `manifests/krea/`: machine-readable Krea prompts, seeds, dimensions, and model settings.",
        "- `prompts/h3/`: selected and exploratory structured H3 prompts.",
        "",
        "Model weights are intentionally not committed. Install the named models in the paths used "
        "by the runners or edit those names for your ComfyUI installation.",
        "",
        "## Final H3 render ledger",
        "",
        "All selected renders are `720x1280`, 24 fps, 20 steps, beta scheduler, `res_multistep`, "
        "and one generation per scene. `Used frames` is the raw frame count minus exactly three.",
        "",
        "| Scene | Shot | Prompt | Seed | Raw frames | Used frames |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for scene, shot, prompt, seed, raw, used in FINAL_H3:
        lines.append(f"| {scene} | {shot} | [`{prompt}`](prompts/h3/{prompt}) | `{seed}` | {raw} | {used} |")

    lines.extend([
        "",
        "The used-frame sequence is `240, 206, 155, 121, 121, 155, 240` = **1,238 frames** "
        "= **51.584 seconds** at 24 fps.",
        "",
        "## Suno score and mix",
        "",
        "Selected Suno generation: "
        "[Skythread - Seven Scene Final Score](https://suno.com/song/b7cac8df-d83b-4ee0-9bc8-71f49e03ee6b). "
        "Settings: instrumental, Suno v5.5, custom duration `0:52`.",
        "",
        "### Style prompt",
        "",
        "```text",
        SUNO_PROMPT,
        "```",
        "",
        "### Exclude styles",
        "",
        "```text",
        SUNO_EXCLUDE,
        "```",
        "",
        "Picture-lock cut points: `10.000000`, `18.583333`, `25.041667`, `30.083333`, "
        "`35.125000`, `41.583333` seconds. The selected score was minimally conformed to "
        "`51.584` seconds, mixed at `-3 dB`, and combined with original H3 ambience at `0.16` gain "
        "using 100 ms seam crossfades.",
        "",
        "## Example commands",
        "",
        "Run the checked-in H3 API runner with Picture 1 = Hana, Picture 2 = kite, and Picture 3 = scene:",
        "",
        "```bash",
        "python workflows/python/run_minimax_h3_r2v.py \\",
        "  --server http://127.0.0.1:8189 \\",
        "  --ref assets/krea/City_Kite_Demo_Krea_Refs/01_hana_character_00001_.png \\",
        "  --ref assets/krea/City_Kite_Demo_Krea_Refs/02_white_kite_00001_.png \\",
        "  --ref assets/krea/Skythread_Environment_Refs_V1/01_mountain_path_00001_.png \\",
        "  --prompt-file prompts/h3/02_mountain_path_v3_proposed.txt \\",
        "  --width 720 --height 1280 --length 195 --seed 88402 \\",
        "  --output-prefix video/Skythread/02_path_energy",
        "```",
        "",
        "SeedVR2 finishing uses `seedvr2_3b_int8_convrot.safetensors`, "
        "`seedvr2_ema_vae_fp16.safetensors`, seed `744319021`, `LAB` color correction, "
        "512-pixel tiles with 128-pixel overlap, and 1.5x proportional scaling.",
        "",
    ])
    append_krea_ledger(lines)
    append_h3_archive(lines)
    lines.extend([
        "## Licensing",
        "",
        "Code and workflow glue are released under the MIT License. Generated reference artwork is "
        "included for reproducibility; copyright in those media assets remains with the repository owner.",
        "",
    ])
    return "\n".join(lines)


if __name__ == "__main__":
    (ROOT / "README.md").write_text(build())

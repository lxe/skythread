#!/usr/bin/env python3
"""Generate seven Skythread V3 storyboard stills with Krea2 + HoloSomnia."""

from __future__ import annotations

import json
from pathlib import Path
import time
from uuid import uuid4

from run_krea2_desert_vignette_stills import request_json


HOLO = Path(__file__).resolve().parent
OUTPUT_PREFIX = "Skythread_V3_Krea_Lora04_PromptV5"
MANIFEST = HOLO / "output" / OUTPUT_PREFIX / "manifest.json"
WIDTH = 720
HEIGHT = 1280
STYLE_LORA_STRENGTH = 0.4

HANA = (
    "Hana, a single eleven-year-old East Asian girl with a chin-length black bob and "
    "warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream "
    "short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red "
    "canvas shoes"
)

KITE = (
    "a single plain white diamond kite the length of her torso, its unmarked white paper "
    "stretched over a simple bamboo cross and finished with two narrow white ribbon tails"
)

STYLE = (
    "The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with "
    "sculpted forms and deep layered space. A vast bright golden-hour sky soars above the "
    "landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, "
    "and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike "
    "their luminous pink and violet faces, and reflect across wet ground and water as "
    "radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp "
    "white against the saturated sky."
)

OVERHEAD_STYLE = (
    "The image is a polished vertical HoloSomnia-style cel-shaded anime illustration "
    "with flowing organic shapes and sculpted surface detail. Water mirrors brilliant pink "
    "and purple golden-hour clouds, crossed by luminous bands of reflected sunlight in "
    "warm gold, magenta, and lavender. The unmarked white kite remains crisp white."
)

SCENES = [
    {
        "slug": "01_veranda_start",
        "seed": 31017,
        "prompt": (
            "A child-eye-level medium-wide view across the wet wooden veranda of a cedar "
            "farmhouse in a Japanese mountain village after rain. "
            + HANA
            + ", kneels right-of-center facing toward the open right side of the veranda, "
            "testing a small dark-wood spool in both hands. Behind her in the lower-left "
            "third rests "
            + KITE
            + ", leaning upright with its full diamond silhouette visible and its cream "
            "string connected directly to her spool. A pale doorway "
            "curtain, a glass wind chime, wet leaves, and irregular hand-shaped rice "
            "terraces curving around the distant mountains create restrained depth. The "
            "right side remains open for her next movement. "
            + STYLE
        ),
    },
    {
        "slug": "02_village_start",
        "seed": 44291,
        "prompt": (
            "A high three-quarter medium-wide view looking down a narrow sunlit lane in "
            "the same Japanese mountain village after rain. "
            + HANA
            + ", runs naturally from the lower-left toward the lower-right while holding a "
            "small dark-wood spool. "
            + KITE.capitalize()
            + " trails behind her in the upper-left third above the tiled roofs, and its "
            "taut cream string forms a clean backward diagonal to the spool in her hands. "
            "Her entire body is clearly separated from the background. White laundry, "
            "indigo towels, persimmon leaves, wooden shop curtains, and receding telephone "
            "wires guide the lane toward green mountains beneath tall summer clouds. "
            + STYLE
        ),
    },
    {
        "slug": "03_rice_start",
        "seed": 58733,
        "prompt": (
            "A low lateral medium-wide view beside luminous rice terraces in the same "
            "Japanese mountain village after rain. "
            + KITE.capitalize()
            + " trails left-of-center at chest height behind "
            + HANA
            + ", who runs toward the right on the same depth plane in a balanced stride, "
            "holding a small dark-wood "
            "spool as the cream string connects her hands to the airborne diamond. "
            "Dry grass and sparse blue and yellow wildflowers fill the lower foreground. "
            "Lush green paddies follow the mountain contours in broad hand-built curves, "
            "with irregular grassy banks, varied widths, and gentle asymmetry leading "
            "toward dark cedar roofs and blue hills. Open air clearly separates both "
            "subjects from the landscape. "
            + STYLE
        ),
    },
    {
        "slug": "04_canal_start",
        "seed": 69109,
        "prompt": (
            "The camera points perpendicular to the ground in an exact straight-down "
            "aerial view. A narrow blue-green irrigation canal meanders from the top edge "
            "to the bottom edge through rice paddies shaped by the natural terrain. Their "
            "hand-built grassy banks bend in loose asymmetrical curves, with varied field "
            "sizes and softly uneven margins. "
            + KITE.capitalize()
            + " flies above the center of the canal, its full diamond silhouette crisp "
            "against the dark water while its cream string continues through the bottom "
            "edge. Neat rows of rice seedlings, submerged round stones, and slow ripples "
            "create calm flowing patterns around the central flight path. "
            + OVERHEAD_STYLE
        ),
    },
    {
        "slug": "05_train_start",
        "seed": 80473,
        "prompt": (
            "A low wide view beside a rural railway crossing at the edge of the same "
            "Japanese mountain village after rain. "
            + HANA
            + ", moves cautiously toward the right in the lower-right third behind a "
            "lowered black-and-amber crossing gate, both hands holding a small dark-wood "
            "spool. "
            + KITE.capitalize()
            + " trails high behind her in the upper-left third, clearly separated from the "
            "clouds, with its taut cream string crossing the open sky to her hands. Parallel "
            "rails remain visible through the center and curve into rice fields and cedar "
            "houses. Blue hydrangeas and wet grass frame the bottom corners. Violet storm "
            "clouds advance from the upper-left while warm light survives at the right edge. "
            + STYLE
        ),
    },
    {
        "slug": "06_cloud_start",
        "seed": 91831,
        "prompt": (
            "An immense upward-looking aerial view inside a corridor of violet-blue storm "
            "clouds above the same Japanese mountain valley. "
            + KITE.capitalize()
            + " climbs diagonally through the lower-middle, pulled from beyond the bottom-right "
            "edge so its two white tails stream backward toward the lower-left. Fine rain "
            "slants across the frame and the cream string descends toward irregular curved "
            "rice terraces far below. Immense bright pink and purple cloud walls curl inward "
            "around a radiant opening as powerful golden sunbeams fan through the corridor. "
            + STYLE
        ),
    },
    {
        "slug": "07_shrine_start",
        "seed": 104729,
        "prompt": (
            "A calm medium-wide view on a weathered mountaintop shrine terrace at luminous "
            "amber sunset, overlooking the same Japanese mountain village. A vermilion "
            "torii forms a strong rectangular frame around "
            + HANA
            + ", who walks slowly toward the right beneath it, shoulders relaxed as she "
            "looks back and holds a small dark-wood spool. "
            + KITE.capitalize()
            + " descends behind her through the upper-left opening of the torii, connected "
            "directly to her hands by a gently taut cream string. Far below, irregular "
            "curved rice terraces, tiny cedar roofs, and a thin railway settle into "
            "blue-green shadow. "
            "A bronze shrine bell hangs near one upper corner as immense amber-edged clouds "
            "open beyond the ridge. The mood is quiet, powerful, and resolved. "
            + STYLE
        ),
    },
]


def graph(scene: dict) -> dict:
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
            "inputs": {"clip": ["4", 0], "text": scene["prompt"]},
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
                "seed": scene["seed"],
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
                "filename_prefix": f"{OUTPUT_PREFIX}/{scene['slug']}",
            },
        },
    }


def main() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    client_id = str(uuid4())
    manifest = {
        "width": WIDTH,
        "height": HEIGHT,
        "seeds": {scene["slug"]: scene["seed"] for scene in SCENES},
        "model": "krea2/Krea2_Raw_convrot_int8mixed.safetensors",
        "turbo_lora": "krea2/krea2_raw_to_turbo_r256_comfy.safetensors",
        "style_lora": "krea2/holosomnia-krea2-style-v3-full.safetensors",
        "style_lora_strength": STYLE_LORA_STRENGTH,
        "scenes": [],
    }
    queued: dict[str, dict] = {}

    for scene in SCENES:
        response = request_json(
            "/prompt", {"prompt": graph(scene), "client_id": client_id}
        )
        prompt_id = response["prompt_id"]
        job = {**scene, "prompt_id": prompt_id}
        queued[prompt_id] = job
        manifest["scenes"].append(job)
        print(f"queued {scene['slug']} prompt_id={prompt_id}", flush=True)

    deadline = time.monotonic() + 3600
    pending = set(queued)
    while pending:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"timed out waiting for {len(pending)} stills")
        for prompt_id in list(pending):
            record = request_json(f"/history/{prompt_id}").get(prompt_id)
            if not record:
                continue
            status = record.get("status", {})
            for message in status.get("messages", []):
                if message and message[0] in {
                    "execution_error",
                    "execution_interrupted",
                }:
                    raise RuntimeError(f"ComfyUI {message[0]}: {message[1]}")
            if not status.get("completed", False):
                continue
            images = record.get("outputs", {}).get("11", {}).get("images", [])
            if len(images) != 1:
                raise RuntimeError(
                    f"expected one image for {prompt_id}, got {images!r}"
                )
            queued[prompt_id]["output"] = images[0]
            pending.remove(prompt_id)
            print(
                f"complete {queued[prompt_id]['slug']} output={images[0]}",
                flush=True,
            )
        if pending:
            time.sleep(3)

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"manifest={MANIFEST}", flush=True)


if __name__ == "__main__":
    main()

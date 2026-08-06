# Skythread

A reproducible reference-to-video workflow for a short vertical animated film: generate separate character, object, and environment references with Krea 2; animate one H3 R2V generation per scene; lock picture; then compose and conform a Suno score to the final cut.

![Skythread Krea reference contact sheet](assets/krea/Skythread_Environment_Refs_V1/contact_sheet.png)

## Attribution

The H3 R2V reference-ordering and structured-prompt approach was adapted from [u/Time-Ad-7720's Reddit post, *Assemble The Multiverse | Minimax H3 R2V is awesome!*](https://www.reddit.com/r/StableDiffusion/comments/1vgf6qx/assemble_the_multiverse_minimax_h3_r2v_is_awesome/). The included base H3 workflow is Comfy-Org's [official MiniMax H3 R2V template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json).

## Process brief

1. **Build clean references.** Generate Hana as a single character sheet, the kite as a single plain-white object sheet, and each location as an empty environment plate. Krea 2 uses a different seed for every requested asset and the HoloSomnia style LoRA at `0.4`.
2. **Assign reference authority.** H3 receives Picture 1 = Hana, Picture 2 = kite, Picture 3 = environment. The prompt explicitly says what identity, geometry, style, and composition each picture controls, and what must not leak between them.
3. **Animate one scene per generation.** Write timed action beats, screen direction, subject scale, camera path, background wind/light motion, topology constraints, and soundscape. Scene durations vary with the action rather than using a shared fixed duration.
4. **Lock picture once.** The selected order is cabin, path-energy, mountain, train, bunnies, soaring clouds, shrine. Exactly the last three frames of each raw clip were omitted in the picture-locked assembly; no mid-clip trimming was used.
5. **Score after picture lock.** Generate one through-composed Suno instrumental against the known cut map, then minimally conform it to the exact runtime and retain low-level H3 ambience.
6. **Finish without aspect distortion.** To remove the model's right-edge band, take an exact `675x1200` 9:16 crop (`x=0`, `y=40`), scale proportionally to `720x1280`, process frame-exact scene chunks through SeedVR2 at `1.5x`, concatenate every frame, and remux the untouched mix audio for a final `1080x1920` master.

## Repository map

- `workflows/comfyui/`: loadable Krea 2, official MiniMax H3 R2V, and native/legacy SeedVR2 video workflow JSON.
- `workflows/python/`: API runners used for Krea references, H3 clips, and SeedVR2 finishing.
- `assets/krea/`: generated PNGs and contact sheets with embedded ComfyUI metadata.
- `manifests/krea/`: machine-readable Krea prompts, seeds, dimensions, and model settings.
- `prompts/h3/`: selected and exploratory structured H3 prompts.

Model weights are intentionally not committed. Install the named models in the paths used by the runners or edit those names for your ComfyUI installation.

## Final H3 render ledger

All selected renders are `720x1280`, 24 fps, 20 steps, beta scheduler, `res_multistep`, and one generation per scene. `Used frames` is the raw frame count minus exactly three.

| Scene | Shot | Prompt | Seed | Raw frames | Used frames |
|---:|---|---|---:|---:|---:|
| 1 | Cabin start | [`01_cabin_porch.txt`](prompts/h3/01_cabin_porch.txt) | `88143` | 243 | 240 |
| 2 | Path energy | [`02_mountain_path_v3_proposed.txt`](prompts/h3/02_mountain_path_v3_proposed.txt) | `88402` | 209 | 206 |
| 3 | Mountain path | [`02_mountain_path_v4_uphill_crane.txt`](prompts/h3/02_mountain_path_v4_uphill_crane.txt) | `92731` | 158 | 155 |
| 4 | Train | [`09_train_wide_plate_v3_720p.txt`](prompts/h3/09_train_wide_plate_v3_720p.txt) | `97019` | 124 | 121 |
| 5 | Bunnies | [`08_bunny_field_scatter_720p.txt`](prompts/h3/08_bunny_field_scatter_720p.txt) | `96541` | 124 | 121 |
| 6 | Soaring clouds | [`06_soaring_skies_v4_fast_kite_720p.txt`](prompts/h3/06_soaring_skies_v4_fast_kite_720p.txt) | `94783` | 158 | 155 |
| 7 | Shrine | [`07_mountain_shrine_v4_walk_reel_close_720p.txt`](prompts/h3/07_mountain_shrine_v4_walk_reel_close_720p.txt) | `94931` | 243 | 240 |

The used-frame sequence is `240, 206, 155, 121, 121, 155, 240` = **1,238 frames** = **51.584 seconds** at 24 fps.

## Suno score and mix

Selected Suno generation: [Skythread - Seven Scene Final Score](https://suno.com/song/b7cac8df-d83b-4ee0-9bc8-71f49e03ee6b). Settings: instrumental, Suno v5.5, custom duration `0:52`.

### Style prompt

```text
Instrumental countryside adventure film score; one seamless through-composed 52s cue, 84 BPM, flowing 6/8, G major with brief E minor. 0-10s: immediately state a memorable rising theme in felt piano and lyrical flute over harp harmonics and thin luminous strings; warm exposition. 10-25s: gain joyful forward motion with restrained pizzicato, cello ostinato, oboe countermelody and widening chamber strings. 25-35s: playful elegant momentum for train and bunnies, agile woodwinds and soft orchestral percussion. 35-42s: fast airborne lift with harp sweeps and soaring strings as the kite climbs. 42-52s: breathe and broaden for the shrine; warm horns and full luminous strings state the theme calmly and powerfully over a low G-D pedal. Complete an authentic G-major cadence by 49s, then piano resolution, harp resonance, decrescendo and a natural concert-hall tail fully complete at 52s. Acoustic orchestra, crisp detail, wide dynamics, seamless across cuts.
```

### Exclude styles

```text
vocals, singing, choir, spoken word, pop song, J-pop, EDM, synthesizer lead, electronic drums, drum kit, electric guitar, distorted guitar, trap, trailer braams, heavy percussion, comedy music, ambient drone intro, abrupt ending, false ending, unresolved cadence, silence gap, hard reset, loop, sudden stop, clipped reverb tail
```

Picture-lock cut points: `10.000000`, `18.583333`, `25.041667`, `30.083333`, `35.125000`, `41.583333` seconds. The selected score was minimally conformed to `51.584` seconds, mixed at `-3 dB`, and combined with original H3 ambience at `0.16` gain using 100 ms seam crossfades.

## Example commands

Run the checked-in H3 API runner with Picture 1 = Hana, Picture 2 = kite, and Picture 3 = scene:

```bash
python workflows/python/run_minimax_h3_r2v.py \
  --server http://127.0.0.1:8189 \
  --ref assets/krea/City_Kite_Demo_Krea_Refs/01_hana_character_00001_.png \
  --ref assets/krea/City_Kite_Demo_Krea_Refs/02_white_kite_00001_.png \
  --ref assets/krea/Skythread_Environment_Refs_V1/01_mountain_path_00001_.png \
  --prompt-file prompts/h3/02_mountain_path_v3_proposed.txt \
  --width 720 --height 1280 --length 195 --seed 88402 \
  --output-prefix video/Skythread/02_path_energy
```

SeedVR2 finishing uses `seedvr2_3b_int8_convrot.safetensors`, `seedvr2_ema_vae_fp16.safetensors`, seed `744319021`, `LAB` color correction, 512-pixel tiles with 128-pixel overlap, and 1.5x proportional scaling.

## Complete Krea prompt and seed ledger

Every checked-in Krea PNG is under `assets/krea/`. The PNGs retain ComfyUI metadata; the JSON manifests are also retained under `manifests/krea/`. The following ledger is generated directly from those manifests so the README and machine-readable records stay aligned.

### Cabin_Porch_Demo_Krea_Scene

Manifest: [`manifests/krea/Cabin_Porch_Demo_Krea_Scene/manifest.json`](manifests/krea/Cabin_Porch_Demo_Krea_Scene/manifest.json)

<details>
<summary><code>01_cabin_porch_environment</code> - seed <code>73147</code></summary>

```text
A polished vertical HoloSomnia-style cel-shaded anime environment plate of a rustic cedar cabin porch overlooking an extraordinarily beautiful mountain landscape at golden hour. Broad rain-polished wooden boards fill the open lower half of the composition and run toward screen-right, creating a clear path for movement. The cabin wall, dark timber posts, an open doorway, and a small glass wind chime frame the left edge; a low railing and three shallow steps frame the right edge without blocking the deck. Beyond the porch, wildflower meadows descend toward a luminous winding lake, layered pine ridges, and distant blue mountains. The porch center is empty, uncluttered, and fully visible. A vast bright sky is filled with soaring pink and purple clouds, while strong golden sunbeams stream through their gaps and reflect in gold, magenta, and lavender across the wet wood, lake, and glass. Clean sculpted forms, deep atmospheric layers, crisp cel shading, iridescent cloud light, and serene cinematic depth define the image.
```

</details>

### City_Kite_Demo_Krea_Refs

Manifest: [`manifests/krea/City_Kite_Demo_Krea_Refs/manifest.json`](manifests/krea/City_Kite_Demo_Krea_Refs/manifest.json)

<details>
<summary><code>01_hana_character</code> - seed <code>21137</code></summary>

```text
A polished vertical HoloSomnia-style cel-shaded anime character reference illustration of one full-body figure. Hana is an eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, and natural child proportions. She wears a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. She stands in a relaxed three-quarter profile facing toward the right, both arms resting naturally at her sides and every garment fully visible. Her expression is gentle, alert, and quietly determined. The uncluttered background is a pale lavender-to-pink studio gradient with a soft oval ground shadow. Clean sculpted forms, precise cel shading, subtle iridescent rim light, and a pristine animation-model-sheet finish define the image.
```

</details>

<details>
<summary><code>02_white_kite</code> - seed <code>42281</code></summary>

```text
A polished vertical HoloSomnia-style cel-shaded prop reference illustration showing one centered plain white diamond kite from the front. Its smooth white paper face is completely unmarked, stretched into a clean symmetrical diamond with a fine warm-grey perimeter and a simple pale bamboo cross visible beneath the paper. Two narrow white ribbon tails extend separately from the bottom point and curve gently downward, both fully visible. A single thin cream string leads from the kite to a small dark-wood spool arranged neatly near the lower edge. The object is isolated against a luminous cobalt-to-lavender sky gradient with soft pink reflected light, crisp silhouette separation, and restrained shadows.
```

</details>

<details>
<summary><code>03_city_start</code> - seed <code>67309</code></summary>

```text
A dynamic vertical HoloSomnia-style cel-shaded anime starting frame in a bright Japanese hillside city at golden hour. Hana, one eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, runs toward screen-right through the right half of a broad pedestrian street. She wears a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, and holds a small dark-wood spool. A plain unmarked white diamond kite with two narrow white ribbon tails flies behind her in the upper-left, connected by one taut cream string that forms a clean backward diagonal. Colorful mid-rise buildings, elevated walkways, glass awnings, balconies, trees, and abstract glowing shop panels create layered urban depth while the street remains open around her. Strong golden sunbeams stream between soaring bright pink and purple clouds and reflect in gold, magenta, and lavender across the rain-polished pavement. The low three-quarter camera gives Hana and the trailing kite clear, separate silhouettes and a strong forward path.
```

</details>

### Skythread_Environment_Refs_V1

Manifest: [`manifests/krea/Skythread_Environment_Refs_V1/manifest.json`](manifests/krea/Skythread_Environment_Refs_V1/manifest.json)

<details>
<summary><code>01_mountain_path</code> - seed <code>74101</code></summary>

```text
A child-height medium-wide view along a broad mountain footpath just beyond a rustic cedar cabin. The dry earth-and-stone path enters from the lower-left, curves smoothly toward screen-right through an open foreground, then descends toward a distant Japanese hillside village. Low split-cedar fences, sparse blue and yellow wildflowers, mossy stones, and wind-bent grasses frame the route without obstructing it. Organic mountain contours, pine groves, a winding lake, and layered blue ridges connect this place to the cabin landscape. The path is empty, uncluttered, and clearly readable as one continuous rightward movement corridor. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

<details>
<summary><code>02_rice_fields</code> - seed <code>74237</code></summary>

```text
A low lateral medium-wide view across beautiful hand-built rice terraces in the same Japanese mountain valley. A dry raised footpath runs continuously from screen-left to screen-right through the lower-middle of the composition, with a broad unobstructed surface and sparse wildflowers along its edges. The paddies follow the natural contours in large flowing curves, with irregular grassy banks, varied widths, asymmetrical shapes, and gently winding irrigation water. Dark cedar farmhouses sit far apart among pine-covered slopes, while a luminous lake and distant blue mountains deepen the view. The environment is serene and open, designed around a clear lateral movement path. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

<details>
<summary><code>03_aerial_path_mountains</code> - seed <code>74381</code></summary>

```text
An exact bird's-eye environment view looking straight down over the folded terrain of the same mountain valley. A pale winding footpath begins at the bottom edge and snakes upward through irregular terraced slopes, patches of pine forest, rounded rocky outcrops, wildflower meadows, and a narrow blue stream. The mountain ridges read as broad organic contour shapes rather than geometric grids, and the trail remains visible as one continuous ribbon across the entire frame. Warm low sunlight strikes the higher ridges and casts long violet shadows, while water and pale stone carry reflected pink, purple, magenta, and gold from the surrounding golden-hour atmosphere. The map-like vertical composition is empty, flowing, and richly layered. The rendering is polished HoloSomnia-style cel-shaded anime with sculpted terrain, luminous color separation, and crisp organic detail.
```

</details>

<details>
<summary><code>04_train_crossing</code> - seed <code>74503</code></summary>

```text
A low wide environment view at a quiet rural railway crossing in the same Japanese mountain valley after rain. A broad paved footpath runs left-to-right through the open lower foreground and meets a lowered black-and-amber crossing gate at a safe waiting area. Two polished rails cut diagonally through the middle distance and curve away between organic rice fields, cedar houses, and pine-covered hills. Blue hydrangeas, wet grasses, small signal lights, and a simple wooden crossing hut frame the edges while leaving the foreground and sky clearly visible. Violet storm depth gathers over the left ridge and radiant warm light opens on the right, creating a dramatic but welcoming transition. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

<details>
<summary><code>05_soaring_skies</code> - seed <code>74629</code></summary>

```text
A vast upward-looking environment view inside an immense soaring cloud corridor above the same Japanese mountain valley. Sculpted banks of brilliant pink, purple, violet, cobalt, peach, and pale cyan clouds curl along the left and right edges, forming a broad diagonal passage from the lower-left toward a radiant opening in the upper-right. Powerful golden-hour sunbeams fan through the gap, strike the luminous cloud faces, and create transparent shafts of gold, magenta, and lavender light. Far below at the bottom edge, organic curved rice terraces, pine ridges, and a threadlike lake recede through blue atmospheric depth. The central sky route is open, grand, and clearly readable for continuous flight. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

<details>
<summary><code>06_mountain_shrine</code> - seed <code>74771</code></summary>

```text
A calm medium-wide environment view across a weathered mountaintop shrine terrace in the same Japanese mountain valley. A tall vermilion torii frames the center without blocking a broad stone-and-earth path that enters from the lower-left, passes beneath the gate, and continues toward screen-right. A small cedar shrine building sits along the left edge, while one bronze bell, white prayer streamers, mossy lanterns, and wind-shaped grasses provide restrained detail around the open terrace. Far below, organic curved rice terraces, tiny cedar roofs, a thin railway, and the winding lake settle into layered blue-green shadow. Immense pink and purple clouds open around the low sun beyond the ridge, creating a quiet, powerful, and resolved landscape. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

### Skythread_Insert_Environment_Refs_V2

Manifest: [`manifests/krea/Skythread_Insert_Environment_Refs_V2/manifest.json`](manifests/krea/Skythread_Insert_Environment_Refs_V2/manifest.json)

<details>
<summary><code>01_bunny_field_environment</code> - seed <code>96121</code></summary>

```text
A low animal-eye-level lateral environment view across a gently sloping summer field in the same Japanese mountain valley. In the immediate lower foreground, exactly four natural wild rabbits, two adults and two smaller kits, gather beside one low weathered rectangular wooden water trough filled with clear water and one compact rectangular golden hay bale. Each rabbit has a separate readable body, correct anatomy, upright alert ears, and a distinct position around the trough. All four have turned their heads toward the open left side of the background and are poised to spring in different directions. Across the unobstructed middle background, one broad dry field path runs continuously from screen-left to screen-right with generous empty space for a distant runner to be added later. Wind-shaped grasses, sparse blue and yellow wildflowers, a cedar fence, irregular curved paddies, pine ridges, and a luminous lake create three clean depth layers. The entire upper sky remains open for a distant flying object to be added later. No people, no kite, no string, no spool, no other animals, no duplicate trough, and no duplicate hay bale. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

<details>
<summary><code>02_train_tracking_environment</code> - seed <code>96307</code></summary>

```text
A stabilized low lateral wide environment view beside a rural railway in the same Japanese mountain valley after rain. One broad safe packed-earth footpath runs horizontally from screen-left to screen-right across the open lower foreground, leaving a long unobstructed movement corridor. One simple cedar fence separates the path from one straight horizontal railway track in the middle distance. Exactly one coherent cream-and-vermilion two-car local electric train is seen in clean side elevation on that track, oriented left-to-right, with consistent windows, doors, roof equipment, wheel spacing, and carriage scale. Preserve generous open lead room at screen-right and clear separation between foreground path, fence, and train for a smooth lateral tracking shot. Wet grasses, blue hydrangeas, organic curved rice fields, sparse cedar houses, and pine-covered hills recede into the valley. The sky is broad and unobstructed. No people, no kite, no string, no spool, no second train, no crossing collision, no Dutch angle, and no motion blur. The image is a polished vertical HoloSomnia-style cel-shaded anime environment plate with clean sculpted forms, deep atmospheric layers, luminous iridescent highlights, and a pristine cinematic finish. Bright golden-hour light pours through soaring pink and purple clouds, creating visible sunbeams and reflected bands of gold, magenta, and lavender across the landscape.
```

</details>

### Skythread_Insert_Refs_V1

Manifest: [`manifests/krea/Skythread_Insert_Refs_V1/manifest.json`](manifests/krea/Skythread_Insert_Refs_V1/manifest.json)

<details>
<summary><code>01_bunny_field_start</code> - seed <code>95113</code></summary>

```text
A low animal-eye-level lateral wide shot across a gently sloping summer field in the same Japanese mountain valley. The composition has three clean depth layers. In the immediate lower foreground, exactly four natural wild rabbits, two adults and two smaller kits, gather beside one low weathered wooden water trough filled with clear water and one compact rectangular golden hay bale. All four rabbits have turned their ears and faces toward the background runner; their bodies are separate, anatomically correct, and poised to spring in different directions, but none has moved yet. In the unobstructed middle background, exactly one Hana, an eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes runs naturally from screen-left toward screen-right along one horizontal field path, small enough to remain clearly behind the rabbits. She holds the dark-wood spool in her right hand. Exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, a simple pale bamboo cross, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool flies high behind Hana in the upper-left, well separated from her, with one long taut cream line connected directly to the spool. The kite trails behind her travel direction and never appears in her hand. Wind-shaped grasses, sparse blue and yellow wildflowers, a distant cedar fence, irregular paddies, pine ridges, and a luminous lake create an open rightward movement corridor. Exactly one girl, four rabbits, one trough, one hay bale, and one kite; no other people or animals. Polished vertical HoloSomnia-style hand-painted cel animation, crisp stable inked contours, flat two-tone cel shading, matte gouache and watercolor texture, clean sculpted forms, deep layered atmospheric perspective, and controlled 2D multiplane depth. Bright golden-hour sunlight pours through immense pink, purple, peach, pale-cyan, and cobalt clouds, creating visible stable rays and reflected bands of gold, magenta, and lavender. Keep the white kite crisp and plain against the saturated landscape.
```

</details>

<details>
<summary><code>02_topdown_kite_birds_start</code> - seed <code>95267</code></summary>

```text
The camera points exactly perpendicular to the earth in a strict ninety-degree straight-down aerial view with no horizon and no oblique perspective. Far below, organic asymmetrical rice paddies, a narrow blue-green irrigation channel, rounded meadow edges, scattered stones, and small pine clusters form flowing map-like shapes. At the exact visual center flies exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, a simple pale bamboo cross, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool, seen cleanly from above with its complete diamond silhouette, bamboo cross, and two separate tails readable. Its single cream string continues straight through the bottom edge toward unseen Hana. Exactly three small barn swallows fly around the kite at different distances in one loose clockwise arc: one near upper-left, one at frame-right, and one lower-right. Each bird is a separate clean dark-and-cream silhouette with two wings, one head, and a forked tail; no overlap, flock clump, or extra birds. Reflected pink-purple clouds and long gold sunbeams shimmer in the irrigation water while soft cloud shadows cross the fields. The graphic composition is spacious and calm, designed for the birds to circle and peel away from the kite. Polished vertical HoloSomnia-style hand-painted cel animation, crisp stable inked contours, flat two-tone cel shading, matte gouache and watercolor texture, clean sculpted forms, deep layered atmospheric perspective, and controlled 2D multiplane depth. Bright golden-hour sunlight pours through immense pink, purple, peach, pale-cyan, and cobalt clouds, creating visible stable rays and reflected bands of gold, magenta, and lavender. Keep the white kite crisp and plain against the saturated landscape.
```

</details>

<details>
<summary><code>03_train_tracking_start</code> - seed <code>95419</code></summary>

```text
A stabilized low lateral wide composition beside a rural railway in the same Japanese mountain valley after rain. The foreground contains one broad safe footpath running horizontally from screen-left to screen-right, separated from the railway by one simple cedar fence. Exactly one hana, an eleven-year-old east asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes runs left-to-right in a lively balanced stride on the foreground path, shown full-body in three-quarter side profile with generous open lead room ahead. She holds the small dark-wood spool in her right hand. Exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, a simple pale bamboo cross, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool remains high and behind her in the upper-left, connected to the spool by one long taut cream line and trailing clearly opposite her direction of travel. In the middle distance, exactly one cream-and-vermilion local electric train passes left-to-right on one straight horizontal track parallel to Hana. Its scale, windows, doors, wheels, and carriage geometry remain coherent and clearly behind the fence. The train and Hana travel in the same direction on separate depth planes, suitable for a smooth lateral tracking camera. Wet grasses, blue hydrangeas, curved rice fields, cedar houses, and pine-covered hills recede beneath bright multicolored clouds. Crisp frozen storyboard moment with no motion blur, Dutch angle, vibration, crossing collision, duplicate train, duplicate girl, or extra kite. Polished vertical HoloSomnia-style hand-painted cel animation, crisp stable inked contours, flat two-tone cel shading, matte gouache and watercolor texture, clean sculpted forms, deep layered atmospheric perspective, and controlled 2D multiplane depth. Bright golden-hour sunlight pours through immense pink, purple, peach, pale-cyan, and cobalt clouds, creating visible stable rays and reflected bands of gold, magenta, and lavender. Keep the white kite crisp and plain against the saturated landscape.
```

</details>

### Skythread_V3_Krea

Manifest: [`manifests/krea/Skythread_V3_Krea/manifest.json`](manifests/krea/Skythread_V3_Krea/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>73017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene one starting frame: a static child-eye-level medium-wide on the wet veranda of the cedar farmhouse in warm late-afternoon light. Hana kneels left-of-center tightening the final knot while the full upright kite rests right-of-center on the boards, both completely visible and connected by the cream string. The spool rests beside her knee. A glass wind chime, a pale doorway curtain, wet leaves, and distant laundry create restrained depth, with clear open space toward frame-right for the launch. Correct natural hands, exactly one girl, one kite, one spool, and two kite tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>73017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene two starting frame: a locked high three-quarter view down a narrow sunlit village lane. Hana is fully visible in the lower-left third beginning a natural run toward frame-right, holding the wooden spool. The full kite is already airborne above tiled roofs in the upper-left-to-middle area, the cream string drawing one clean visible diagonal between them. White laundry, indigo towels, persimmon leaves, telephone wires, shop curtains, and one bicycle form layered depth without obscuring Hana or the kite. Exactly one girl, one kite, one spool, one string, and two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>73017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene three starting frame: a low lateral view at kite height beside luminous rice terraces. The full kite occupies the left-middle foreground just above blue and yellow wildflowers, pointed toward frame-right. Hana is fully visible farther behind on a raised path in a natural running stride, holding the spool, with one cream string correctly connecting her to the kite. Reflective paddies, mountain roofs, blue hills, rice leaves, and one small blue dragonfly create strong layered depth. Do not let flowers cover the subjects. Exactly one girl, one kite, one spool, one string, two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>73017</code></summary>

```text
The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene four starting frame: an exact straight-down graphic view with no horizon. A narrow blue-green irrigation canal forms a vertical ribbon through geometric rice terraces. At the lower-left water edge, the first clear reflection of the same kite enters frame with its centered vermilion disk, dark cross spars, one string reflection, and exactly two indigo tail reflections. Two white egrets stand on opposite grassy banks; small silver fish and pale cloud reflections sit beneath the transparent water. One kite reflection only, two egrets total, no girl, no solid kite resting in water. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>73017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene five starting frame: a locked low wide beside a rural railway crossing before the train arrives. Hana stands safely behind a black-and-amber striped gate in the lower-left third, full body visible, braced and looking up while holding the spool with both hands. The full kite is airborne in the upper-right third above the tracks, connected by one taut cream string. Blue hydrangeas and wet grass fill the lower foreground, rice fields and the village recede behind, and violet-blue storm clouds advance from upper-left while a warm opening remains at frame-right. Leave the middle tracks unobstructed for the later train. Exactly one girl, one kite, one spool, one string, two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>73017</code></summary>

```text
The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene six starting frame: an immense upward-looking aerial view inside a corridor of violet-blue storm clouds. The full kite is in the lower-middle third climbing diagonally toward frame-right through fine rain, with its cream string attached and descending out of the lower edge toward tiny flat rice terraces far below. A narrow cream-and-amber opening glows high at frame-right. Giant cloud masses create a clear diagonal route. One kite only, one string, one vermilion disk, two indigo tails, no girl, no railway gate. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>73017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene seven starting frame: a calm medium-wide on a mountaintop shrine terrace at luminous amber sunset. A weathered vermilion torii frames the view. Hana stands full-body beneath it in the left-middle, calmly holding the spool and looking up. The full kite descends from the upper-left-to-middle area toward her, connected by one gently taut cream string. The valley below shows tiny village roofs, reflective rice terraces, and the railway beneath immense amber-edged clouds. One bronze bell, white prayer streamers, and a cedar branch frame the top. Exactly one girl, one kite, one spool, one string, one bell, and two kite tails. Calm, grand, resolved. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

### Skythread_V3_Krea_Lora04

Manifest: [`manifests/krea/Skythread_V3_Krea_Lora04/manifest.json`](manifests/krea/Skythread_V3_Krea_Lora04/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>31017</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene one starting frame: a static child-eye-level medium-wide on the wet veranda of the cedar farmhouse in warm late-afternoon light. Hana kneels left-of-center tightening the final knot while the full upright kite rests right-of-center on the boards, both completely visible and connected by the cream string. The spool rests beside her knee. A glass wind chime, a pale doorway curtain, wet leaves, and distant laundry create restrained depth, with clear open space toward frame-right for the launch. Correct natural hands, exactly one girl, one kite, one spool, and two kite tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>44291</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene two starting frame: a locked high three-quarter view down a narrow sunlit village lane. Hana is fully visible in the lower-left third beginning a natural run toward frame-right, holding the wooden spool. The full kite is already airborne above tiled roofs in the upper-left-to-middle area, the cream string drawing one clean visible diagonal between them. White laundry, indigo towels, persimmon leaves, telephone wires, shop curtains, and one bicycle form layered depth without obscuring Hana or the kite. Exactly one girl, one kite, one spool, one string, and two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>58733</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene three starting frame: a low lateral view at kite height beside luminous rice terraces. The full kite occupies the left-middle foreground just above blue and yellow wildflowers, pointed toward frame-right. Hana is fully visible farther behind on a raised path in a natural running stride, holding the spool, with one cream string correctly connecting her to the kite. Reflective paddies, mountain roofs, blue hills, rice leaves, and one small blue dragonfly create strong layered depth. Do not let flowers cover the subjects. Exactly one girl, one kite, one spool, one string, two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>69109</code></summary>

```text
The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene four starting frame: an exact straight-down graphic view with no horizon. A narrow blue-green irrigation canal forms a vertical ribbon through geometric rice terraces. At the lower-left water edge, the first clear reflection of the same kite enters frame with its centered vermilion disk, dark cross spars, one string reflection, and exactly two indigo tail reflections. Two white egrets stand on opposite grassy banks; small silver fish and pale cloud reflections sit beneath the transparent water. One kite reflection only, two egrets total, no girl, no solid kite resting in water. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>80473</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene five starting frame: a locked low wide beside a rural railway crossing before the train arrives. Hana stands safely behind a black-and-amber striped gate in the lower-left third, full body visible, braced and looking up while holding the spool with both hands. The full kite is airborne in the upper-right third above the tracks, connected by one taut cream string. Blue hydrangeas and wet grass fill the lower foreground, rice fields and the village recede behind, and violet-blue storm clouds advance from upper-left while a warm opening remains at frame-right. Leave the middle tracks unobstructed for the later train. Exactly one girl, one kite, one spool, one string, two tails. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>91831</code></summary>

```text
The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene six starting frame: an immense upward-looking aerial view inside a corridor of violet-blue storm clouds. The full kite is in the lower-middle third climbing diagonally toward frame-right through fine rain, with its cream string attached and descending out of the lower edge toward tiny flat rice terraces far below. A narrow cream-and-amber opening glows high at frame-right. Giant cloud masses create a clear diagonal route. One kite only, one string, one vermilion disk, two indigo tails, no girl, no railway gate. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>104729</code></summary>

```text
Hana is always the same eleven-year-old East Asian girl with a chin-length black bob, large warm dark-brown eyes, a straw sunhat with one indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Keep her face, age, proportions, clothing, and colors identical. The kite is always the same rigid handmade ivory diamond kite, about the length of Hana's torso, with exactly one perfectly centered vermilion sun disk, visible dark bamboo cross spars, exactly two long narrow indigo ribbon tails, and one thin cream string attached to one small dark-wood spool. Keep its scale, geometry, construction, and colors identical; never add another kite, disk, tail, or string. All scenes belong to one midsummer Japanese mountain village after rain: a cedar farmhouse above narrow lanes, luminous rice terraces below, a rural railway at the valley edge, giant cloud corridors overhead, and a weathered ridge shrine. Scene seven starting frame: a calm medium-wide on a mountaintop shrine terrace at luminous amber sunset. A weathered vermilion torii frames the view. Hana stands full-body beneath it in the left-middle, calmly holding the spool and looking up. The full kite descends from the upper-left-to-middle area toward her, connected by one gently taut cream string. The valley below shows tiny village roofs, reflective rice terraces, and the railway beneath immense amber-edged clouds. One bronze bell, white prayer streamers, and a cedar branch frame the top. Exactly one girl, one kite, one spool, one string, one bell, and two kite tails. Calm, grand, resolved. Rendered in the distinctive HoloSomnia style as a polished digital 3D anime illustration with sharp clean cel shading, sculpted glossy forms, smooth stylized surfaces, luminous iridescent highlights, latex-like and crystalline cloud textures, saturated cyan, cobalt, magenta, violet, vermilion, gold, orange, indigo, and emerald colors, deep high-contrast shadows, bright clean rim light, dramatic layered depth, and a pristine highly detailed finish. Cinematic native vertical 9:16 composition, one coherent frame, no text, no logo, no watermark, no split screen, no collage.
```

</details>

### Skythread_V3_Krea_Lora04_PromptV2

Manifest: [`manifests/krea/Skythread_V3_Krea_Lora04_PromptV2/manifest.json`](manifests/krea/Skythread_V3_Krea_Lora04_PromptV2/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>31017</code></summary>

```text
A child-eye-level medium-wide view across the wet wooden veranda of a cedar farmhouse in a Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, kneels in the lower-left third, her hands tightening the final knot on a single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails. It leans upright immediately to her right with its full diamond silhouette visible; the spool rests beside her left knee. A pale doorway curtain, a glass wind chime, wet leaves, and distant rice terraces create restrained depth, while the right side of the veranda remains open for her next movement. Warm late-afternoon light follows the rain. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>44291</code></summary>

```text
A high three-quarter medium-wide view looking down a narrow sunlit lane in the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs naturally from the lower-left toward the lower-right while holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies in the upper-left third above the tiled roofs, and its taut cream string forms a clean diagonal to the spool in her hands. Her entire body is clearly separated from the background. White laundry, indigo towels, persimmon leaves, wooden shop curtains, and receding telephone wires guide the lane toward green mountains beneath tall summer clouds. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>58733</code></summary>

```text
A low lateral medium-wide view beside luminous rice terraces in the same Japanese mountain village after rain. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies through the left foreground just above a sparse edge of blue and yellow wildflowers, its diamond silhouette fully visible and angled toward the right. In the middle distance on a raised path, Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs toward the right in a balanced stride, holding a small dark-wood spool as the cream string connects her hands to the airborne diamond. Reflective paddies form horizontal steps behind her, leading to dark cedar roofs, blue hills, and towering summer clouds. The foreground remains open around both subjects. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>69109</code></summary>

```text
An exact straight-down aerial view over a narrow blue-green irrigation canal that forms a vertical ribbon through geometric rice terraces in the same Japanese mountain village after rain. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies above the canal in the lower-middle of the composition, its full diamond silhouette crisp against the dark water while its string continues out through the bottom edge. Two white egrets stand far apart on opposite grassy banks. Submerged stones, small silver fish, rice seedlings, and pale cloud color are visible through the clear water, organized as calm graphic shapes around the central flight path. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>80473</code></summary>

```text
A low wide view beside a rural railway crossing at the edge of the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, stands full-body in the lower-left third behind a lowered black-and-amber crossing gate, feet braced as both hands hold a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies high in the upper-right third, clearly separated from the clouds, with its taut cream string crossing the open sky to her hands. Parallel rails remain visible through the center and curve into rice fields and cedar houses. Blue hydrangeas and wet grass frame the bottom corners. Violet storm clouds advance from the upper-left while warm light survives at the right edge. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>91831</code></summary>

```text
An immense upward-looking aerial view inside a corridor of violet-blue storm clouds above the same Japanese mountain valley. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails climbs diagonally from the lower-middle toward a narrow amber opening in the upper-right, its complete diamond silhouette isolated within a clear band of sky. Fine rain slants across the frame and the cream string descends from the kite through the bottom edge toward tiny geometric rice terraces far below. The surrounding cloud walls curl inward as immense sculpted masses, creating a grand tunnel of violet, cobalt, pale cyan, and warm gold light. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>104729</code></summary>

```text
A calm medium-wide view on a weathered mountaintop shrine terrace at luminous amber sunset, overlooking the same Japanese mountain village. A vermilion torii forms a strong rectangular frame around Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who stands full-body slightly left of center, shoulders relaxed as she looks upward and holds a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails descends through the open upper-middle of the torii, connected directly to her hands by a gently taut cream string. Far below, reflective rice terraces, tiny cedar roofs, and a thin railway settle into blue-green shadow. A bronze shrine bell hangs near one upper corner as immense amber-edged clouds open beyond the ridge. The mood is quiet, powerful, and resolved. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

### Skythread_V3_Krea_Lora04_PromptV3

Manifest: [`manifests/krea/Skythread_V3_Krea_Lora04_PromptV3/manifest.json`](manifests/krea/Skythread_V3_Krea_Lora04_PromptV3/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>31017</code></summary>

```text
A child-eye-level medium-wide view across the wet wooden veranda of a cedar farmhouse in a Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, kneels in the lower-left third, her hands tightening the final knot on a single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails. It leans upright immediately to her right with its full diamond silhouette visible; the spool rests beside her left knee. A pale doorway curtain, a glass wind chime, wet leaves, and distant rice terraces create restrained depth, while the right side of the veranda remains open for her next movement. Warm late-afternoon light follows the rain. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>44291</code></summary>

```text
A high three-quarter medium-wide view looking down a narrow sunlit lane in the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs naturally from the lower-left toward the lower-right while holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies in the upper-left third above the tiled roofs, and its taut cream string forms a clean diagonal to the spool in her hands. Her entire body is clearly separated from the background. White laundry, indigo towels, persimmon leaves, wooden shop curtains, and receding telephone wires guide the lane toward green mountains beneath tall summer clouds. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>58733</code></summary>

```text
A low lateral medium-wide view beside luminous rice terraces in the same Japanese mountain village after rain. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies left-of-center at chest height above a dry raised path, its diamond silhouette fully visible and approximately the height of a child's torso. On the same depth plane to the right, Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs toward the right in a balanced stride, holding a small dark-wood spool as the cream string connects her hands to the airborne diamond. Dry grass and sparse blue and yellow wildflowers fill the lower foreground. Lush green terraces begin behind the path and form horizontal steps toward dark cedar roofs, blue hills, and towering summer clouds. Open air clearly separates both subjects from the landscape. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>69109</code></summary>

```text
The camera points perpendicular to the ground in an exact straight-down aerial view. A narrow blue-green irrigation canal forms a vertical ribbon from the top edge to the bottom edge, surrounded on every side by rectangular rice paddies and grassy banks in the same Japanese mountain village. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies above the center of the canal, its full diamond silhouette crisp against the dark water while its cream string continues through the bottom edge. Neat rows of rice seedlings, submerged round stones, and slow ripples create calm graphic patterns around the central flight path. Rectangular field boundaries remain parallel to the image edges, producing a flat, map-like composition. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with clean geometric shapes and sculpted surface detail. Golden-hour illumination turns the water into luminous bands of cyan, pink, peach, violet, and warm gold while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>80473</code></summary>

```text
A low wide view beside a rural railway crossing at the edge of the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, stands full-body in the lower-left third behind a lowered black-and-amber crossing gate, feet braced as both hands hold a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies high in the upper-right third, clearly separated from the clouds, with its taut cream string crossing the open sky to her hands. Parallel rails remain visible through the center and curve into rice fields and cedar houses. Blue hydrangeas and wet grass frame the bottom corners. Violet storm clouds advance from the upper-left while warm light survives at the right edge. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>91831</code></summary>

```text
An immense upward-looking aerial view inside a corridor of violet-blue storm clouds above the same Japanese mountain valley. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails climbs diagonally from the lower-middle toward a narrow amber opening in the upper-right, its complete diamond silhouette isolated within a clear band of sky. Fine rain slants across the frame and the cream string descends from the kite through the bottom edge toward tiny geometric rice terraces far below. The surrounding cloud walls curl inward as immense sculpted masses, creating a grand tunnel of violet, cobalt, pale cyan, and warm gold light. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>104729</code></summary>

```text
A calm medium-wide view on a weathered mountaintop shrine terrace at luminous amber sunset, overlooking the same Japanese mountain village. A vermilion torii forms a strong rectangular frame around Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who stands full-body slightly left of center, shoulders relaxed as she looks upward and holds a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails descends through the open upper-middle of the torii, connected directly to her hands by a gently taut cream string. Far below, reflective rice terraces, tiny cedar roofs, and a thin railway settle into blue-green shadow. A bronze shrine bell hangs near one upper corner as immense amber-edged clouds open beyond the ridge. The mood is quiet, powerful, and resolved. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, filled with luminous multicolored clouds in cyan, cobalt, pink, magenta, violet, peach, coral, and warm gold. Brilliant low sunlight creates iridescent cloud edges, radiant atmospheric depth, clean rim light, and long warm highlights, while the unmarked white kite remains crisp white.
```

</details>

### Skythread_V3_Krea_Lora04_PromptV4

Manifest: [`manifests/krea/Skythread_V3_Krea_Lora04_PromptV4/manifest.json`](manifests/krea/Skythread_V3_Krea_Lora04_PromptV4/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>31017</code></summary>

```text
A child-eye-level medium-wide view across the wet wooden veranda of a cedar farmhouse in a Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, kneels right-of-center facing toward the open right side of the veranda, her hands tightening the final knot on a single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails. It leans upright behind her in the lower-left third with its full diamond silhouette visible; the spool rests beside her left knee. A pale doorway curtain, a glass wind chime, wet leaves, and irregular hand-shaped rice terraces curving around the distant mountains create restrained depth. The right side remains open for her next movement. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>44291</code></summary>

```text
A high three-quarter medium-wide view looking down a narrow sunlit lane in the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs naturally from the lower-left toward the lower-right while holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails behind her in the upper-left third above the tiled roofs, and its taut cream string forms a clean backward diagonal to the spool in her hands. Her entire body is clearly separated from the background. White laundry, indigo towels, persimmon leaves, wooden shop curtains, and receding telephone wires guide the lane toward green mountains beneath tall summer clouds. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>58733</code></summary>

```text
A low lateral medium-wide view beside luminous rice terraces in the same Japanese mountain village after rain. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails left-of-center at chest height behind Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who runs toward the right on the same depth plane in a balanced stride, holding a small dark-wood spool as the cream string connects her hands to the airborne diamond. Dry grass and sparse blue and yellow wildflowers fill the lower foreground. Lush green paddies follow the mountain contours in broad hand-built curves, with irregular grassy banks, varied widths, and gentle asymmetry leading toward dark cedar roofs and blue hills. Open air clearly separates both subjects from the landscape. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>69109</code></summary>

```text
The camera points perpendicular to the ground in an exact straight-down aerial view. A narrow blue-green irrigation canal meanders from the top edge to the bottom edge through rice paddies shaped by the natural terrain. Their hand-built grassy banks bend in loose asymmetrical curves, with varied field sizes and softly uneven margins. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies above the center of the canal, its full diamond silhouette crisp against the dark water while its cream string continues through the bottom edge. Neat rows of rice seedlings, submerged round stones, and slow ripples create calm flowing patterns around the central flight path. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with flowing organic shapes and sculpted surface detail. Water mirrors brilliant pink and purple golden-hour clouds, crossed by luminous bands of reflected sunlight in warm gold, magenta, and lavender. The unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>80473</code></summary>

```text
A low wide view beside a rural railway crossing at the edge of the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, moves cautiously toward the right in the lower-right third behind a lowered black-and-amber crossing gate, both hands holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails high behind her in the upper-left third, clearly separated from the clouds, with its taut cream string crossing the open sky to her hands. Parallel rails remain visible through the center and curve into rice fields and cedar houses. Blue hydrangeas and wet grass frame the bottom corners. Violet storm clouds advance from the upper-left while warm light survives at the right edge. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>91831</code></summary>

```text
An immense upward-looking aerial view inside a corridor of violet-blue storm clouds above the same Japanese mountain valley. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails climbs diagonally through the lower-middle, pulled from beyond the bottom-right edge so its two white tails stream backward toward the lower-left. Fine rain slants across the frame and the cream string descends toward irregular curved rice terraces far below. Immense bright pink and purple cloud walls curl inward around a radiant opening as powerful golden sunbeams fan through the corridor. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>104729</code></summary>

```text
A calm medium-wide view on a weathered mountaintop shrine terrace at luminous amber sunset, overlooking the same Japanese mountain village. A vermilion torii forms a strong rectangular frame around Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who walks slowly toward the right beneath it, shoulders relaxed as she looks back and holds a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails descends behind her through the upper-left opening of the torii, connected directly to her hands by a gently taut cream string. Far below, irregular curved rice terraces, tiny cedar roofs, and a thin railway settle into blue-green shadow. A bronze shrine bell hangs near one upper corner as immense amber-edged clouds open beyond the ridge. The mood is quiet, powerful, and resolved. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

### Skythread_V3_Krea_Lora04_PromptV5

Manifest: [`manifests/krea/Skythread_V3_Krea_Lora04_PromptV5/manifest.json`](manifests/krea/Skythread_V3_Krea_Lora04_PromptV5/manifest.json)

<details>
<summary><code>01_veranda_start</code> - seed <code>31017</code></summary>

```text
A child-eye-level medium-wide view across the wet wooden veranda of a cedar farmhouse in a Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, kneels right-of-center facing toward the open right side of the veranda, testing a small dark-wood spool in both hands. Behind her in the lower-left third rests a single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails, leaning upright with its full diamond silhouette visible and its cream string connected directly to her spool. A pale doorway curtain, a glass wind chime, wet leaves, and irregular hand-shaped rice terraces curving around the distant mountains create restrained depth. The right side remains open for her next movement. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>02_village_start</code> - seed <code>44291</code></summary>

```text
A high three-quarter medium-wide view looking down a narrow sunlit lane in the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, runs naturally from the lower-left toward the lower-right while holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails behind her in the upper-left third above the tiled roofs, and its taut cream string forms a clean backward diagonal to the spool in her hands. Her entire body is clearly separated from the background. White laundry, indigo towels, persimmon leaves, wooden shop curtains, and receding telephone wires guide the lane toward green mountains beneath tall summer clouds. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>03_rice_start</code> - seed <code>58733</code></summary>

```text
A low lateral medium-wide view beside luminous rice terraces in the same Japanese mountain village after rain. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails left-of-center at chest height behind Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who runs toward the right on the same depth plane in a balanced stride, holding a small dark-wood spool as the cream string connects her hands to the airborne diamond. Dry grass and sparse blue and yellow wildflowers fill the lower foreground. Lush green paddies follow the mountain contours in broad hand-built curves, with irregular grassy banks, varied widths, and gentle asymmetry leading toward dark cedar roofs and blue hills. Open air clearly separates both subjects from the landscape. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>04_canal_start</code> - seed <code>69109</code></summary>

```text
The camera points perpendicular to the ground in an exact straight-down aerial view. A narrow blue-green irrigation canal meanders from the top edge to the bottom edge through rice paddies shaped by the natural terrain. Their hand-built grassy banks bend in loose asymmetrical curves, with varied field sizes and softly uneven margins. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails flies above the center of the canal, its full diamond silhouette crisp against the dark water while its cream string continues through the bottom edge. Neat rows of rice seedlings, submerged round stones, and slow ripples create calm flowing patterns around the central flight path. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with flowing organic shapes and sculpted surface detail. Water mirrors brilliant pink and purple golden-hour clouds, crossed by luminous bands of reflected sunlight in warm gold, magenta, and lavender. The unmarked white kite remains crisp white.
```

</details>

<details>
<summary><code>05_train_start</code> - seed <code>80473</code></summary>

```text
A low wide view beside a rural railway crossing at the edge of the same Japanese mountain village after rain. Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, moves cautiously toward the right in the lower-right third behind a lowered black-and-amber crossing gate, both hands holding a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails trails high behind her in the upper-left third, clearly separated from the clouds, with its taut cream string crossing the open sky to her hands. Parallel rails remain visible through the center and curve into rice fields and cedar houses. Blue hydrangeas and wet grass frame the bottom corners. Violet storm clouds advance from the upper-left while warm light survives at the right edge. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>06_cloud_start</code> - seed <code>91831</code></summary>

```text
An immense upward-looking aerial view inside a corridor of violet-blue storm clouds above the same Japanese mountain valley. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails climbs diagonally through the lower-middle, pulled from beyond the bottom-right edge so its two white tails stream backward toward the lower-left. Fine rain slants across the frame and the cream string descends toward irregular curved rice terraces far below. Immense bright pink and purple cloud walls curl inward around a radiant opening as powerful golden sunbeams fan through the corridor. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

<details>
<summary><code>07_shrine_start</code> - seed <code>104729</code></summary>

```text
A calm medium-wide view on a weathered mountaintop shrine terrace at luminous amber sunset, overlooking the same Japanese mountain village. A vermilion torii forms a strong rectangular frame around Hana, a single eleven-year-old East Asian girl with a chin-length black bob and warm dark-brown eyes, wearing a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes, who walks slowly toward the right beneath it, shoulders relaxed as she looks back and holds a small dark-wood spool. A single plain white diamond kite the length of her torso, its unmarked white paper stretched over a simple bamboo cross and finished with two narrow white ribbon tails descends behind her through the upper-left opening of the torii, connected directly to her hands by a gently taut cream string. Far below, irregular curved rice terraces, tiny cedar roofs, and a thin railway settle into blue-green shadow. A bronze shrine bell hangs near one upper corner as immense amber-edged clouds open beyond the ridge. The mood is quiet, powerful, and resolved. The image is a polished vertical HoloSomnia-style cel-shaded anime illustration with sculpted forms and deep layered space. A vast bright golden-hour sky soars above the landscape, dominated by brilliant pink and purple clouds with touches of cyan, peach, and cobalt. Clearly visible shafts of warm sunlight stream between the clouds, strike their luminous pink and violet faces, and reflect across wet ground and water as radiant gold, magenta, and lavender highlights. The unmarked white kite remains crisp white against the saturated sky.
```

</details>

## Complete H3 prompt archive

All retained H3 prompt iterations are reproduced below. A seed is shown where that exact prompt was used by a selected final render; exploratory prompts without a selected output are labeled accordingly rather than inventing a seed.

<details>
<summary><code>01_cabin_porch.txt</code> - final render seed `88143`</summary>

Source: [`prompts/h3/01_cabin_porch.txt`](prompts/h3/01_cabin_porch.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the empty cedar cabin porch, mountain-lake landscape, golden-hour illumination, HoloSomnia cel-shaded rendering, camera geometry, and rightward exit path. Place Hana and the kite into this environment without transferring wood, flowers, clouds, or landscape materials into their bodies or clothing. Keep all three reference roles separate and create no additional people, kites, strings, tails, or spools.

integrated_multimodal_description: One uninterrupted ten-second vertical shot. At the first frame Hana is already kneeling left-of-center on the broad porch boards, facing screen-right and holding the plain white kite upright in front of her. From zero to three seconds, she stabilizes the kite with her left hand and carefully straightens its bamboo cross and two separate white ribbon tails with her right hand; the kite stays one coherent rigid diamond. From three to six seconds, she reaches to the single dark-wood spool beside her knee, draws out the thin cream string, connects its free end to the small bridle point at the center of the kite, and gives the string one gentle test pull so the connection becomes clearly taut. Her fingers move deliberately and the kite remains fully visible rather than blocking her face. From six to ten seconds, Hana rises smoothly, turns toward screen-right, and breaks into a light run along the porch and down the shallow right-hand steps. She carries the spool in her right hand. The kite starts behind her at screen-left, skims lightly over the wooden boards, then catches the breeze and lifts just above the porch while continuing to trail behind her. The cream string always forms one clean backward diagonal from her hand to the kite, and both white tails stream separately toward screen-left. The camera begins as a child-height medium-wide and performs one smooth dolly and pan toward screen-right, keeping Hana, her hands, the spool connection, and the trailing kite readable through the entire action. The cabin wind chime sways, wildflowers bend gently, and brilliant golden rays pass through soaring pink and purple clouds and reflect across the wet boards and distant lake. Preserve Hana's exact face, wardrobe, proportions, the kite's plain-white construction, and consistent rightward screen direction. Continuous coherent motion with no cuts, jumps, teleports, morphing, duplicate subjects, extra limbs, sudden zooms, frozen poses, or camera shake.

overall_soundscape: quiet mountain wind, soft kite-paper and ribbon flutter, a delicate glass wind chime, small handling sounds from wood and string, canvas shoes on damp porch boards, distant birds and lake water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>02_mountain_path.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/02_mountain_path.txt`](prompts/h3/02_mountain_path.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the mountain path, cabin landscape, golden-hour illumination, HoloSomnia cel-shaded rendering, and route geometry. Keep the three reference roles separate without transferring landscape materials or colors into Hana or the kite.

integrated_multimodal_description: One uninterrupted six-second vertical shot. Hana enters left-of-center already running toward screen-right along the broad curving mountain path, carrying the spool in her right hand. The plain white kite trails behind her at screen-left, hovering around shoulder height with one taut backward diagonal string; its two white tails stream independently and never merge. Use a child-height 35mm-equivalent camera on a smooth stabilized lateral dolly from her left-rear quarter, matching her speed while gently panning through the bend so the horizon remains level and the movement direction stays clear. Keep Hana full-body and let the path lead ahead of her rather than crowding the frame. Background motion is subtle: grasses and sparse wildflowers lean in the breeze, the lake glints softly, distant pine branches shift slightly, and pink-purple clouds evolve almost imperceptibly while golden rays remain stable. Preserve exact identity, wardrobe, kite construction, HoloSomnia palette, and rightward screen direction. No cuts, jumps, teleports, morphing, duplicates, sudden zooms, frozen poses, or camera shake.

overall_soundscape: light running footsteps on packed earth, mountain breeze, soft ribbon and kite-paper flutter, distant birds and lake water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>02_mountain_path_v2.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/02_mountain_path_v2.txt`](prompts/h3/02_mountain_path_v2.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the curving mountain path, cabin landscape, golden-hour illumination, HoloSomnia cel-shaded rendering, and route geometry. Keep the three reference roles separate without transferring landscape materials or colors into Hana or the kite.

integrated_multimodal_description: One uninterrupted eight-second vertical performance shot. Hana begins left-of-center moving toward screen-right along the broad curving path. From zero to two and a half seconds she runs with fluid childlike biomechanics: her weight shifts naturally from foot to foot, knees flex, shoulders counter-rotate, her free left arm swings, and the spool-bearing right hand responds to the changing string tension. The white kite initially trails behind her at screen-left around shoulder height. From two and a half to four seconds she takes two light joyful skipping steps with a small buoyant rise and an asymmetric landing, then transitions smoothly back to running. From four to five and a half seconds she slows to a brief natural stop on the bend, plants one foot ahead of the other, tilts her chin upward, and looks directly toward the kite with a delighted attentive expression. During this pause a stronger gust lifts the kite rapidly but smoothly into the high upper-left sky. The single cream string remains visibly and continuously connected from the kite to the dark-wood spool in her right hand, becoming taut as the kite rises; its two white tails stream independently in the wind. From five and a half to eight seconds Hana responds to the pull with a soft lean, takes several quick lively steps toward screen-right, and resumes an easy run while still glancing upward once. The kite stays high behind her and never crosses ahead.

Use a stabilized child-height camera beginning as a medium-full 50mm-equivalent tracking view from Hana's left-front quarter. As she moves, perform one continuous controlled dolly backward combined with a gradual optical zoom-out toward 28mm and a subtle crane upward, ending in a wider landscape composition that includes Hana, the full taut string, and the high kite. Keep the horizon level, maintain natural parallax, and lead her movement with open space at screen-right. Background motion is restrained: grasses and wildflowers sway, pine branches move softly, the lake glints, and pink-purple cloud faces drift almost imperceptibly around steady golden rays. Preserve exact identity, wardrobe, kite construction, HoloSomnia style, and rightward screen direction. Continuous coherent motion with no cuts, jumps, teleports, morphing, duplicates, sudden camera movement, frozen posing, foot sliding, or camera shake.

overall_soundscape: varied running and skipping footfalls on packed earth, a brief shoe scuff as she stops, mountain breeze rising into one stronger gust, soft kite-paper and ribbon flutter, distant birds and lake water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>02_mountain_path_v3_proposed.txt</code> - final render seed `88402`</summary>

Source: [`prompts/h3/02_mountain_path_v3_proposed.txt`](prompts/h3/02_mountain_path_v3_proposed.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the curving mountain path, cabin landscape, golden-hour illumination, HoloSomnia cel-shaded rendering, and route geometry. Keep the three reference roles separate without transferring landscape materials or colors into Hana or the kite.

integrated_multimodal_description: One uninterrupted eight-second vertical performance shot filled with joyful forward energy. Hana begins left-of-center already running toward screen-right along the broad curving path. On the very first frame, a fresh gust catches the plain white kite and it immediately begins rising from behind her left shoulder toward the high upper-left sky. The single cream string is already taut and remains a clearly visible continuous straight line from the kite directly to the dark-wood spool secured in Hana's right hand. The connection never breaks, loops, tangles, or becomes slack.

From zero to one and a quarter seconds, Hana continues running while she notices the sudden upward pull. Her eyes widen, eyebrows lift, chin turns toward the kite, and her mouth forms a small delighted round “ooh” expression. Her body keeps traveling forward; she only shortens one step in a brief half-beat of surprise and never becomes stationary. The kite climbs continuously and reaches the upper-left third by the end of this beat, with both white tails streaming independently behind it.

From one and a quarter to two and a half seconds, she looks up at the rising kite and takes two buoyant skipping steps while still moving screen-right. Each skip has a distinct push-off, light airborne moment, asymmetric landing, natural knee flexion, and active counter-swing from her free left arm. The spool hand follows the taut string tension without losing its grip. Her “ooh” expression blossoms into a broad excited smile.

From two and a half to three and a quarter seconds, Hana performs one joyful forward-and-upward jump while continuing along the path. Both feet leave the ground clearly, her knees bend beneath her, her free arm lifts with excitement, and her torso rises naturally. She keeps the spool secure in her right hand and keeps looking toward the kite. She lands softly on one foot and immediately rolls into the next running stride without pausing.

From three and a quarter to eight seconds, Hana accelerates into a lively, increasingly confident run toward screen-right. Her stride lengthens, cadence quickens, shoulders and hips counter-rotate naturally, her free arm pumps, her blouse and culottes respond to motion, and her footfalls vary organically. She glances upward twice with visible delight while maintaining forward momentum. The kite continues climbing into the high upper-left and then remains very high behind her, pulling strongly on the straight connected string as its two tails stream in the wind. Her energy grows through the final frame rather than settling down.

Use a stabilized child-height camera beginning as a medium-full 45mm-equivalent tracking view from Hana's left-front quarter. Begin pulling backward and widening immediately on frame one. Perform one continuous smooth dolly backward, gradual optical zoom-out toward 24mm, and subtle crane upward so the composition expands in direct response to the kite's ascent. By the middle of the shot, Hana occupies the lower-right half and the high kite occupies the upper-left, with the complete taut string visible between them. End in a broad energetic landscape view while still tracking her forward motion. Keep the horizon level, preserve natural parallax, and leave open space ahead at screen-right. Background motion remains restrained: grasses and wildflowers sway, pine branches move softly, the lake glints, and pink-purple clouds drift slowly around stable golden rays. Preserve exact identity, wardrobe, kite construction, HoloSomnia style, and rightward screen direction. Continuous coherent motion with no cuts, jumps in time, teleports, morphing, duplicate subjects, foot sliding, stiff repeated run cycles, stationary hold, sudden camera move, or camera shake.

overall_soundscape: lively varied running and skipping footfalls on packed earth, one soft two-foot airborne hush and landing scuff, mountain breeze swelling immediately into a sustained gust, bright kite-paper and ribbon flutter, distant birds and lake water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>02_mountain_path_v4_uphill_crane.txt</code> - final render seed `92731`</summary>

Source: [`prompts/h3/02_mountain_path_v4_uphill_crane.txt`](prompts/h3/02_mountain_path_v4_uphill_crane.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a pale bamboo cross, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the HoloSomnia mountain path scene: the path begins very close at bottom-center, winds away through a broad right bend and left bend, and climbs toward the wooden cabin in the upper-left middle distance. Preserve the cabin, fences, organic path geometry, flowers, grasses, mountain valley, golden lake, radiant pink-purple clouds, and warm sunlight from frame right.

integrated_multimodal_description: One uninterrupted 6.6-second vertical shot with one continuous action and one continuous camera move.

OPENING COMPOSITION: begin on the exact empty foreground path from <Picture 3>, viewed from low standing height. The near stones and grasses frame the bottom edge, the S-shaped path leads deep toward the cabin, and the bright valley remains visible beyond. Hana is not waiting in the scene. During the first quarter-second, Hana bursts into view from below the bottom-center edge already running rapidly away from the camera. We see her from behind. She is centered precisely on the path and moving uphill into the picture, never toward the camera.

ACTION: Hana runs energetically away along the actual painted path, following every visible bend toward the cabin. She begins large in the near foreground, rounds the broad rightward curve, crosses the middle section, then follows the leftward turn toward the cabin. Her scale decreases continuously and naturally as she covers real ground. Her running has youthful asymmetry and forward urgency rather than a repeated game-character loop: stride lengths vary, planted feet grip the path without sliding, her free left arm drives naturally, her shoulders counter-rotate, and her hat brim, blouse, and culottes respond to speed and wind. On the first gentle bend she adds one buoyant skipping stride without stopping, then accelerates smoothly. She remains back-facing or in brief three-quarter-back profile and never turns to address the camera.

Hana holds the small dark-wood spool securely in her right hand from the instant she enters. The single plain white kite is already airborne and trails high behind her in the wind; it does not begin on the ground and is never held in her hand. Keep the kite well separated from Hana, with one long fine cream string visibly and continuously connected from the spool to the kite. The line stays taut under wind pressure. The kite drifts high across the open upper-right sky while Hana runs toward the upper-left cabin, preserving a strong diagonal span across the frame. Its two white tails stream separately and coherently. The kite never dives, overtakes Hana, detaches, or becomes enormous in the foreground.

CAMERA: perform one smooth stabilized vertical crane upward from the opening frame through the end. The camera rises decisively above the foreground path while tilting downward just enough to keep Hana and the winding route visible. Do not chase beside her, orbit her, or reverse direction. As the camera gains height, the near fences and flowers slide downward in strong painted parallax, the entire S-curve opens beneath us, and the cabin and broad valley become increasingly prominent. The ascent naturally converts the shot from a low wide rear view into a majestic high wide landscape view. Keep Hana moving deeper and becoming smaller; do not zoom in to preserve her size.

ENDING: in the final second Hana is a small, fast-moving figure approaching the cabin-side bend in the upper-left middle distance. She continues running with energy through the final frame while the camera completes its upward reveal. The kite remains high behind her with the complete taut line readable. End in motion on the expansive path, cabin, lake, mountains, and radiant sky; no freeze, pose, or cut.

ENVIRONMENTAL MOTION: restrained and coherent. Foreground grass and blue flowers bow in the same breeze, pine tips shift subtly, the distant lake glints, and pink-purple clouds drift slowly around stable golden rays. Preserve crisp inked contours, flat two-tone cel shading, matte gouache texture, consistent identity and scale, and clean separation between Hana, kite, line, and landscape.

Hard constraints: exactly one Hana and one kite; Hana enters from bottom-center and runs away toward the cabin; no running toward camera; no side-to-side screen crossing; no centered standing start; no relaunch; no grounded kite; no detached, slack, looping, or broken line; no duplicate subjects; no stiff repeated gait; no foot sliding; no teleport; no morphing; no camera orbit; no sudden zoom; no reverse; no cut; no subtitles; no logo; no watermark.

overall_soundscape: Rapid varied footfalls receding up packed earth, one light skipping landing, steady mountain wind, taut string hum, distant white kite-paper and ribbon flutter, grasses, pine needles, birds, and faint lake water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>03_rice_fields.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/03_rice_fields.txt`](prompts/h3/03_rice_fields.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the organic rice terraces, raised footpath, mountain valley, golden-hour illumination, and polished HoloSomnia cel-shaded rendering. Keep the reference roles separate without transferring landscape textures into Hana or the kite.

integrated_multimodal_description: One uninterrupted seven-second vertical lateral tracking shot. Hana runs naturally toward screen-right along the dry raised path, centered slightly right, with a balanced age-appropriate stride and the dark-wood spool steady in her right hand. The white kite remains behind her on screen-left at roughly chest height, rising gently with one breeze and settling without overtaking her. One cream string stays continuously connected; the two white ribbon tails lag with coherent drag. The camera uses a low 50mm-equivalent side profile on a stabilized dolly, traveling parallel to the path with a very slow boom upward during the final third to reveal more of the curved terraces. Maintain clean foreground-to-background parallax and a level horizon. The hand-built paddies retain broad flowing curves, irregular banks, and varied widths. Background motion stays restrained: rice blades ripple in small waves, irrigation water reflects gold and lavender, distant trees move faintly, and luminous pink-purple clouds drift slowly around steady sunbeams. Preserve exact identity, clothing, prop geometry, scale, style, and rightward direction. No cuts, jumps, teleports, morphing, duplicates, warped limbs, frozen posing, or camera shake.

overall_soundscape: rhythmic footsteps on dry earth, rice leaves rustling, soft kite flutter, insects, breeze and distant irrigation water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>03_rice_fields_v2.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/03_rice_fields_v2.txt`](prompts/h3/03_rice_fields_v2.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the organic rice terraces, raised path, mountain valley, golden-hour illumination, and polished HoloSomnia cel-shaded rendering. Keep character, prop, and environment materials separate and preserve the broad rightward route.

integrated_multimodal_description: One uninterrupted six-second vertical continuation of Scene 2. Hana is already running steadily and confidently toward screen-right along the dry raised path. Her earlier surprise has become sustained exhilaration: she wears a bright open smile, keeps an energetic forward lean, and occasionally flicks her eyes upward without breaking stride. Her gait is fluid and purposeful, with varied footfalls, natural knee flexion, active free-arm drive, counter-rotation through shoulders and hips, and responsive movement in her blouse and culottes. She holds the dark-wood spool securely in her right hand.

The single plain white kite begins very high behind Hana in the upper-left sky and remains high throughout the shot. It climbs slightly farther on one steady gust, then glides smoothly above the terraces without dipping toward the ground or overtaking her. One thin cream string stays taut, straight, clearly visible, and continuously connected from the kite directly to the spool in her hand. The two white ribbon tails stream separately and coherently in the wind.

Use a competent stabilized wide-shot reveal. Begin with a 35mm-equivalent medium-wide tracking view from Hana's left-front quarter, already moving backward at her speed. Immediately perform one continuous smooth dolly backward combined with a gradual optical zoom-out toward approximately 20mm and a gentle crane upward. The camera movement expands rather than accelerates: Hana transitions from a prominent full-body figure in the lower-right third to a smaller but still readable figure within an immense landscape, while the high kite remains isolated in the upper-left and the complete connecting string stays visible. Let the foreground path, irregular grassy banks, curved terrace walls, and reflective irrigation channels sweep broadly across the lower frame through strong controlled parallax. The landscape should appear to unfold in front of the viewer as the camera recedes, revealing the luminous lake, cedar farmhouses, pine ridges, and layered mountains. Keep the horizon level and the rightward screen direction unambiguous.

Background animation is subtle and physically coherent: rice blades ripple in small waves, wildflowers and grasses lean softly, irrigation water carries slow gold and lavender reflections, distant pine branches shift faintly, and pink-purple clouds drift almost imperceptibly around stable golden sunbeams. Preserve Hana's exact identity and wardrobe, the kite's plain-white geometry, the HoloSomnia palette, and consistent scale relationships. Continuous coherent movement with no cuts, jumps in time, teleports, morphing, duplicate subjects, foot sliding, stiff repeated run cycles, sudden zoom, horizon roll, frozen poses, or camera shake.

overall_soundscape: steady varied running footfalls on dry earth, sustained mountain wind, high kite-paper and ribbon flutter, rice leaves, insects, and distant irrigation water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>03_rice_fields_v3_continuity.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/03_rice_fields_v3_continuity.txt`](prompts/h3/03_rice_fields_v3_continuity.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the irregular rice terraces, narrow raised earth path, reflective water, mountain valley, radiant golden-hour sky, and polished HoloSomnia hand-painted cel-animation style. Preserve the organic curved geography and luminous pink, lavender, and gold cloud reflections.

integrated_multimodal_description: One uninterrupted six-second vertical continuation of Scene 2, with one action and one camera move. Scene 2 has already established a great distance between Hana and the kite: the kite is already flying extremely high, connected to Hana by a long taut line. Preserve that state immediately. Do not launch the kite again.

FIRST FRAME AND COMPOSITION: begin already in a natural high oblique aerial view, almost top-down, with the camera roughly sixty-five degrees downward over the rice terraces. This is a wide landscape shot from the first frame, never a medium shot and never a close view. The curving raised path crosses the lower half of frame. The single white kite is already small and high in the upper-left sky, well separated from the ground. Its full long cream string angles cleanly down across the open frame toward the path. Hana is initially outside the left edge; no character waits or poses in frame.

ACTION: within the first half-second, Hana bursts into frame from the left already running fast. She is a small full-body figure, about one-sixth of the frame height. Her right hand firmly holds the dark-wood spool, and the same unbroken cream string remains visibly attached from the spool all the way to the high kite. She races naturally along the curved raised path toward the lower-right, following its bends with agile, youthful momentum. Use a lively irregular run rather than a repeated game-character cycle: long and short strides alternate, her free arm drives naturally, her torso leans into the bends, her hat brim and clothes answer the wind, and each planted foot grips the earth without sliding. She does not slow down, stop, pose, look at the camera, or lift the kite by hand. The kite never descends. It remains high above and behind her, pulling steadily in the wind while its two ribbon tails stream coherently.

CAMERA: perform one smooth stabilized aerial tracking pullback. The camera glides diagonally with Hana's route while continuously rising and widening, keeping the curved path and immense valley dominant. It follows her motion but gains altitude faster than it gains ground, so Hana becomes progressively smaller as terraces, irrigation mirrors, farm roofs, and layered mountains sweep open beneath us. Maintain the same left-to-right travel direction and a stable horizon. In the final second, let the camera lag slightly as Hana runs quickly down the path and exits the lower-right edge; the high kite and taut line follow her direction out of the composition. End on the expanding landscape with no freeze and no cut.

MOTION DESIGN: camera motion and Hana's single fast path-crossing are the primary movement. Add only subtle coherent environmental life: gentle waves pass through rice blades, small grasses lean in the same wind, water reflections shimmer slowly, and bright pink-purple clouds hold stable golden light rays. Use controlled painted multiplane parallax: near terrace banks sweep fastest, middle paddies drift moderately, and the mountain layers move slowly. Preserve crisp stable linework, flat cel shading, matte gouache texture, consistent anatomy, consistent scale, and clean object separation.

Never show the kite near Hana or near the ground. Never begin with Hana centered, large, standing, or jogging toward camera. No second girl, no second kite, no detached string, no broken or looping line, no hand-held kite, no relaunch, no stiff repeated run cycle, no foot sliding, no teleport, no morphing, no camera orbit, no sudden digital zoom, no close-up, no reverse direction, no cut, no subtitles, no logos, no watermark.

overall_soundscape: Fast varied footfalls on dry earth passing left to right, steady high mountain wind, distant taut kite-paper and ribbon flutter, soft rice hiss, insects, and quiet irrigation water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>03_rice_fields_v4_scene2_handoff.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/03_rice_fields_v4_scene2_handoff.txt`](prompts/h3/03_rice_fields_v4_scene2_handoff.txt)

```text
<Picture 1> is the authoritative continuity reference from the end of Scene 2. Preserve the same single Hana, the same single plain white diamond kite, the same dark-wood spool, and especially their established spatial relationship: Hana and the kite are separated by a great distance, the kite is already small and very high, and one long taut cream line visibly connects it to the spool. Transfer those identities and that long-distance relationship only. Do not reuse Picture 1's path, fence, camera angle, or background.

<Picture 2> is the exclusive authority for Scene 3's irregular rice terraces, winding raised path, reflective paddies, mountain valley, radiant golden-hour sky, and polished HoloSomnia hand-painted cel-animation style. Preserve the organic curved geography and luminous pink, lavender, and gold cloud reflections.

integrated_multimodal_description: One uninterrupted six-second vertical continuation. One primary action and one primary camera behavior. The kite was launched in Scene 2 and is already flying high; there is no launch, pickup, or adjustment in this shot.

EXACT OPENING: the first frame is already a very wide high-oblique aerial view, pitched about sixty-five degrees downward over the winding rice-field path. The immense landscape dominates immediately. The path crosses diagonally from the left edge toward the lower-right. Hana is not centered and never appears large: at time zero she is still offscreen, with at most the leading edge of one small running foot or shoulder just crossing the far left boundary. The single white kite is already a small distant diamond in the upper-left, no larger than Hana's hat, far above and far behind her route. A long fine cream line spans the open composition from that small kite to the left frame edge. Do not place a large kite in the foreground.

ACTION: during the first half-second, Hana bursts fully into frame from the left already at a fast run. She remains a small full-body figure, approximately one-eighth of frame height. Her right hand firmly holds the dark-wood spool and the same unbroken cream line remains visibly attached from spool to the distant kite. She races along the raised path toward the lower-right, taking its bends with energetic youthful momentum. Her running is responsive rather than cyclic: alternating stride lengths, secure planted feet, active free-arm drive, slight torso lean through curves, and wind response in her hat brim, blouse, and culottes. She never stops, poses, jogs toward the camera, or looks at the viewer. The kite never approaches her and never descends. It stays small and very high behind her, tugging steadily, with its two ribbon tails streaming cleanly.

CAMERA: one smooth stabilized drone move from beginning to end. Track diagonally along the route while rising and pulling farther back at a constant confident pace. Keep Hana readable but small, and reveal increasingly broad nested terraces, irrigation mirrors, farmhouse roofs, and layered mountains. The camera follows the geography rather than orbiting Hana. Near banks sweep through strong painted parallax, middle paddies drift more slowly, and distant ridges barely move. Maintain left-to-right screen direction and a stable horizon. During the final second, the camera deliberately lags while continuing to rise; Hana runs down the path and exits the lower-right edge at speed. The taut line follows her out while the small high kite remains momentarily visible near the upper-left. End on the moving golden landscape, not on a frozen pose.

ENVIRONMENTAL MOTION: subtle coherent wind only. Rice blades ripple in low waves, grasses and wildflowers lean together, irrigation reflections shimmer gently, and vivid pink-purple clouds retain stable golden shafts of sunlight. Preserve crisp stable inked contours, flat two-tone cel shading, matte gouache texture, consistent anatomy and wardrobe, clean object separation, and organic terrace curves.

Hard constraints: exactly one Hana and one kite. Kite small and distant from the first frame. Long taut string continuously connected to the spool. No foreground kite, no close or medium opening, no centered waiting character, no relaunch, no detached or looping string, no second subject, no stiff repeated run loop, no foot sliding, no teleport, no morphing, no camera orbit, no sudden zoom, no reverse direction, no cut, no subtitles, no logo, no watermark.

overall_soundscape: Fast varied footfalls passing left to right over dry earth, steady mountain wind, distant taut kite-paper and ribbon flutter, soft rice hiss, insects, and quiet irrigation water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>04_aerial_path.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/04_aerial_path.txt`](prompts/h3/04_aerial_path.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, proportions, wardrobe colors, and straw hat. Preserve one eleven-year-old East Asian girl with a chin-length black bob, cream collared blouse, loose indigo culottes, white socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white diamond kite with a simple pale bamboo cross, exactly two separate white ribbon tails, one cream string, and one dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the true bird's-eye mountain terrain, winding path, organic contours, lighting, palette, and HoloSomnia cel-shaded rendering. Keep character, prop, and terrain materials strictly separate.

integrated_multimodal_description: One uninterrupted six-second exact top-down aerial follow. The camera remains perpendicular to the ground with no horizon or roll. Hana appears as one clearly readable small figure on the pale path in the lower third and runs continuously upward and slightly toward screen-right along its first broad curve. Her red shoes, straw hat, cream blouse, and indigo culottes remain distinct at this scale. The single white kite follows behind her lower-left along the same route, separated from her silhouette and connected by one visible cream string; both tails stream backward toward the bottom-left. The drone floats forward at her average speed and makes one gentle altitude increase, revealing more of the winding trail while preserving the map-like geometry. Background motion is subtle: pine crowns stir, the narrow stream shimmers, small grass patches bend, and long violet shadows shift almost imperceptibly. Warm ridge light and reflected pink-purple color remain consistent. No cuts, perspective tilt, rapid rotation, zoom snap, duplicated figures, duplicated kites, morphing terrain, or frozen motion.

overall_soundscape: high open wind, faint footsteps far below, soft kite flutter, stream water and distant birds; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>05_train_crossing.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/05_train_crossing.txt`](prompts/h3/05_train_crossing.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the rural railway crossing, gate, track geometry, wet landscape, golden-hour lighting, and HoloSomnia rendering. Keep the references materially and spatially separate.

integrated_multimodal_description: One uninterrupted eight-second low wide shot with disciplined blocking. During the first two seconds Hana jogs from the lower-left toward screen-right and slows within the safe waiting area behind the lowered crossing gate. The white kite stays behind her in the upper-left, tugging gently while the single string remains connected to the spool. From two to three seconds she plants her feet and steadies the spool with both hands as the crossing bell sounds. From three to seven seconds one compact amber rural train emerges from the distant curve and rolls forward along the existing rails through the middle of frame, always behind the gate and clearly separated from Hana and the kite. The passing airflow stirs her blouse, hydrangeas, and the two kite tails without changing the kite's position or shape. During the final second the train clears the near edge and Hana looks right, ready to continue. Use a low 40mm-equivalent camera locked to a sturdy tripod with only a very restrained slow push-in; keep verticals stable and avoid panning after the train enters. Background motion is subtle apart from the train: puddles shimmer, grasses sway, signal lights blink steadily, and pink-purple clouds move slowly around fixed golden rays. Preserve exact identity, prop construction, style, and safe depth separation. No cuts, jumps, teleports, duplicate trains, duplicate people, duplicate kites, morphing rails, frozen posing, or camera shake.

overall_soundscape: crossing bell, approaching and passing rail clatter, light wind, hydrangea leaves, kite-paper flutter and soft shoe scuffs; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>06_soaring_skies.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/06_soaring_skies.txt`](prompts/h3/06_soaring_skies.txt)

```text
<Picture 1> is the exclusive authority for the kite. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, and one thin cream string. Use none of the gradient background or spool from this reference.

<Picture 2> is the exclusive authority for the soaring cloud corridor, distant mountain valley, golden-hour rays, multicolored palette, and polished HoloSomnia cel-shaded rendering. Keep the white kite's material and shape separate from the cloud textures.

integrated_multimodal_description: One uninterrupted six-second soaring aerial chase. Begin with the white kite in the lower-middle, already moving diagonally toward the radiant upper-right opening. The unseen pull remains beyond the lower-right edge, so the single cream string angles down-right while both white ribbon tails trail independently toward the lower-left. The kite banks gently once into the airflow, flexes only slightly like real paper over a rigid frame, then levels and continues climbing without changing geometry, scale, or color. Use a smooth 28mm-equivalent chase camera positioned slightly below and behind the kite, advancing at matching speed with a slow controlled tilt upward and no roll. The cloud corridor stays monumental rather than racing past: pink and purple banks curl subtly, their luminous faces evolve slowly, distant valley haze shifts gently, and powerful golden rays shimmer without flicker. Maintain clear silhouette separation and serene forward momentum. No cuts, jumps, duplicated kites, extra strings or tails, morphing, sudden acceleration, frozen motion, or camera shake.

overall_soundscape: broad high-altitude wind, soft paper and ribbon flutter, distant fading thunder and open mountain air; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>06_soaring_skies_v2_continuity_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/06_soaring_skies_v2_continuity_720p.txt`](prompts/h3/06_soaring_skies_v2_continuity_720p.txt)

```text
<Picture 1> is the authoritative continuity frame from the approved preceding shot. Preserve exactly one Hana as a tiny figure beside the cabin, exactly one plain white diamond kite already high above her, the long nearly vertical cream line between them, the warm late-afternoon direction, and the same HoloSomnia painted-cel style. Use this reference only for the established subject state and opening handoff; do not retain its cabin, path, or hills after the camera rises into the clouds.

<Picture 2> is the exclusive authority for the monumental multicolored cloud corridor, distant mountain valley, radiant opening, pink-purple-gold palette, stable sunbeams, layered atmospheric depth, and polished HoloSomnia hand-painted cel-animation rendering.

integrated_multimodal_description: One uninterrupted 6.6-second vertical continuation with one subject action and one camera move. The kite has already been launched and is already very high. There is no relaunch, pickup, reset, or second kite.

OPENING HANDOFF: begin from a very high wide continuation of <Picture 1>. For the first half-second only, Hana remains a tiny readable figure near the bottom edge beside the cabin while the single small white kite is far above her near upper-middle. One long fine cream line remains continuously visible between them. The camera is already rising along the taut line. Do not begin with a large foreground kite or a close character view.

ASCENT: perform one smooth stabilized aerial crane and tilt upward, following the existing line from Hana toward the kite. The ground, cabin, and tiny Hana slide naturally downward and leave frame during the first second; the camera never cuts. The single kite continues climbing into the enormous cloud corridor from lower-middle toward the radiant upper-right opening. Keep it a modest distant diamond, roughly one-tenth of frame height, with stable warm-grey edges, pale cross spars, and exactly two narrow white ribbon tails. The cream line continues downward out of frame toward the unseen Hana. The kite makes one gentle bank with the wind, flexes only slightly like paper over a rigid frame, then levels and glides upward without changing construction.

CAMERA AND DEPTH: the camera travels upward slightly below and behind the kite at a calm confident pace, gradually widening as altitude increases. No orbit, roll, shake, racing push-in, or sudden zoom. Monumental violet cloud banks frame the outer edges; nearer painted cloud layers drift past with controlled parallax while distant pink, lavender, peach, and pale-cyan layers move slowly. Stable golden and rose light shafts open through the center and reflect through distant valley haze. The cloud opening should feel vast, bright, multicolored, and physically continuous rather than like a tunnel warp.

ENDING AND CONTINUITY: in the final two seconds the kite clears the densest cloud wall into serene warm open sky. Its climb eases into a shallow rightward glide, preparing the direction toward the ridge shrine. Keep the kite small in the upper-right third with the taut line trailing diagonally down-left beyond frame. End in sustained motion on luminous open air, leaving room below and left for the next shot to reveal Hana and the shrine. No freeze or cut inside the generation.

Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache and watercolor texture, luminous cobalt, violet, pink, cream, peach, and gold, clean silhouette separation, coherent scale, and subtle 2D multiplane parallax. No photorealism, 3D gloss, texture flicker, line wobble, duplicated kite, extra string, extra tails, detached line, enormous foreground kite, morphing geometry, teleport, or subtitles.

overall_soundscape: Broad high-altitude wind rising from the valley, soft distant kite-paper and twin-ribbon flutter, a fine taut-string hum, faint birds disappearing below, and open mountain air. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>06_soaring_skies_v3_simple_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/06_soaring_skies_v3_simple_720p.txt`](prompts/h3/06_soaring_skies_v3_simple_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background. Hana remains below and outside the visible frame during this sky-focused shot.

<Picture 2> is the exclusive authority for the kite and line. Preserve exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, pale bamboo cross spars, exactly two narrow white ribbon tails, and one thin cream string. Use none of the gradient background or spool.

<Picture 3> is the exclusive authority for the soaring multicolored cloud corridor, distant valley, golden-hour rays, pink-purple-cobalt-peach palette, atmospheric depth, and polished HoloSomnia hand-painted cel-animation style.

integrated_multimodal_description: One uninterrupted 6.6-second vertical aerial shot. The single plain white kite begins in the lower-middle already flying upward through the broad cloud corridor toward the radiant upper-right opening. Its cream string continues diagonally down-right beyond the frame toward unseen Hana, and its two white tails stream independently toward the lower-left.

The kite makes one gentle bank into the wind, flexes only slightly like paper over a rigid bamboo frame, then levels and continues a calm steady climb. Keep the kite coherent, crisp, and moderately small against the enormous sky. It never dives, stops, changes shape, grows enormous, duplicates, or loses its string.

Use one smooth stabilized chase camera slightly below and behind the kite, traveling at matching speed while tilting upward gently. No orbit, roll, shake, sudden zoom, or acceleration. Painted cloud banks drift slowly with controlled depth: nearer violet and cobalt edges move somewhat faster, middle pink and peach layers move gently, and the distant radiant opening remains stable. Golden, magenta, and lavender light shafts shimmer softly without flicker. Far below, the mountain valley and winding lake recede through blue haze.

End with the kite gliding serenely into the bright upper-right opening, still connected by the cream line extending out of frame. Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, luminous HoloSomnia color, clean silhouette separation, and subtle multiplane parallax. No photorealism, 3D gloss, line wobble, texture flicker, extra kite, extra tails, detached line, morphing, cut, subtitles, logo, or watermark.

overall_soundscape: Broad high-altitude wind, soft kite-paper and twin-ribbon flutter, a faint taut-string hum, distant birds, and open mountain air. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>06_soaring_skies_v4_fast_kite_720p.txt</code> - final render seed `94783`</summary>

Source: [`prompts/h3/06_soaring_skies_v4_fast_kite_720p.txt`](prompts/h3/06_soaring_skies_v4_fast_kite_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity and wardrobe. Preserve exactly one Hana if referenced by the model, but keep her entirely outside the visible frame during this sky-only shot. Use none of the studio background.

<Picture 2> is the exclusive authority for the single plain white kite and spool system. Preserve one rigid unmarked white paper diamond, one pale vertical bamboo spine, one gently curved horizontal bamboo spar, exactly two narrow white ribbon tails attached only at the lower point, one thin cream flight line, and one dark-wood spool. The flight line is connected to a bridle on the hidden back/underside of the kite slightly below the spar intersection. From the camera's view it must emerge from behind the lower half of the kite and continue downward toward the unseen spool. The line must never attach to the top point, upper edge, upper panel, or visible top face, and it must never cross over the front face of the white paper.

<Picture 3> is the exclusive authority for the immense multicolored cloud corridor, distant mountain valley, radiant upper-right opening, golden sunbeams, pink-purple-cobalt-peach palette, and polished HoloSomnia hand-painted cel-animation style.

integrated_multimodal_description: One uninterrupted 6.6-second fast vertical aerial action shot. The single white kite begins lower-middle already airborne, its hidden rear bridle pulling the cream line cleanly down-left behind it while the two white tails stream from the lower point. A powerful gust immediately snaps the line taut and launches the kite rapidly toward the radiant upper-right cloud opening.

The kite is lively and wind-driven. It flutters quickly from side to side, yaws through a sharp S-curve between two cloud banks, rolls briefly edge-on, completes one fast joyful clockwise twirl around its stable bridle axis, then levels and surges upward again. Its white paper flexes subtly over the rigid bamboo frame without folding or changing geometry. The two ribbon tails whip, curl, and stream independently in turbulent air. The flight line draws broad responsive arcs behind the kite while remaining continuously connected to the hidden underside bridle. The line never touches or appears on the upper face.

Use one fast stabilized chase camera that dives and rises with the kite from slightly below and behind. The camera accelerates through the corridor, banks with the S-turn, briefly swings to a side profile during the twirl, then pushes upward as the kite shoots through a brilliant shaft of light. Motion is energetic and cinematic but always readable: no handheld shake, vibration, random roll, teleport, or jump cut.

Cloud movement is equally alive. Near violet and cobalt cloud curls sweep past with strong painted parallax, pink and peach vapor spirals in the kite's wake, thin cloud ribbons peel around the tails, and stable gold, magenta, and lavender rays flash across the white paper as it turns. The distant valley drops rapidly through blue atmospheric depth.

End with the kite racing upward-right into bright open sky, still fluttering and pulling hard, with the cream line trailing behind from the hidden underside connection. Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, clean silhouette separation, exact kite construction, and luminous HoloSomnia color. Exactly one kite, one line, and two tails. No visible line on the top face, top-corner attachment, duplicate kite, extra string, extra tails, detached line, tangled bridle, morphing, 3D gloss, line wobble, subtitles, logo, or watermark.

overall_soundscape: Fast high-altitude wind, strong kite-paper snaps and flutter, two ribbons whipping through gusts, taut string singing under changing tension, rushing cloud air, and distant open valley ambience. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>07_mountain_shrine.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/07_mountain_shrine.txt`](prompts/h3/07_mountain_shrine.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background from this reference.

<Picture 2> is the exclusive authority for the kite, string, and spool. Preserve one plain unmarked white paper diamond kite with a fine warm-grey perimeter, a simple pale bamboo cross, exactly two separate narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background from this reference.

<Picture 3> is the exclusive authority for the mountaintop shrine, torii, terrace path, valley, golden-hour illumination, and polished HoloSomnia cel-shaded rendering. Keep all three reference roles separate and preserve the open rightward path.

integrated_multimodal_description: One uninterrupted nine-second calm closing shot. Hana enters from the lower-left and walks beneath the vermilion torii toward screen-right, breathing evenly after the run and holding the spool low in her right hand. The white kite glides behind her through the upper-left opening, connected by one gently taut backward string; its two separate tails drift left in the ridge breeze. During the middle of the shot she slows near the right side of the terrace, turns her head toward the luminous valley, and relaxes her shoulders while the kite settles into a steady hover behind her. Use a 35mm-equivalent camera beginning at child height in a balanced medium-wide, then perform a very slow stabilized crane backward and upward to reveal the shrine, curved rice terraces, lake, railway, and mountain layers. The move is deliberate and nearly imperceptible at first, becoming grand only in the final third. During the last two seconds hold the resolved composition while prayer streamers, grasses, Hana's clothing, kite tails, cloud edges, and reflected lake light continue subtle natural motion. Pink-purple clouds frame the low sun and stable golden rays wash through the valley. Preserve exact identity, wardrobe, prop geometry, HoloSomnia style, and rightward screen direction. No cuts, jumps, teleports, duplicates, morphing, sudden zooms, frozen frame, or camera shake.

overall_soundscape: gentle ridge wind, one soft bronze shrine-bell resonance, prayer streamers, kite flutter, distant birds and valley water; no dialogue.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>07_mountain_shrine_v2_resolution_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/07_mountain_shrine_v2_resolution_720p.txt`](prompts/h3/07_mountain_shrine_v2_resolution_720p.txt)

```text
<Picture 1> is the authoritative final frame of the immediately preceding cloud-ascent shot. Preserve its single white kite in the upper-right, its rightward glide, the taut cream line running diagonally down-left, the warm pink-purple-gold open sky, the valley depth, and the exact HoloSomnia painted-cel rendering as the incoming continuity state. Carry that direction and diagonal into the shrine composition, fitting the kite naturally into the new wide scale. Do not reproduce the cloud corridor as a separate location once the shrine terrace is revealed.

<Picture 2> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 3> is the exclusive authority for the kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with a fine warm-grey perimeter, pale bamboo cross spars, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background.

<Picture 4> is the exclusive authority for the mountaintop shrine terrace, lower-left stone steps, vermilion torii, shrine building, lanterns, prayer streamers, curved rice terraces, lake, layered mountains, sunset lighting, and polished HoloSomnia hand-painted cel-animation style.

integrated_multimodal_description: One uninterrupted 8.7-second vertical resolution shot with one continuous character action and one slow camera move. The flight is already in progress; there is no relaunch and no second kite.

OPENING: begin in a balanced high three-quarter wide view of the exact shrine terrace in <Picture 4>, visually matching <Picture 1>'s warm valley and diagonal. The torii stands across the upper-middle and the lower-left stone steps provide the entrance. The single white kite is already gliding in the upper-right sky on a long taut cream line that angles down toward the lower-left steps. It begins prominently enough to match the outgoing shot, then recedes naturally into the wider shrine scale as the camera pulls back. During the first half-second Hana runs up from the lower-left steps into the terrace, holding the connected dark-wood spool in her right hand. She is breathing after the long run but remains composed and joyful.

ACTION: Hana crosses into the open center of the terrace, slows naturally from a run to a walk, turns to face the high kite, and plants her feet beneath the torii's opening. She begins one continuous controlled retrieval: alternating hand-over-hand pulls guide the taut line while the spool turns in her right hand. The string shortens smoothly and remains visibly connected at every moment. The kite descends in one broad graceful arc from upper-right toward Hana, staying rigid and plain white while its two tails float independently. It never drops suddenly, strikes the ground, circles behind architecture, detaches, or changes shape.

Near the seventh second the kite reaches Hana at chest height. She takes one small step forward and catches its lower frame gently with her left hand while retaining the spool in her right. The line relaxes only after the catch. She settles the kite beside her shoulder, turns with it toward the luminous valley, and becomes still in a relaxed upright stance beneath the torii. Her expression is quietly proud and peaceful rather than exaggerated.

CAMERA: perform one very slow stabilized pullback and vertical crane upward from beginning to end. Start wide enough to show the complete line between Hana and kite; never use a close-up. The movement is subtle during the retrieval, then gains a little height after the catch to reveal the entire torii, shrine terrace, curved paddies, glowing lake, and layered mountain silhouettes. Preserve screen geography and a level horizon. In the final 1.5 seconds, hold the grand resolved composition through continued camera drift rather than freezing.

ENVIRONMENT AND ENDING: prayer streamers lift softly, pampas grass and Hana's clothing breathe in the same ridge wind, the bronze bell sways once, cloud edges drift slowly, and the lake carries warm reflected light. Stable golden rays pass through pink and lavender clouds around the low sun. End with Hana and the secured white kite small beneath the torii against the immense glowing valley: calm, complete, and grand.

Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, luminous but controlled HoloSomnia colors, consistent anatomy and wardrobe, exact prop geometry, and clean object separation. Exactly one Hana and one kite. No duplicate subjects, extra limbs, broken or looping string, relaunch, teleport, morphing, sudden zoom, orbit, camera shake, cut, subtitles, logo, or watermark.

overall_soundscape: Gentle ridge wind, receding footfalls on stone, soft hand-over-hand string and spool sounds, white kite-paper and ribbon flutter descending closer, one restrained bronze shrine-bell resonance, prayer streamers, distant birds, and valley water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>07_mountain_shrine_v3_simple_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/07_mountain_shrine_v3_simple_720p.txt`](prompts/h3/07_mountain_shrine_v3_simple_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 2> is the exclusive authority for the kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with a fine warm-grey edge, pale bamboo cross spars, exactly two narrow white ribbon tails, one thin cream string, and one small dark-wood spool. Use none of the gradient background.

<Picture 3> is the exclusive authority for the mountaintop shrine terrace, lower-left stone path, vermilion torii, cedar shrine building, lanterns, prayer streamers, curved rice terraces, glowing lake, layered mountains, golden-hour lighting, and polished HoloSomnia hand-painted cel-animation style.

integrated_multimodal_description: One uninterrupted 8.7-second calm closing shot. Begin in a balanced medium-wide view of the shrine terrace. Hana enters from the lower-left at a light run, traveling toward screen-right while holding the dark-wood spool in her right hand. The single white kite glides high behind her through the upper-left sky, connected by one clean gently taut cream string. Its two white tails stream separately in the ridge wind.

Hana crosses beneath the vermilion torii and naturally slows from a run to a walk. Near the open center-right of the terrace she eases to a stop, relaxes her shoulders, and turns her head toward the glowing valley. She keeps the spool low in her right hand. The kite remains high and stable behind her, drifting softly without descending, diving, or changing shape. The string stays visibly connected and gently taut.

Use one very slow stabilized camera pullback and crane upward. Begin at child height with Hana readable as a full figure, then gradually reveal the complete torii, shrine terrace, curved paddies, lake, and mountain layers. The move stays smooth, level, and restrained, becoming grand only in the final third. During the last two seconds, keep the resolved wide composition while the camera continues an almost imperceptible drift.

Prayer streamers lift softly, pampas grass and Hana's clothing move in the same breeze, one bronze bell sways gently, cloud edges drift slowly, and the lake carries warm reflected light. Stable golden rays pass through immense pink and lavender clouds around the low sun. End with Hana and the high white kite small beneath the torii against the luminous valley: peaceful, powerful, and complete.

Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, exact identity and wardrobe, exact kite geometry, clean object separation, and consistent screen direction. Exactly one Hana and one kite. No duplicate subjects, extra limbs, broken or looping line, grounded kite, relaunch, catch choreography, teleport, morphing, sudden zoom, orbit, camera shake, cut, subtitles, logo, or watermark.

overall_soundscape: Gentle ridge wind, receding canvas-shoe footfalls on stone, soft spool and taut-string sounds, distant kite-paper and ribbon flutter, prayer streamers, one restrained bronze bell resonance, distant birds, and valley water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>07_mountain_shrine_v4_walk_reel_close_720p.txt</code> - final render seed `94931`</summary>

Source: [`prompts/h3/07_mountain_shrine_v4_walk_reel_close_720p.txt`](prompts/h3/07_mountain_shrine_v4_walk_reel_close_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, warm dark-brown eyes, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 2> is the exclusive authority for the single plain white kite, line, and spool. Preserve one rigid unmarked white paper diamond, pale bamboo cross spars, exactly two narrow white ribbon tails attached at the lower point, one thin cream flight line connected to a hidden back/underside bridle below the spar intersection, and one small dark-wood spool. The line never attaches to the top point or crosses the visible upper face.

<Picture 3> is the exclusive authority for the mountaintop shrine terrace, stone approach, vermilion torii, cedar shrine building, mossy lanterns, prayer streamers, curved paddies, glowing lake, layered mountains, setting sun, wind-shaped grasses, and polished HoloSomnia hand-painted cel-animation style.

integrated_multimodal_description: A 10.1-second vertical closing scene told in two deliberate cinematic shots. Preserve one Hana, one kite, one spool, one continuous line, the same shrine, the same setting sun, and the same wind across the cut.

[Shot 1 — 0.0 to 3.4 seconds] Begin in a majestic wide view from behind and slightly below Hana. She is already in the lower foreground walking steadily away from the camera along the stone approach toward the shrine and vermilion torii. She holds the dark-wood spool in her right hand. The single white kite flies high above and behind her in the upper-right sky, its cream line connected from the hidden underside bridle to the spool. The camera performs a smooth forward dolly that gradually closes the distance to Hana while preserving the complete torii, low setting sun, glowing lake, mountain layers, and broad wind-filled terrace. Her pace is calm after the run; her hat brim, bobbed hair, blouse, culottes, prayer streamers, and pampas grass all move coherently in the ridge wind.

[Shot 2 — clean cut at 3.4 seconds] Cut to a frontal three-quarter medium-wide angle from near the shrine, looking back toward Hana, the torii, and the luminous valley. Hana continues walking toward the camera for one step, then slows and begins winding the kite down. She turns the small spool steadily with her right hand and guides the cream line with her left. The line shortens continuously while remaining connected to the hidden underside bridle. The kite descends from the upper-right in one smooth wind-borne arc, fluttering and rocking gently while its two tails stream behind it. The camera slowly dollies closer throughout this shot but remains wide enough to retain the torii, setting sun, colored clouds, lake, and moving grasses behind her.

Around 7.8 seconds the kite reaches Hana at shoulder height. She stops winding, reaches with her left hand, catches the lower bamboo frame, and pulls the kite close against her chest. The spool stays secure in her right hand with the line neatly gathered. She takes one settling breath, turns slightly toward the warm light, and smiles with quiet joy. The wind continues to stir her hat ribbon, hair, clothes, kite tails, prayer streamers, and pampas grass.

End with Hana prominent in the foreground from roughly the waist up, holding the complete white kite close and smiling. Behind her, the vermilion torii frames the low sun and the immense valley remains clearly readable. The final image feels intimate and grand at once. Keep the camera gently moving closer through the last frame; no frozen pose.

Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, luminous pink-purple-gold HoloSomnia color, consistent anatomy, exact wardrobe, and exact kite construction. No duplicate Hana, duplicate kite, extra limbs, broken or looping line, top-face string attachment, grounded kite, sudden fall, morphing, continuity change across the cut, camera shake, Dutch angle, subtitles, logo, or watermark.

overall_soundscape: Gentle ridge wind, soft footsteps on stone, spool turning and line sliding through Hana's guiding hand, kite-paper and twin-ribbon flutter drawing closer, prayer streamers, one quiet bronze bell resonance, distant birds, and valley water. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>08_bunny_field_scatter_720p.txt</code> - final render seed `96541`</summary>

Source: [`prompts/h3/08_bunny_field_scatter_720p.txt`](prompts/h3/08_bunny_field_scatter_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 2> is the exclusive authority for the single kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with pale bamboo cross spars, exactly two narrow white ribbon tails at its lower point, one cream flight line connected behind the lower half of the kite, and one small dark-wood spool. Use none of the gradient background.

<Picture 3> is the exclusive authority for the golden field, exactly four rabbits, one wooden water trough, one rectangular hay bale, horizontal background path, lake, paddies, mountains, multicolored golden-hour sky, and polished HoloSomnia hand-painted cel-animation style. Preserve the three clean depth layers and all foreground object positions.

integrated_multimodal_description: One uninterrupted approximately five-second vertical action shot at rabbit-eye height. Begin with the exact four rabbits from <Picture 3> separated around the foreground trough and hay bale. Two adults and two smaller kits are calm but alert. In the distant background, Hana bursts into frame from screen-left already running rapidly toward screen-right along the horizontal field path. She is small in the landscape and clearly behind the rabbits. She holds the dark-wood spool in her right hand. The single white kite flies high behind her in the upper-left sky, far from her body, with one long taut cream line visibly connected to the spool and two tails streaming backward.

During the first second Hana's approaching footfalls and the moving kite shadow catch the rabbits' attention. All four ears snap upright and pivot toward her; four heads turn in quick succession from left to right. A small wind ripple crosses the trough water and the tall grass bows toward screen-right.

As Hana reaches the background center, the rabbit family scatters in four distinct readable paths. The left adult bounds through the flowers toward the lower-left edge. The right adult makes one clean energetic leap past the near corner of the hay bale toward lower-right. One kit darts behind the trough toward frame-left, and the other kit zigzags once before disappearing into tall grass beside the hay. Each rabbit remains anatomically coherent with separate legs, ears, and body; none duplicates, merges, changes size, or collides with another rabbit, the trough, or the bale.

Hana continues her fast left-to-right run throughout, using lively varied strides and one buoyant bounding step without stopping or looking at camera. A stronger gust lifts the kite slightly higher and makes both white tails flutter sharply; the kite remains behind her direction of travel and the line remains connected.

Use one smooth stabilized low lateral camera slide toward screen-right, moving slower than Hana so the foreground rabbits, trough, and hay bale create strong painted parallax while her background crossing stays readable. Near flowers and seed heads sweep gently past the lens, middle grass rolls in wind waves, trough water carries gold and lavender reflections, and distant cloud rays remain stable. End as Hana clears the right background and the last rabbit tail vanishes into the grass, with wind still moving through the field.

Preserve crisp inked contours, flat two-tone cel shading, matte gouache texture, luminous pink-purple-gold HoloSomnia color, exact identity, coherent scale, and clean depth separation. Exactly one Hana, one kite, four rabbits, one trough, and one hay bale. No duplicate subjects, extra animals, grounded kite, broken string, stiff run loop, foot sliding, rabbit morphing, camera shake, sudden zoom, cut, subtitles, logo, or watermark.

overall_soundscape: Quick distant footfalls, grass hiss rising in the wind, four light rabbit rustles and soft landing thumps, one small trough-water slosh, kite-paper and twin-ribbon flutter, insects, and distant lake ambience. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>09_train_lateral_overtake_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/09_train_lateral_overtake_720p.txt`](prompts/h3/09_train_lateral_overtake_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 2> is the exclusive authority for the single kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with pale bamboo cross spars, exactly two narrow white ribbon tails at its lower point, one cream flight line connected behind the lower half of the kite, and one small dark-wood spool. Use none of the gradient background.

<Picture 3> is the exclusive authority for the safe foreground path, cedar fence, straight railway, single coherent cream-and-vermilion two-car train, wet paddies, hydrangeas, valley, multicolored golden-hour sky, and polished HoloSomnia hand-painted cel-animation style. Preserve the clean side-on depth separation and horizontal left-to-right route.

integrated_multimodal_description: One uninterrupted approximately five-second vertical tracking shot with fast left-to-right energy. Hana enters from screen-left already sprinting naturally along the safe foreground path. She remains completely in front of the cedar fence and never approaches the rails. She holds the dark-wood spool securely in her right hand. The single white kite flies high and well behind her in the upper-left, connected to the spool by one long taut cream line, with its two tails streaming opposite her direction of travel.

At the same moment, the single two-car local train from <Picture 3> travels left-to-right on the middle-distance track parallel to Hana. It begins slightly behind her and moves somewhat faster, smoothly overtaking her during the shot. The train remains one stable connected two-car vehicle with coherent windows, doors, pantographs, wheels, and carriage length. Warm sunset reflections slide across its windows, briefly casting moving gold and magenta bands over the wet paddies and Hana's clothing as it passes.

Hana runs with lively varied mechanics rather than a repeated cycle: strong planted steps, changing stride length, active free-arm drive, natural shoulder and hip counter-rotation, and one long buoyant stride when the train draws level. She glances sideways at the passing windows with an excited smile, then looks forward and accelerates. She never stops, poses, crosses the fence, or turns toward the camera.

As the train overtakes, its pressure wave moves visibly through the scene from left to right. Hydrangea leaves tremble, tall grasses flatten then spring back, water ripples spread across the paddies, Hana's hat brim lifts, her bob and clothing stream, and the kite surges higher on the taut line. The kite remains behind Hana and never touches the train, poles, wires, or fence.

Use one competent stabilized lateral camera track at Hana's speed from a low three-quarter side view. Maintain a level horizon and constant subject scale with no handheld shake, vibration, orbit, or zoom. Foreground hydrangeas and grass sweep quickly, fence posts pass at a steady rhythm, Hana remains crisp and readable, the train slides faster on the middle plane, and distant hills move slowly in controlled multiplane parallax. End as the rear carriage moves ahead toward screen-right while Hana keeps running powerfully beneath the high trailing kite.

Preserve crisp inked contours, flat two-tone cel shading, matte gouache texture, luminous pink-purple-gold HoloSomnia color, consistent identity, stable train geometry, and clean object separation. Exactly one Hana, one kite, and one two-car train. No duplicate vehicles, detached carriage, extra limbs, broken string, grounded kite, collision, reversed train, foot sliding, stiff run loop, camera shake, sudden zoom, cut, subtitles, logo, or watermark.

overall_soundscape: Fast varied footfalls on packed earth, smooth electric-train motor and rail rhythm, a brief passing-air swell, fence and grass rush, hydrangea leaves, water ripples, taut string hum, kite-paper and twin-ribbon flutter, and distant mountain birds. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>09_train_lateral_simple_v2_720p.txt</code> - exploration prompt; no selected-render seed</summary>

Source: [`prompts/h3/09_train_lateral_simple_v2_720p.txt`](prompts/h3/09_train_lateral_simple_v2_720p.txt)

```text
<Picture 1> is the exclusive authority for Hana's identity, age, face, hair, body proportions, and wardrobe. Preserve exactly one eleven-year-old East Asian girl with one head, one torso, exactly two arms, exactly two hands, and exactly two legs. She has a chin-length black bob, a straw sunhat with an indigo band, a cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Use none of the studio background.

<Picture 2> is the exclusive authority for the single kite, line, and spool. Preserve exactly one plain unmarked white paper diamond kite with pale bamboo cross spars, exactly two narrow white ribbon tails at its lower point, one thin cream flight line, and one small dark-wood spool. Use none of the gradient background.

<Picture 3> is the exclusive authority for the composition and setting. Preserve the same broad foreground path, cedar fence, straight railway, single cream-and-vermilion two-car local train, wet paddies, hydrangeas, valley, golden-hour sky, and polished HoloSomnia hand-painted cel-animation style. Do not redesign, relocate, duplicate, or replace the train, path, fence, fields, or camera axis.

integrated_multimodal_description: One uninterrupted approximately five-second vertical shot. Hana runs naturally from screen-left to screen-right along the safe foreground path. She remains entirely in front of the cedar fence and never approaches the railway. Her right hand alone holds the dark-wood spool for the entire shot. Her left hand is empty for the entire shot and simply swings with her running gait. Her two hands remain clearly separated and attached to their correct arms at all times.

The single local train passes from screen-left to screen-right on the middle-distance track behind Hana. Hana and the train move in the same direction on two separate depth planes. The train travels slightly faster and slides past her smoothly while preserving the exact two-car geometry, windows, doors, wheels, roof equipment, and cream-and-vermilion colors from <Picture 3>.

The single plain white kite flies high behind Hana in the upper-left sky. One long taut cream line connects the kite directly to the spool in her right hand. The kite trails opposite Hana's direction of travel, remains safely clear of the train and wires, and keeps exactly two ribbon tails.

Use one smooth stabilized lateral camera track toward screen-right at Hana's running speed. Keep Hana full-body and readable in a clean side profile with open space ahead. Maintain a level horizon, constant camera height, and constant subject scale. Foreground grasses and hydrangeas slide past gently, fence posts create steady parallax, the train moves smoothly behind her, and distant hills shift slowly. Golden light remains stable while a light breeze moves the grass, Hana's hat brim and clothing, and the kite tails.

Hana performs one simple continuous run with natural alternating steps, planted feet, ordinary arm swing, and no tricks. She looks forward where she is going. No glance toward train, no jump, no skip, no wave, no hand change, no object transfer, no dramatic gust, and no pressure-wave reaction.

Preserve crisp stable ink contours, flat two-tone cel shading, matte gouache texture, luminous pink-purple-gold HoloSomnia color, exact identity, stable train geometry, and clean object separation. Exactly one Hana, two arms, two hands, two legs, one spool in the right hand, one kite, one string, and one two-car train. No third hand, extra arm, extra fingers, duplicate subject, detached carriage, broken string, grounded kite, collision, reversed motion, foot sliding, morphing anatomy, camera shake, vibration, sudden zoom, cut, subtitles, logo, or watermark.

overall_soundscape: Steady natural running footfalls, smooth electric-train motor and rail rhythm passing behind her, light wind through grasses and hydrangeas, soft kite-paper and ribbon flutter, and distant mountain birds. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

<details>
<summary><code>09_train_wide_plate_v3_720p.txt</code> - final render seed `97019`</summary>

Source: [`prompts/h3/09_train_wide_plate_v3_720p.txt`](prompts/h3/09_train_wide_plate_v3_720p.txt)

```text
<Picture 1> defines Hana only: one eleven-year-old East Asian girl with a chin-length black bob, straw sunhat with indigo band, cream short-sleeve collared blouse, loose indigo culottes, white ankle socks, and red canvas shoes. Preserve her identity and proportions exactly. Ignore the portrait background.

<Picture 2> defines one plain white paper diamond kite only: pale bamboo cross spars, two narrow white ribbon tails, one thin cream flight line, and one small dark-wood spool. Ignore the blue gradient background.

<Picture 3> defines the shot. Preserve its wide composition, camera height, scale, depth, and HoloSomnia cel-painted style: the broad diagonal dirt path in the foreground, hydrangeas at the lower edge, flooded paddies, low cedar fence, the small cream-and-vermilion two-car local train on the middle-distance track, valley, mountains, and luminous pink-purple-gold sunset. Do not replace this with a close side-profile view. The train must remain small and fully readable at approximately its Picture 3 scale.

integrated_multimodal_description: One uninterrupted five-second wide vertical landscape shot. Begin from almost exactly the composition of <Picture 3>. Hana enters from the lower-left edge and runs energetically toward screen-right along the broad foreground dirt path. She stays small in the landscape, approximately one-sixth of the image height, and remains safely in front of the fence. Her stride is loose, lively, and natural, with alternating planted footsteps and an ordinary two-arm running rhythm.

Both of Hana's hands are empty, simple closed running fists. Her left hand belongs only to her left arm and her right hand belongs only to her right arm. The small wooden spool is securely clipped at her right waistband beside her hip; she never touches it. The single thin flight line begins at that hip-mounted spool, extends cleanly upward behind her, and connects to the underside bridle of one modest-sized white kite high in the upper-left sky. The kite trails her motion and its two ribbon tails flutter in the breeze.

At the same time, the same small two-car train already visible in <Picture 3> glides smoothly from screen-left toward screen-right along the middle-distance railway behind Hana. It keeps its original diagonal perspective, exact two-car form, colors, roof equipment, and distance. The train gradually passes behind her while never becoming huge or filling the frame.

The camera makes a gentle stabilized pan-track toward screen-right, just enough to keep Hana in the lower foreground while preserving the grand landscape and the train's original scale. The horizon is locked and level. Fence posts and foreground grass create clean lateral parallax; distant mountains barely move. Water softly reflects the sunset, grasses and Hana's hat brim respond to a light breeze, and the golden-pink rays remain steady. No camera shake, zoom, cut, or scene redesign.

Visual priorities: preserve <Picture 3> first; one small Hana, one small two-car train, one modest white kite. Hana has exactly one head, one torso, two arms, two hands, and two legs. Both hands stay empty. The spool remains clipped to her hip. No extra hand, duplicate limb, fused arm, object in hand, giant kite, giant train, close-up, anatomy morph, foot sliding, train deformation, broken string, reversed direction, duplicate subject, text, logo, or watermark.

overall_soundscape: light natural running footfalls on dirt, a smooth electric-train motor and quiet rail rhythm in the middle distance, breeze through grass, soft kite-paper and ribbon flutter, and distant birds. No dialogue and no music.
non_diegetic_music: N/A
```

</details>

## Licensing

Code and workflow glue are released under the MIT License. Generated reference artwork is included for reproducibility; copyright in those media assets remains with the repository owner.

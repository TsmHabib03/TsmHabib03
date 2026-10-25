---
name: Tokyo at Night
description: Moonlit rooftop pixel-art identity for Habib's GitHub developer profile.
colors:
  sky: "#11132C"
  sky-low: "#191D3F"
  distant: "#232D57"
  mid: "#34477C"
  front: "#465992"
  edge: "#7182BC"
  window: "#D5E5FF"
  window-dim: "#7388BF"
  warm: "#D5BC97"
  moon: "#B9B5F4"
  moon-light: "#D6D6FF"
  moon-shade: "#898BD0"
  cat: "#10152D"
  cat-edge: "#A8ACF0"
  cat-shade: "#1C2445"
  ledge: "#202747"
  rail: "#8387D4"
  text: "#DCEBFF"
  cyan: "#76C8EA"
  orange-base: "#CE925C"
  orange-shade: "#9D633F"
  orange-rim: "#F1CEA0"
  orange-patch: "#9D633F"
  orange-ear: "#D6A1A0"
  calico-base: "#E1DED7"
  calico-shade: "#A7A4AE"
  calico-rim: "#F5EDDF"
  calico-patch: "#C88C57"
  calico-dark: "#34364C"
  calico-ear: "#D6A1A0"
spacing:
  lettering-inset: "32px"
components:
  hero-desktop:
    backgroundColor: "{colors.sky}"
    textColor: "{colors.text}"
    width: "1200px"
    height: "440px"
  hero-mobile:
    backgroundColor: "{colors.sky}"
    textColor: "{colors.text}"
    width: "600px"
    height: "464px"
  connect-desktop:
    backgroundColor: "{colors.sky}"
    width: "1200px"
    height: "200px"
  connect-mobile:
    backgroundColor: "{colors.sky}"
    width: "600px"
    height: "200px"
---

# Design System: Tokyo at Night

## Overview

**Creative North Star: "Tokyo at Night"**

A large back-view calico cat watches a moonlit indigo city from a pixel rooftop. Layered blue buildings, dense cool windows, a lavender stepped moon, and quiet pale lettering establish the identity. A curled tail occasionally changes pose, and a sparse subset of windows briefly dims; the architecture, moon, clouds, and name remain stationary.

The system describes the current profile hero, a three-cat Connect panorama, and compact brand/contact marks. The reference image guides the composition and atmosphere; the artwork is original self-contained SVG geometry. GitHub owns surrounding Markdown typography, spacing, link states, and page colors. The scoped `ROOFTOP_NIGHT` dictionary in `scripts/profile_theme.py` owns current scene colors; `CAT_COATS` owns shared black, orange, and calico fur colors. Legacy `AFTER_HOURS` tokens, city/rail helpers, and older artwork remain available with their existing behavior; compact marks retain source colors or established display tints.

**Key Characteristics:**

- Crisp bitmap lettering and integer scene geometry.
- Three tonal city layers with cool window patterns and sparse warm lights.
- Seated cats with asymmetric ears, coat-specific rim pixels, warm orange stripes or calico patches, and four discrete tail poses.
- A stepped crater moon and raised building roofs with coping, deck seams, and windowed façades.
- Complete static artwork beside native profile content and functional links.

## Colors

The palette runs from midnight indigo through muted blue façades to pale windows and lavender moonlight. The frontmatter records the exact values from `ROOFTOP_NIGHT`.

### Primary

**Cyan** carries the qualification subtitle. **Text** carries the prominent name, keeping the identity distinct from the detailed lower city.

### Secondary

**Moon**, **moon-light**, and **moon-shade** form the stepped lunar disc and crater pixels. **Cat-edge** gives the black silhouette a narrow lavender rim rather than a glow. Orange and calico coats use their own pale rim colors, shaded fur, ear interiors, and restrained warm patches from `CAT_COATS`; the frontmatter records those exact shared colors.

### Tertiary

**Warm** appears in a small share of illuminated windows. The dominant window character remains cool.

### Neutral

**Sky** and **sky-low** define two flat sky tones. **Distant**, **mid**, and **front** separate building depth; **edge** is the shared scene-detail token. **Window** and **window-dim** provide readable architectural patterns. **Cat** and **cat-shade** define the silhouette, body details, and cast pixel shadow. **Ledge** and **rail** separate the foreground rooftop from the city.

These illustration colors do not recolor every technology logo. The portfolio/email marks use the established authored pixel geometry and legacy palette; other compact marks preserve trustworthy upstream silhouettes and display tints.

## Typography

Hero lettering is authored geometry from `PIXEL_FONT` in `scripts/generate-profile-assets.py`, with no CSS font or external font file. Most uppercase glyphs use five columns and five rows; punctuation and spaces have their own widths.

The desktop name uses 10px cells, producing 50px-high glyphs at source scale. Mobile uses 9px cells and two name lines, producing 45px-high glyphs. The `BSCS · WEB DEVELOPER` subtitle uses 3px cells on desktop and 4px cells on mobile, producing 15px and 20px-high glyphs. These dimensions are SVG source units and scale with the displayed image.

GitHub provides native heading, paragraph, list, and link typography. Background, project context, skill names, and destinations stay in Markdown; decorative scene banners contain no factual section text.

## Layout

Desktop hero artwork is 1200 × 440; mobile is independently composed at 600 × 464. Both start lettering 32 source units from the left. Desktop places the name at y=36 and subtitle at y=104. Mobile places `HABIB` at y=32, `JAUDIAN D.` at y=98, and the subtitle at y=160.

The quiet upper-left sky carries the identity, with the moon at upper right and a large calico seated on a raised foreground building roof. The flat lower-sky band begins at y=142 on desktop and y=208 on mobile. Mobile recomposes the scene and type rather than cropping the desktop source.

Only Connect has a second panorama: 1200 × 200 desktop and 600 × 200 mobile. Black, orange, and calico cats share one raised rooftop. About Me, Current Focus, Tech Stack, and Featured Projects use native text without illustrations. Fixed seeds and shared geometry preserve the city identity across the two scenes. The current README composition lives in `.impeccable/surfaces/readme-md.md`.

The README selects mobile sources at viewport widths up to 600px, after reduced-motion sources. Technology marks display at 40px in four compact labeled groups; contact marks display at 36px beside six linked labels, and project marks remain 18px. Short rows wrap naturally at narrow widths; the email address sits below its linked label. Full-width images adapt to the available host column. Local Chromium previews at 320px, 375px, and desktop widths are local evidence; live GitHub rendering has not been verified.

## Elevation & Depth

Depth comes from flat tonal layering, architecture occluding distant windows, and the foreground cat and rooftop ledge. Animated lamps remain inside their city layers so nearer buildings still cover them. The cat uses a stepped solid-color shadow, rather than a blurred effect. Current scenes contain no gradients, filters, glow, or atmospheric blur.

## Shapes

Scene geometry uses integer rectangles batched into same-color paths with `shape-rendering="crispEdges"`. The current outer artwork is rectangular. Buildings, cloud steps, moon craters, asymmetric cat ears, tail segments, and checkered parapet edges share hard pixel geometry.

The moon spans 24 stepped rows: 4px cells on desktop, 3px on mobile, and 2px in section panoramas. The cat silhouette is 48 cells high: 3px cells in heroes and 2px in Connect. Hero paws sit 60 source units above the scene bottom; Connect paws sit 44 units above it. Tail and shadow geometry extend onto the roof deck. The Connect trio uses 110-unit spacing on a shared 400-unit roof; hero roof widths are 340 desktop and 284 mobile.

At arbitrary browser widths, source coordinates may map to fractional device pixels. Crisp-edge rendering preserves the intended hard-edged character; it does not guarantee a one-to-one source/device pixel grid.

## Components

### Rooftop hero

Four variants share the scene helper, palette, bitmap font, and tail/light model. Desktop and mobile each have animated and animation-free `-still.svg` editions. The name remains `HABIB JAUDIAN D.` and the subtitle remains `BSCS · WEB DEVELOPER`. The current hero contains no train.

The README's `<picture>` selects reduced-motion still sources before standard mobile selection. Animated SVGs also contain an internal reduced-motion query. The hero image alternative identifies Habib, the qualification, and the moonlit city/cat scene.

### Cat tail and window lights

Four tail groups switch visibility using `steps(1,end)` in a 14-second cycle. The tail rests for most of the cycle, then briefly switches among rise, curl, and return poses before returning to rest. Exactly one pose per cat is visible at a time; there is no smooth rotation of pixel geometry.

A few windows use staggered 11-, 17-, and 23-second cycles with delays of −3, −9, and −15 seconds. Their opacity briefly drops from 1 to 0.22, then returns. Most windows remain stationary, avoiding synchronized whole-scene flashing.

Reduced motion disables tail and window animations. With CSS unavailable, visibility attributes show only the resting tail and all windows remain illuminated. Static editions contain no animation stylesheet and preserve the same complete scene.

### Connect panorama

Connect uses four variants: animated/static × desktop/mobile. Three distinct coats share the same seated silhouette, connected tail geometry, and rooftop. Its image alternative describes the cats; native linked labels communicate the contact destinations. The four middle sections have no panorama references. Legacy section assets and full-generation support remain available for compatibility.

### Compact marks

The current output set contains 28 SVGs: four heroes, four Connect variants, and 20 transparent 28 × 28 brand/contact marks. Inputs from Devicon and Simple Icons are attributed in `assets/README.md`; portfolio and email marks are authored geometry. Compact PHP, Bootstrap, and VS Code marks flatten source gradients and remove filters while retaining upstream silhouettes. Raw inputs and legacy labeled assets remain intact.

### Native text and links

Markdown headings, paragraphs, lists, project links, and the six supplied contact links use GitHub's native rendering and interaction states. Embedded SVGs supply no custom interactive controls. Contribution graphics are omitted because GitHub already displays contribution activity; their generation and data remain available.

## Do's and Don'ts

### Do

- Do change scene colors through `ROOFTOP_NIGHT` and shared fur colors through `CAT_COATS`.
- Do preserve the resting cat and illuminated city in static and reduced-motion alternatives.
- Do keep profile facts, technology names, and destinations in native Markdown.
- Do regenerate current README artwork with `python scripts/generate-profile-assets.py --profile-only`; `--hero-only` remains available for the four heroes.

### Don't

- Don't animate the name, buildings, moon, or clouds.
- Don't add a train to the current rooftop scene.
- Don't add gradients, glow, excessive neon, or external image/font dependencies to current scenes.
- Don't change legacy tokens or artwork as a side effect of current profile edits.
- Don't claim live GitHub compatibility from local browser screenshots.
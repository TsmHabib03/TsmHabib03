---
name: Tokyo After Hours
description: Restrained pixel-art identity for Habib's GitHub developer profile.
colors:
  sky: "#081426"
  distant: "#12233D"
  mid: "#1D3554"
  front: "#294766"
  edge: "#42617F"
  dim: "#3B5674"
  text: "#DCEBFF"
  cyan: "#76C8EA"
  warm: "#D5AA72"
  steel: "#A5B8CC"
  roof: "#66839F"
  glass: "#152B43"
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
---

# Design System: Tokyo After Hours

## Overview

**Creative North Star: "Tokyo After Hours"**

The profile's artwork uses a quiet night city and a cyan-striped commuter train to give Habib's developer identity a recognizable setting. Pale pixel lettering and sparse warm lights carry the emphasis. The city stays stationary while the train supplies one clear animated moment.

This system describes the four profile hero SVGs. GitHub owns the surrounding Markdown typography, spacing, link states, and page colors. Legacy TokyoNight Storm assets and helpers retain their existing tokens; the scoped `AFTER_HOURS` dictionary in `scripts/profile_theme.py` is the hero palette source.

**Key Characteristics:**

- Crisp bitmap lettering and integer scene geometry.
- Tonal building layers with restrained warm lights.
- Three connected carriages unified by a cyan stripe.
- Native profile text and links with useful static artwork alternatives.

## Colors

The palette moves from dark navy to slate blue, with pale text, a single cool accent, and limited warm highlights. The frontmatter records the exact values from `AFTER_HOURS`.

### Primary

**Cyan:** the shared train stripe and scene title. Its repetition connects the identity lettering to the moving train.

### Secondary

**Warm:** the Tokyo Tower lattice, a small share of building windows, and train window highlights.

### Neutral

**Sky** supplies the quiet background. **Distant**, **mid**, and **front** distinguish building depth. **Dim** and **edge** define sparse windows and railway details. **Text** carries the name. **Steel**, **roof**, and **glass** separate carriage bodies, equipment, doors, and windows.

The name and cyan scene title have recorded contrast ratios of 15.26:1 and 9.86:1 against the sky. These checks apply to artwork text; GitHub controls native text colors.

## Typography

Hero lettering is authored geometry from `PIXEL_FONT` in `scripts/generate-profile-assets.py`, rather than a CSS font or external font file. Most uppercase glyphs use five columns and five rows. A one-cell gap separates glyphs; spaces and punctuation have their own widths.

The desktop name uses 10px cells, creating a 50px-high glyph. Mobile uses 9px cells and a two-line name, creating 45px-high glyphs. The scene title uses 3px cells, creating 15px-high glyphs in both variants. All dimensions are source SVG units and scale with the displayed image.

The README keeps personal background, project context, skills, and destinations as native Markdown. Do not substitute bitmap image text for that content.

## Layout

The desktop source is 1200 × 440; mobile is independently composed at 600 × 464. The README displays the selected image at full available width and switches to mobile sources at viewport widths up to 600px. Lettering starts 32 source units from the left. City stages begin at y=140 on desktop and y=188 on mobile.

The name remains in quiet upper sky. The skyline and tower occupy the lower scene, with the elevated railway beneath them. Mobile uses fewer buildings and two name lines to preserve readability rather than cropping the desktop composition.

The current native section order belongs to `.impeccable/surfaces/profile.md`. Source artwork and local padded host previews were inspected at 320px, 375px, and desktop widths; these are not live GitHub captures.

## Elevation & Depth

Depth comes from tonal building layers and ordered overlaps: the tower sits between middle buildings and the low foreground; railway masts cross the train. There are no shadows, gradients, filters, glow, or blurred atmospheric effects in the hero.

## Shapes

The scene uses integer rectangles batched into same-color paths, with `shape-rendering="crispEdges"`. Most architectural details follow a two-pixel source grid. The outer sky panel has an 8px stepped corner cut; the scene uses a rectangular clip. Tower taper, cross-braces, and decks use stepped pixel geometry.

The geometry contract applies to source coordinates. At arbitrary browser display widths, scaling maps source pixels onto device pixels; crisp-edge rendering preserves the intended hard-edged character.

## Components

### Tokyo hero

The four variants share the palette, train model, bitmap font, and scene helpers. Desktop and mobile each have animated and animation-free `-still.svg` assets. The README's `<picture>` selects reduced-motion still variants before the standard mobile source, and animated SVGs also contain an internal reduced-motion query. A meaningful image alternative identifies Habib and the scene.

### Three-car commuter train

Three 116px carriages separated by two 8px gaps form a 364 × 48 train. The same model supplies windows, paired doors, roof equipment, wheels, outward cabs, and the cyan stripe in every hero. The still transform centers the complete train.

Only the train animates. Linear loops last 28 seconds on desktop and 24 seconds on mobile. Travel starts at `-TRAIN_WIDTH - TRAIN_MARGIN` and ends at `scene_width + TRAIN_MARGIN`, using a 12px margin. The final 12% of each cycle holds beyond the scene edge before resetting; both reset positions hide the entire train. A calculated negative delay begins with the full train visible.

### Native text and links

Markdown headings, paragraphs, lists, repository links, and social links use GitHub's rendering and interaction states. SVG contents do not provide custom link or hover controls in the embedded profile. Contribution assets and other legacy artwork remain available but are omitted from the current README.

## Do's and Don'ts

### Do

- Do change hero colors through the scoped `AFTER_HOURS` palette.
- Do preserve a complete visible train in static and reduced-motion alternatives.
- Do keep informative profile content and destinations in native Markdown.
- Do regenerate the four variants together with `python scripts/generate-profile-assets.py --hero-only`.

### Don't

- Don't animate the name or scatter motion across the background.
- Don't add glow, gradients, excessive neon, or external image/font dependencies to the hero.
- Don't change legacy artwork tokens as a side effect of editing the hero.
- Don't claim live GitHub compatibility from local browser screenshots.

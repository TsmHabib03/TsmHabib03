---
name: Orange Pixel Profile
description: Dark developer dossier with orange pixel artwork, project cards, and a city footer.
colors:
  ground: "#0d1117"
  panel: "#171c25"
  project-feature: "#1c252b"
  line: "#343c49"
  ink: "#e9eef5"
  muted: "#afbccb"
  orange: "#ff9d38"
  cyan: "#76d8f0"
  purple: "#c5a0ef"
  amber: "#f4cd70"
  mint: "#9ddcb5"
typography:
  display:
    fontFamily: "Silkscreen, monospace"
    fontSize: "clamp(2rem, 5.3vw, 3.6rem)"
    fontWeight: 400
    lineHeight: 1.2
  section:
    fontFamily: "Silkscreen, monospace"
    fontSize: "1rem"
    fontWeight: 400
  title:
    fontFamily: "Silkscreen, monospace"
    fontSize: "1.1rem"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.75
  label:
    fontFamily: "Silkscreen, monospace"
    fontSize: ".75rem"
    fontWeight: 400
rounded:
  square: "0px"
spacing:
  small: "8px"
  gap: "16px"
  group: "24px"
  card: "28px"
  section: "56px"
components:
  action:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.ground}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "13px 16px"
  project-card:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.muted}"
    rounded: "{rounded.square}"
    padding: "28px"
  technology-badge:
    backgroundColor: "{colors.panel}"
    height: "28px"
  contact-mark:
    width: "32px"
    height: "32px"
---

# Design System: Orange Pixel Profile

## Overview

**Creative North Star: "Orange pixel dossier"**

Charcoal surfaces and orange abstract pixels introduce Habib's work. Pixel lettering gives headings character; a regular body face keeps project descriptions readable. Cyan, lavender, amber, and mint distinguish content groups. The supplied city/cat scene anchors the footer.

This replacement follows the latest user brief and supersedes the rejected city-first profile. [profile.css](profile.css) and [profile.html](profile.html) implement the visual behavior. [README.md](README.md) adapts the same content to GitHub-supported HTML. GitHub owns its final background, text styling, table widths, and link states; custom CSS, fonts, overlays, transitions, and animations do not survive README sanitization.

**Key Characteristics:**

- Dark tonal panels, thin borders, and square corners.
- Orange pixel hero with native selectable text.
- Pixel display lettering alongside readable prose.
- Three banner motion variations with reduced-motion support.
- Supplied city/cat at the bottom above four contact destinations.

## Colors

Orange identifies the name, section headings, and primary actions. Cyan identifies the featured schedule project and frontend group. Purple identifies API resources and backend; amber identifies the database group; mint identifies tools and tags.

The ground, panel, featured panel, line, ink, and muted tokens provide tonal depth and legibility. Badges use the panel background with service-rendered white labels. Contact brand marks retain their established colors and attribution.

## Typography

The companion self-hosts Silkscreen under the SIL Open Font License. It carries display headings, navigation, identity, tags, and motion controls. Segoe UI with a sans-serif fallback carries prose. The fluid hero preserves the two-line name on mobile.

Functional pixel labels are 12px. Main paragraphs have a 70ch maximum. The README uses native headings and samp text; GitHub supplies the actual monospace face. Pixel font loading is a companion capability.

## Layout

The companion is at most 960px wide, with 32px side space and 40px outer vertical margin on desktop. At 640px, side space and outer margin become 16px. Sections have 56px separation, reduced to 44px on mobile.

About uses a narrow heading column and wider content column. QCU spans the project grid; API resources and the full-stack card follow in unequal columns. Cards stack on mobile. Technology and education label/value columns also stack. The city image keeps its full 16:9 composition above a centered row of four contacts.

The README uses one column and individual single-cell tables for identity and projects. GitHub strips table width attributes, so visible widths follow content. Badge rows wrap naturally. The required six-section order belongs to the surface brief.

## Elevation & Depth

Depth comes from tonal surfaces, thin borders, and the dark hero blend. Cards have no shadows. Hero inversion, luminosity blending, an orange color layer, and dark gradients adapt the unchanged supplied reference. These effects are confined to the companion.

## Shapes

Cards, actions, and canvas have square corners. One-pixel borders define modules and separators. The abstract reference is clipped as a rectangular crop outside embedded sample lettering. Source pixels remain unchanged.

## Components

### Hero and motion controls

The artwork is a standard image in an absolute crop, with selectable text above it. A labeled fieldset selects Pixel drift, Soft dissolve, or Still. Drift moves the image through six stepped increments over ten seconds. Dissolve changes opacity and saturation over eight seconds. Hover and focus increase visibility through a 700ms transition. Reduced-motion disables keyframes, transitions, and smooth scrolling.

### Actions and navigation

The primary action uses orange with dark text and 13px by 16px padding. Inline links have offset underlines. Navigation wraps naturally; cyan outlines identify keyboard focus. The skip link appears on focus. Selection and scrollbar colors use the palette.

### Project cards

Thin borders and 28px padding define cards, with reduced mobile padding. QCU uses the alternate tonal panel and cyan title. Tags use mint pixel labels. Verified destinations are native links; the API card visibly marks the unresolved destination without invented behavior.

### Technology badges

Twelve Shields.io images use the service's 28px height in four groups. Java and VS Code are text-only badges.

### Footer and contacts

The supplied city/cat appears at the final artwork position. Four existing local marks link to Facebook, Instagram, GitHub, and email. Companion icons have adjacent labels; README images have meaningful alternatives. Existing email geometry has corrected draw order to show its fold.

## Do's and Don'ts

- Do keep facts selectable and project claims tied to verified sources.
- Do retain supplied pixels and provenance; crop and blend through companion CSS.
- Do keep pixel controls readable and support reduced motion.
- Do disclose template inputs and distinguish local previews from published evidence.
- Don't claim custom CSS or fonts work in GitHub README rendering.
- Don't introduce emojis or generated scene artwork into this requested design.
- Don't publish the raw template as complete while its banner and API destination remain unresolved.

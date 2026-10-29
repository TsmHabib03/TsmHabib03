---
name: Reference Square GitHub Profile
description: Three fading identity variations, unified technology logos and one continuous connection banner on GitHub.
colors:
  ink: "#edf2f7"
  white: "#ffffff"
  black: "#232323"
  hero-orange: "#ff8000"
  hero-blue: "#4098f3"
  hero-purple: "#a000d9"
  orange-pale: "#ffe269"
  orange-light: "#ffb528"
  orange-middle: "#ff9700"
  orange-hot: "#ff5b00"
  orange-deep: "#ed2400"
  blue-pale: "#92e4fc"
  blue-light: "#58c9f7"
  blue-cyan: "#00dbe7"
  blue-middle: "#397ae4"
  blue-violet: "#7154ef"
  purple-pale: "#f290f6"
  purple-light: "#da5deb"
  purple-middle: "#b02ddd"
  purple-deep: "#8500c3"
  purple-dark: "#5e0098"
  connection-ground: "#080b1a"
  connection-blue: "#468cc8"
  connection-cyan: "#66c9f3"
  connection-indigo: "#394586"
  cyan: "#76d8f0"
  stack-orange: "#ff8a00"
  lavender: "#c5a0ef"
  stack-amber: "#f4cd70"
typography:
  display:
    fontFamily: "Open Sans"
    fontSize: "40px"
    fontWeight: 700
  display-mobile:
    fontFamily: "Open Sans"
    fontSize: "43px"
    fontWeight: 700
  identity:
    fontFamily: "Open Sans"
    fontSize: "25px"
    fontWeight: 400
  identity-mobile:
    fontFamily: "Open Sans"
    fontSize: "26px"
    fontWeight: 400
  hero-caption:
    fontFamily: "Open Sans"
    fontSize: "19px"
    fontWeight: 400
  hero-caption-mobile:
    fontFamily: "Open Sans"
    fontSize: "20px"
    fontWeight: 400
  web:
    fontFamily: "Open Sans"
    fontSize: "46px"
    fontWeight: 700
  web-mobile:
    fontFamily: "Open Sans"
    fontSize: "42px"
    fontWeight: 700
  developer:
    fontFamily: "Open Sans"
    fontSize: "27px"
    fontWeight: 400
  developer-mobile:
    fontFamily: "Open Sans"
    fontSize: "25px"
    fontWeight: 400
  connection-first-line:
    fontFamily: "Open Sans"
    fontSize: "49px"
    fontWeight: 700
  connection-second-line:
    fontFamily: "Open Sans"
    fontSize: "45px"
    fontWeight: 700
  connection-mobile-first-line:
    fontFamily: "Open Sans"
    fontSize: "35px"
    fontWeight: 700
  connection-mobile-second-line:
    fontFamily: "Open Sans"
    fontSize: "29px"
    fontWeight: 700
  connection-invitation:
    fontFamily: "Open Sans"
    fontSize: "31px"
    fontWeight: 600
  connection-invitation-mobile:
    fontFamily: "Open Sans"
    fontSize: "25px"
    fontWeight: 600
  connection-caption:
    fontFamily: "Open Sans"
    fontSize: "21px"
    fontWeight: 400
  contact-label:
    fontFamily: "Open Sans"
    fontSize: "25px"
    fontWeight: 600
  contact-label-mobile:
    fontFamily: "Open Sans"
    fontSize: "30px"
    fontWeight: 600
  technology-label:
    fontFamily: "Open Sans"
    fontSize: "14px"
    fontWeight: 600
  qualification-first-line:
    fontFamily: "Open Sans"
    fontSize: "24px"
    fontWeight: 600
  qualification-second-line:
    fontFamily: "Open Sans"
    fontSize: "24px"
    fontWeight: 600
rounded:
  square: "0px"
components:
  hero:
    backgroundColor: "{colors.white}"
    textColor: "{colors.black}"
    typography: "{typography.display}"
    width: "1200px"
    height: "384px"
  hero-mobile:
    backgroundColor: "{colors.white}"
    textColor: "{colors.black}"
    typography: "{typography.display-mobile}"
    width: "600px"
    height: "400px"
  connection:
    backgroundColor: "{colors.white}"
    textColor: "{colors.black}"
    width: "1200px"
    height: "310px"
  connection-mobile:
    backgroundColor: "{colors.white}"
    textColor: "{colors.black}"
    width: "600px"
    height: "440px"
  contact-icon:
    width: "72px"
    height: "72px"
  contact-icon-mobile:
    width: "80px"
    height: "80px"
  technology-module:
    textColor: "{colors.ink}"
    typography: "{typography.technology-label}"
    width: "128px"
    height: "94px"
  technology-logo:
    width: "48px"
    height: "48px"
  qualification-bscs:
    textColor: "{colors.stack-orange}"
    typography: "{typography.qualification-first-line}"
    width: "288px"
    height: "64px"
  qualification-tesda:
    textColor: "{colors.cyan}"
    typography: "{typography.qualification-first-line}"
    width: "288px"
    height: "64px"
---

# Design System: Reference Square GitHub Profile

## Overview

**Creative North Star: "Reference square frame"**

White and saturated square fields introduce Habib's identity through three complete orange, blue and purple variations. Smooth sans-serif lettering gives the name and WEB / DEVELOPER hierarchy the character of the user's named reference. A deep navy and white modular connection banner closes the reading sequence with all four social icons and labels in one continuous image, followed by a compact line of native text links.

The full experience renders in README.md. The primary reference governs the three identity compositions; the second reference governs the modular connection geometry. Authored self-contained SVG paths reproduce their abstract material while GitHub supplies native headings, highlighted prose and link behavior. The exact reference typeface is unknown; Open Sans is a licensed visual match.

**Key Characteristics:**

- Three saturated identity variations with full-banner fades.
- Smooth outlined sans-serif lettering throughout active SVG assets.
- Prominent phone identity above the decorative square field.
- One native GitHub column with all twelve technology modules in one wrapping group.
- Larger selectable About text and bold, underlined institution names.
- Stacked qualification titles with equally sized lines.
- One continuous connection image containing every social icon, with compact native links below.

## Colors

White and black establish the reference's light field and readable foreground. Orange, blue and purple form the identity banner's saturated fields; pale, middle and deep accents build the scattered square transitions. Blue mirrors the desktop fields. Purple uses white WEB / DEVELOPER lettering to preserve contrast.

Deep navy and white form the connection fields. Connection blue, cyan and indigo create the repeating modular edge. Facebook uses its blue tint (#1877f2), Instagram purple (#a236b4), GitHub black and the smooth authored email envelope cyan-blue (#168bbd). These brand-specific tints come from the connection builder.

Transparent technology modules expose GitHub's canvas. Attributed Devicon geometry retains available brand colors and the generator's flat display tints. Stack orange identifies BS Computer Science and cyan identifies NC III Web Development. Retained amber and lavender accents belong to unchanged logo/provenance inputs; there are no active category headings. GitHub owns the surrounding page theme and native text colors.

## Typography

Open Sans variable font is the build-time source for active SVG lettering, licensed under SIL OFL. FontTools instantiates the normal-width weight and converts real Bezier glyph outlines into paths. Browser rendering needs no font download, embedded font or raster lettering. Frontmatter sizes are generator inputs in SVG coordinates; responsive banners scale with displayed width, while technology and qualification images retain their declared dimensions.

The name and WEB roles are bold; identity subtitles, supporting hero copy and DEVELOPER are regular. Connection opening lines are bold, invitation and contact labels semibold, and supporting copy regular. Technology captions and both qualification lines use smooth semibold outlines. Native About and institution h3 elements rendered at 20px in the sanitized GitHub preview; strong plus ins preserves bold, underlined institution names. Those native sizes and margins are platform-controlled rather than an authored README stylesheet.

**The Native Text Rule.** Keep About facts and institution highlights in supported native HTML so they remain selectable and survive GitHub sanitization.

The exact screenshot face is not established. Use the matched Open Sans source without claiming exact identification. Dormant Silkscreen assets and their license remain retained legacy provenance.

## Layout

README.md uses one column: identity, About, one Tech Stack group, Education and Connection. One paragraph holds all twelve technology modules in their approved order. Sanitized previews show two columns at 320px and 375px, five at 768px and six at 1280px without shrinking modules. Each qualification title precedes a native highlighted institution h3.

Picture sources select mobile banners at 640px or below. Desktop identity places the name and WEB / DEVELOPER on opposite fields, mirrored in blue. Phone layouts keep the identity above the decorative square field. The connection desktop composition places four icons across the white field; phone places them in a two-by-two layout beneath the modular header, within one image. A centered native paragraph immediately below holds four text-only contact links. GitHub controls section spacing, typography and focus behavior.

**The Continuous Banner Rule.** Keep all four social icons in a single responsive image; place working native text links directly below it.

## Elevation & Depth

Active banners are flat. Overlapping rectangles, saturated fields and opacity create abstract depth. No shadows, gradients, blur or physical-material simulation are used. Three complete identity layers crossfade; individual squares do not drift independently.

## Shapes

Rectangular canvases, square identity scatter and rectangular connection modules define the visual language. Identity scatter divides each decorative field into eight rows; mobile applies it only to the lower field. The connection uses one navy/white ground with a repeating blue/cyan/indigo edge. Brand marks use attributed vector silhouettes; email uses smooth authored rounded-rectangle and envelope-line geometry.

## Components

### Identity variations

Orange and purple place identity left and WEB / DEVELOPER right; blue mirrors desktop fields. Phone identity stays above geometry in all states. Three full-banner layers run an eighteen-second loop, each holding five seconds and crossfading one second with ease-in-out interpolation. Reduced motion disables the animations and shows complete orange. Embedded SVG images provide no host callbacks for offscreen pausing or README hover controls.

### Native information sections

Supported h2 section headings and larger h3 About statements carry the profile facts. Quezon City University in About, Quezon City University in Education and TESDA in Education use strong plus ins. Exact approved text remains selectable. GitHub supplies the native typography, underline, spacing and link states.

### Unified technology modules

Each transparent local module places its logo viewport at x=40, y=10 and centered smooth label beginning at y=72. One paragraph contains all twelve fixed-size modules with meaningful alternatives. All technologies have attributed logos, including Java and VS Code. Native inline image layout supplies wrapping. Four earlier category-title assets remain generated but unused by README.md.

### Qualification blocks

Two transparent title images precede selectable, bold and underlined school/provider text. Orange reads BS COMPUTER / SCIENCE; cyan reads NC III / WEB DEVELOPMENT. Both smooth lines use the same qualification size and begin at y=4 and y=37. Alternatives carry full qualification names; no dates, proficiency or graduation claims are added.

### Continuous connection banner and links

Deep navy at left and white at right share a modular blue/cyan/indigo edge. The image reads LET'S / CONNECT and a useful-software invitation, with Facebook, Instagram, GitHub and Email icons and labels together. Desktop uses four icons across; phone uses two rows of two within the continuous image. Responsive picture sources choose the appropriate composition.

Four actual HTML text anchors immediately below preserve destinations and native keyboard focus. Image icons are illustrative rather than interactive image maps. Compact text links are explicitly user-approved; no custom touch-target size is claimed. Eight earlier contact slices remain generated for provenance but are unused by the active README.

## Do's and Don'ts

- Do retain the primary reference's orange, blue and purple compositions and mirrored blue fields.
- Do use smooth Open Sans Bezier outlines throughout active SVG lettering.
- Do preserve the complete orange reduced-motion fallback.
- Do keep all twelve technology modules together at their declared dimensions and let them wrap.
- Do keep About facts and highlighted school/provider names as native selectable text.
- Do keep every social icon inside one continuous connection image and four actual text links immediately below.
- Do retain attributed brand geometry, local font licenses and unchanged reference provenance.
- Don't assert the unknown screenshot typeface is exactly Open Sans.
- Don't add pixel typography, emojis, generated scenes, a cat or Featured Work to the active profile.
- Don't promise custom README CSS, SVG image-map links, hover controls or host-driven offscreen pausing.
- Don't introduce proficiency, dates or graduation claims.

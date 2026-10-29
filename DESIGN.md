---
name: Abstract Pixel GitHub Profile
description: Orange identity and blue modular connection banners framing a native GitHub profile.
colors:
  ground: "#0d1117"
  ink: "#edf2f7"
  orange: "#ff8a00"
  orange-light: "#ffb02e"
  orange-hot: "#ff6300"
  orange-deep: "#e34800"
  amber-light: "#ffc65a"
  amber: "#f99617"
  cyan: "#76d8f0"
  connection-ground: "#101c30"
  blue: "#3f83bf"
  blue-light: "#67c7ef"
  blue-deep: "#29437c"
  badge-ground: "#171c25"
  badge-orange: "#ff9d38"
  badge-purple: "#c5a0ef"
  badge-amber: "#f4cd70"
typography:
  display:
    fontFamily: "Silkscreen"
    fontSize: "48px"
    fontWeight: 400
  display-mobile-second-line:
    fontFamily: "Silkscreen"
    fontSize: "40px"
    fontWeight: 400
  identity:
    fontFamily: "Silkscreen"
    fontSize: "22px"
    fontWeight: 400
  connection:
    fontFamily: "Silkscreen"
    fontSize: "36px"
    fontWeight: 400
  caption:
    fontFamily: "Silkscreen"
    fontSize: "18px"
    fontWeight: 400
rounded:
  square: "0px"
components:
  hero:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    typography: "{typography.display}"
    rounded: "{rounded.square}"
    width: "1200px"
    height: "340px"
  hero-mobile:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    width: "600px"
    height: "360px"
  connection:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.cyan}"
    typography: "{typography.connection}"
    width: "1200px"
    height: "220px"
  connection-mobile:
    width: "600px"
    height: "240px"
  technology-badge:
    backgroundColor: "{colors.badge-ground}"
    height: "28px"
  contact-mark:
    width: "32px"
    height: "32px"
---

# Design System: Abstract Pixel GitHub Profile

## Overview

**Creative North Star: "Abstract pixel frame"**

Orange scattering squares introduce Habib's identity. Blue and cyan modular squares close the profile with a connection invitation. Crisp pixel lettering carries both banners; GitHub's own headings and readable prose carry the information between them.

The full experience renders in README.md. The supplied references determine the abstract composition and asymmetry. Self-contained SVG geometry adapts their light fields to the requested dark theme without embedding or editing stock JPEGs.

**Key Characteristics:**

- Orange square scatter beside the name.
- Blue modular square edge beside the connection invitation.
- Outlined pixel lettering with no remote font dependency.
- One native GitHub column and naturally wrapping badges.
- Separate mobile banner compositions.

## Colors

Warm orange shades form the hero's dense right field and separated square transition. Ink carries the name; cyan carries its subtitle. The connection banner combines a blue ground patch with blue, deep blue and cyan squares. Both SVGs use the ground token to blend into GitHub dark mode.

Technology badges retain their charcoal backgrounds and established orange, cyan, purple and amber logo colors. Contact marks retain their existing brand tints. GitHub supplies the surrounding page theme and native text colors.

## Typography

Silkscreen is the build-time source for banner lettering, licensed under SIL OFL. The generator converts bitmap glyph runs into SVG paths. No browser font download is required. Token sizes are generator input sizes in each SVG's coordinate system; displayed letters scale with the image width.

The desktop name uses 48px input type. Mobile splits HABIB and JAUDIAN D. into two lines at 48px and 40px. The cyan identity subtitle uses 22px. CONNECT uses 36px; the two-line invitation uses 18px. Native GitHub headings, samp labels and prose retain the platform's actual typography.

## Layout

README.md uses a single column. Its sequence is the hero, About, Tech Stack, Education, Connection and centered contacts. Twelve badges wrap within four technology groups. The education table contains two rows and two columns.

Picture sources select the mobile SVGs at a viewport width of 640px or below. Desktop hero and connection viewBoxes are 1200 x 340 and 1200 x 220. Mobile variants are 600 x 360 and 600 x 240. The images fill the available README width. GitHub determines outer spacing and native section margins.

## Elevation & Depth

The banners are flat. Square overlap, shade and opacity create the transition from solid color to the dark field. No shadow, gradient, blur or simulated physical material is used.

## Shapes

Rectangular canvases and exact square geometry define the banners. Desktop hero squares use a 48px grid; mobile uses 40px. Connection squares use 44px desktop and 40px mobile. Small separated hero squares provide a sparse animated accent.

## Components

### Identity banner

The name and subtitle sit in the dark left field. Orange occupies the right field and dissolves into squares toward the text. Three decorative desktop squares or two mobile squares drift vertically by 6px with an opacity change from 0.7 to 1 over a nine-second alternating ease-in-out cycle. A reduced-motion rule disables the animation. Lettering stays visible in every state.

### Native information sections

Supported HTML headings and prose carry the profile facts. GitHub owns their appearance and link states. No custom README stylesheet or standalone browser page is needed.

### Technology badges

Twelve Shields.io images use the service's for-the-badge format in Frontend, Backend, Database and Tools groups. Java and VS Code are text-only badges. Images carry meaningful alternatives.

### Education table

Two rows pair BS Computer Science with Quezon City University, and NC III Web Development with TESDA. Content wraps naturally on narrow screens.

### Connection banner and contacts

An asymmetric blue modular square edge occupies the left; cyan CONNECT and ink invitation text occupy the right. Four centered 32px local marks link to Facebook, Instagram, GitHub and email, with destination names in their alternatives.

## Do's and Don'ts

- Do keep each banner self-contained with outlined lettering and meaningful alternatives.
- Do preserve the supplied abstract square compositions and separate mobile layouts.
- Do keep profile facts as native selectable prose.
- Do keep decorative motion independent from content visibility and respect reduced motion.
- Don't introduce emojis or generated scene artwork.
- Don't restore the cat, Featured Work, missing placeholders or Pages links to this profile.
- Don't promise custom README CSS, fonts or hover controls that GitHub removes.

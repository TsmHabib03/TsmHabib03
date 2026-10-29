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
  lavender: "#c5a0ef"
  stack-amber: "#f4cd70"
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
  technology-label:
    fontFamily: "Silkscreen"
    fontSize: "14px"
    fontWeight: 400
  group-heading:
    fontFamily: "Silkscreen"
    fontSize: "20px"
    fontWeight: 400
  qualification-first-line:
    fontFamily: "Silkscreen"
    fontSize: "20px"
    fontWeight: 400
  qualification-second-line:
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
  technology-module:
    textColor: "{colors.ink}"
    typography: "{typography.technology-label}"
    width: "128px"
    height: "94px"
  technology-logo:
    width: "48px"
    height: "48px"
  group-frontend:
    textColor: "{colors.cyan}"
    typography: "{typography.group-heading}"
    width: "124px"
    height: "24px"
  group-backend:
    textColor: "{colors.orange}"
    typography: "{typography.group-heading}"
    width: "110px"
    height: "24px"
  group-database:
    textColor: "{colors.stack-amber}"
    typography: "{typography.group-heading}"
    width: "120px"
    height: "24px"
  group-tools:
    textColor: "{colors.lavender}"
    typography: "{typography.group-heading}"
    width: "75px"
    height: "24px"
  qualification-bscs:
    textColor: "{colors.orange}"
    typography: "{typography.qualification-first-line}"
    width: "264px"
    height: "48px"
  qualification-tesda:
    textColor: "{colors.cyan}"
    typography: "{typography.qualification-first-line}"
    width: "264px"
    height: "48px"
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
- One native GitHub column and independently wrapping logo groups.
- Transparent logo modules and stacked pixel qualification titles.
- Separate mobile banner compositions.

## Colors

Warm orange shades form the hero's dense right field and separated square transition. Ink carries the name; cyan carries its subtitle. The connection banner combines a blue ground patch with blue, deep blue and cyan squares. Both SVGs use the ground token to blend into GitHub dark mode.

Transparent technology modules expose the surrounding GitHub canvas. Cyan identifies Frontend, orange Backend, stack amber Database, and lavender Tools. Orange identifies the BS Computer Science title and cyan the NC III Web Development title. Logo geometry and available brand colors come from the attributed local Devicon sources, with the retained generator's flat rendering and display tints. Contact marks retain their existing brand tints. GitHub supplies the surrounding page theme and native text colors.

## Typography

Silkscreen is the build-time source for pixel lettering, licensed under SIL OFL. The generators use Pillow and the local font to convert bitmap glyph runs into SVG paths. Shipped SVG outputs embed no fonts, images or filters and make no network requests. Token sizes are generator input sizes in each SVG's coordinate system; banner lettering scales with the image width, while technology modules retain their declared dimensions.

The desktop name uses 48px input type. Mobile splits HABIB and JAUDIAN D. into two lines at 48px and 40px. The cyan identity subtitle uses 22px. CONNECT uses 36px; the two-line invitation uses 18px. Native GitHub headings, samp labels and prose retain the platform's actual typography.

Technology labels use the technology-label role, centered beneath each logo. Group headings use the group-heading role in transparent canvases with four group accents. Qualification titles use the first-line and second-line roles in two-line compositions. School and provider names remain native selectable prose.

## Layout

README.md uses a single column. Its sequence is the hero, About, Tech Stack, Education, Connection and centered contacts. Twelve fixed-size technology modules wrap independently within Frontend, Backend, Database and Tools paragraphs. Five Frontend modules and four Tools modules fit their desktop rows. Verified 320px and 375px captures show two columns without shrinking the logos or labels. Education uses two stacked qualification blocks, each followed by its native school or provider paragraph.

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

### Technology groups and modules

Local transparent SVG modules pair a centered logo viewport with an outlined pixel label. All twelve technologies have logos, including Java and VS Code. Logo viewports start at x=40, y=10 within each module; labels begin at y=72. Supported h3 elements contain local group-title SVGs; paragraph elements contain the fixed-size modules with meaningful alternatives. The open groups wrap through GitHub's native inline image layout, with no enclosing panel or custom README stylesheet.

### Qualification blocks

Two transparent title SVGs precede selectable school and provider prose. The orange title reads BS COMPUTER / SCIENCE; the cyan title reads NC III / WEB DEVELOPMENT. Their two outlined lines start at y=4 and y=30. The following paragraphs read Quezon City University and TESDA. Meaningful image alternatives carry the complete qualification names; no dates, proficiency or graduation claims are added.

### Connection banner and contacts

An asymmetric blue modular square edge occupies the left; cyan CONNECT and ink invitation text occupy the right. Four centered 32px local marks link to Facebook, Instagram, GitHub and email, with destination names in their alternatives.

## Do's and Don'ts

- Do keep each banner self-contained with outlined lettering and meaningful alternatives.
- Do preserve the supplied abstract square compositions and separate mobile layouts.
- Do keep profile facts as native selectable prose.
- Do keep technology modules at their declared dimensions and let each group wrap independently.
- Do retain attributed brand geometry and outlined pixel labels in transparent self-contained SVGs.
- Do keep decorative motion independent from content visibility and respect reduced motion.
- Don't introduce emojis or generated scene artwork.
- Don't restore the cat, Featured Work, missing placeholders or Pages links to this profile.
- Don't promise custom README CSS, fonts or hover controls that GitHub removes.

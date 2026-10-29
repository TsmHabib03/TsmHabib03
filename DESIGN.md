---
name: Tokyo Night Profile
description: A single black-cat city banner with a concise native GitHub profile.
colors:
  badge-background: "#1A1B26"
  frontend: "#7AA2F7"
  backend: "#BB9AF7"
  database: "#7DCFFF"
  tools: "#C0CAF5"
components:
  banner:
    width: "736px"
    height: "414px"
  technology-badge:
    height: "28px"
  contact-mark:
    width: "32px"
    height: "32px"
---

# Design System: Tokyo Night Profile

## Overview

One black cat watches a moonlit pixel city above a concise developer profile. The supplied image sets the midnight-blue and lavender atmosphere. A centered identity panel introduces Habib Jaudian D.; native About, Tech Stack, Education, and Contact sections carry the profile facts and destinations.

The current surface is [README.md](README.md), with its direction recorded in [.impeccable/surfaces/readme-md.md](.impeccable/surfaces/readme-md.md). Pinned GitHub repositories provide project discovery. This direction supersedes the earlier generated calico hero, three-cat Connect panorama, and Featured Projects section. Those assets and their generators remain available for compatibility.

GitHub owns the page background, typography, table border, spacing, and link states. The README uses supported HTML and Markdown, with no custom stylesheet, scripts, font overrides, or fabricated background attributes.

## Artwork and provenance

The only scene referenced by the README is [assets/readme/night-city-cat.jpg](assets/readme/night-city-cat.jpg), a 736 × 414 JPEG supplied by the user as 0ae95a03469fe58971c9c2577579e7d9.jpg. It shows one dark cat, an indigo skyline, and a lavender moon. No artwork was generated or visually edited; decoded pixels match the supplied source. A JPEG comment records its origin without recompressing the image. No creator attribution was supplied.

Source SHA-256: 14513d1b7db936bb0c65b7f30170df2ebcf1df79edf49cef8d38ddc129894acc.

Shipping SHA-256: 2652e77fadd3a4644d84628418c970e15a59bddd3b86a56c5b15614fb8a8ff5b.

The banner displays at the available column width and retains its 16:9 composition. It is static at every viewport, including reduced-motion settings. Its alternative describes the black cat and moonlit city; the person's name and qualification remain native text below the image.

## Color and typography

Shields.io technology badges use a #1A1B26 background with #7AA2F7 frontend, #BB9AF7 backend, #7DCFFF database, and #C0CAF5 tools logo accents. White labels retain the service's standard rendering. Java and VS Code use text-only badges. The artwork itself retains the supplied colors.

The name is a native H1, and BSCS · WEB DEVELOPER uses native inline code. Section and technology-group headings use H2 and H3. Body text and linked labels use GitHub's regular font. Text remains selectable, readable, and useful when artwork or badges do not load.

## Layout and content

The profile has one column. A full-width banner comes first, followed by a centered single-cell HTML table containing the name, qualification, short introduction, and Portfolio, Repositories, and Email links. The identity wraps naturally on narrow screens.

About contains the supplied sentence “Building useful software, one project at a time.” and the Computer Science background at Quezon City University. Tech Stack has four unnumbered groups: Frontend (HTML, CSS, JavaScript, Tailwind CSS, Bootstrap), Backend (PHP, Java), Database (MySQL), and Tools (Git, GitHub, Docker, VS Code). Badge rows wrap through normal inline layout.

Education records BS Computer Science at Quezon City University and NC III Web Development at TESDA. Contact uses centered, individually linked Portfolio, GitHub, LinkedIn, and Email labels with 32px local marks. Two short centered rows fit narrow screens; nonbreaking spaces join each icon to its label. Decorative contact marks have empty alternatives because their adjacent labels name each destination.

The LinkedIn destination is the owner-listed https://www.linkedin.com/in/habib-jaudian-661a9a424/. No achievements, employers, adoption claims, or additional learning priorities are inferred.

## Verification

GitHub's Markdown API sanitized the current composition; that returned HTML was rendered locally with the open-source github-markdown-css stylesheet. Checks cover 320px, 375px, and 1280px widths, loaded images, readable wrapping, accessible linked labels, and page/table overflow. The twelve Shields.io responses were also retrieved successfully. The finish report and screenshots are in the ignored .impeccable/review/simple-black-cat/ directory.

This verifies a local preview of GitHub-sanitized HTML. It does not establish that this version has been published to the live GitHub profile. GitHub controls its final styling and image caching.

## Retained generators

The Python artwork tools remain available for earlier SVG scenes and compact marks. The --profile-only option of scripts/generate-profile-assets.py produces the retained set of 28 rooftop assets and icons; it does not generate the supplied JPEG or technology badges. The --hero-only option produces the four legacy heroes, and the full command also generates older sections, project strips, footers, accents, and labeled icons.

Contribution images and their refresh workflow remain optional and unreferenced by the README. They use verified GitHub data and display snapshot dates. Run python -m unittest discover -s tests -v to check current README references, retained artwork contracts, and contribution integrity. Asset provenance and regeneration commands are documented in [assets/README.md](assets/README.md).

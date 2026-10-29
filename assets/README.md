# Profile assets

[README.md](../README.md) renders the entire profile directly on GitHub. Three fading identity variations introduce About, twelve transparent technology modules and two stacked qualifications. A modular connection banner contains four independently linked contact slices inside its table boundary.

| Asset | Display | Source |
| --- | --- | --- |
| `readme/profile-banner.svg` | 1200 x 384 identity banner | Authored orange (#ff8000), blue (#4098f3) and purple (#a000d9) square-field variations with smooth Open Sans outlines; blue mirrors the desktop fields |
| `readme/profile-banner-mobile.svg` | 600 x 400 phone identity banner | Prominent identity above decorative geometry in all three variations |
| `readme/connect-banner.svg` | 1200 x 220 connection header | Navy (#080b1a)/white fields and modular blue (#468cc8), cyan (#66c9f3), indigo (#394586) rectangles inspired by reference 2 |
| `readme/connect-banner-mobile.svg` | 600 x 160 phone connection header | Separate narrow-screen composition |
| `readme/connect-{facebook,instagram,github,email}.svg` | Four 600 x 170 desktop slices; 56px icon canvases and 27px smooth labels before responsive scaling | Attributed contact mark inputs; smooth authored email geometry; each image has a separate actual HTML link |
| `readme/connect-{facebook,instagram,github,email}-mobile.svg` | Four 600 x 300 phone slices; 140px icon canvases and 64px labels before responsive scaling | Larger contact canvas treatment inside the same two-column/two-row boundary |
| `fonts/open-sans-variable.ttf` | Build-time source for smooth real Bezier lettering | Open Sans variable font; [SIL OFL license](fonts/OFL-open-sans.txt). The exact screenshot face is unknown; this is a matched sans-serif |
| `readme/tech-*.svg` | Twelve transparent 128 x 94px modules; 48 x 48px logo viewports and 14px smooth outlined labels | Attributed local Devicon geometry: HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `readme/heading-*.svg` | Four 24px-high transparent canvases with 20px outlined group names | Frontend cyan (#76d8f0), Backend orange (#ff8a00), Database amber (#f4cd70), Tools lavender (#c5a0ef) |
| `readme/education-bscs.svg`, `readme/education-tesda.svg` | Two transparent 264 x 48px qualification title images; first line 20px, second line 18px | Orange BS COMPUTER / SCIENCE and cyan NC III / WEB DEVELOPMENT; school/provider remain native README prose |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Retained contact mark inputs | Attributed brand geometry; the active connection builder supplies smooth email geometry |

[scripts/build-readme-banners.py](../scripts/build-readme-banners.py) creates responsive identity banners, connection headers and eight contact slices. FontTools instantiates the local Open Sans variable face at normal width and converts real Bezier glyph outlines into paths. FontTools, the local font and Pillow used by retained generators are build-time dependencies only. No font or raster is embedded. The exact reference face is unknown; Open Sans is a licensed match. The identity runs an eighteen-second loop with three five-second holds and one-second full-banner fades. Reduced motion shows complete orange. No individual square drift, README hover control or host-driven offscreen pause is promised.

[scripts/build-readme-stack.py](../scripts/build-readme-stack.py) creates the twelve logo modules, four group headings and two qualification title images. It reuses the banner generator's smooth Open Sans outlines and the retained profile generator's attributed icon symbols. Logo viewports begin at x=40, y=10 and labels at y=72 within the modules. Group headings and qualification titles retain their orange, cyan, amber and lavender accents. These transparent SVG outputs contain no embedded fonts, images, filters or network dependencies. GitHub wraps each technology group independently; modules retain their declared size. No pixel font remains in the active README, including its native section headings.

The connection header spans a table's first row; two rows of independently linked slices follow within that boundary. Facebook, Instagram, GitHub and Email retain their actual HTML destinations and native keyboard focus. Native GitHub table borders and padding create visible seams. Contacts are not interactive links inside one SVG and the slices are not seamless.

The supplied `330982eb338215bfe1379446458b8802.jpg` and `789c8708e57ef4b55ea26df089f2bcee.jpg` are composition references, retained as `readme/orange-reference.jpg` and `readme/modular-reference.jpg`. Their decoded pixels, sample text and watermarks remain unchanged. Origins and hashes are in [reference-provenance.json](readme/reference-provenance.json). No scene artwork was generated and no new raster is used by the README.

Parent-validated GitHub Markdown API-sanitized output was checked at 320px, 375px and 1280px: correct responsive SVG selection, independent logo-group wrapping, no broken images and no page overflow. Narrow captures show two columns without shrinking logos or labels; desktop shows five Frontend and four Tools modules across. All three variations, midpoint fades, reduced motion, four correct destinations, keyboard focus and targets of at least 44px were verified. All 23 relevant tests pass, detector returned [], and contribution data is unchanged. The fresh reviewer returned ship with no implementation fixes; the current documentation refresh completes its pending documentation obligation. Evidence is in the ignored `.impeccable/review/profile-readme/` directory.

## Retained assets

Earlier city/cat scenes, project strips, original reference JPEGs and contribution assets remain for their existing generators and attribution history. The corrected README does not reference the cat, project strips or legacy scenes. Contribution data and refresh files remain unchanged by this revision.

The dormant `fonts/silkscreen-latin.ttf` and [OFL-silkscreen.txt](fonts/OFL-silkscreen.txt) remain for legacy generators and provenance. Active README lettering uses Open Sans. The supplied reference JPEGs remain unchanged and no new raster asset is generated or used by the README.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets and contribution integrity.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) and [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) and [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. The README stack uses Devicon geometry through `icon_symbol(..., flat=True)` in the retained profile generator; this removes gradients and filters while preserving the upstream silhouettes. Available brand colors are retained, with display tints defined by `BRAND_TINT` where applicable. Retained portfolio and email mark files contain authored pixel geometry; the active connection builder replaces its email input with smooth authored envelope geometry. Other contact inputs use the attributed sources above.

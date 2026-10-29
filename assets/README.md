# Profile assets

[README.md](../README.md) renders the whole profile directly on GitHub. Three fading identity variations introduce larger native About text, one group of twelve technology modules and two highlighted qualifications. One continuous connection image contains every social icon and label; a compact native text-link line below provides the destinations.

| Asset | Display | Source |
| --- | --- | --- |
| `readme/profile-banner.svg` | 1200 x 384 identity | Authored orange (#ff8000), blue (#4098f3) and purple (#a000d9) square fields with smooth Open Sans outlines; blue mirrors desktop fields |
| `readme/profile-banner-mobile.svg` | 600 x 400 phone identity | Prominent identity above decorative geometry in all three variations |
| `readme/connect-banner.svg` | One 1200 x 310 connection image; four 72px icon canvases and 25px labels | Navy (#080b1a)/white fields with modular blue (#468cc8), cyan (#66c9f3) and indigo (#394586); Facebook, Instagram, GitHub and Email together |
| `readme/connect-banner-mobile.svg` | One 600 x 440 phone connection image; 80px icon canvases and 30px labels | Modular header above four contacts in a two-by-two layout inside one image |
| `readme/tech-*.svg` | Twelve transparent 128 x 94px modules; 48px logos and 14px outlined labels | Attributed Devicon geometry: HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `readme/education-bscs.svg`, `readme/education-tesda.svg` | Two transparent 288 x 64px titles; both lines 24px | Orange BS COMPUTER / SCIENCE and cyan NC III / WEB DEVELOPMENT; highlighted institutions remain native README text |
| `fonts/open-sans-variable.ttf` | Build-time smooth Bezier lettering source | Open Sans variable font; [SIL OFL license](fonts/OFL-open-sans.txt). Exact screenshot face is unknown; this is a visual match |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Retained contact inputs | Attributed brand geometry; connection builder supplies smooth authored email geometry |
| `readme/connect-{facebook,instagram,github,email}.svg`, corresponding `-mobile.svg` | Eight previous contact slices, retained unused | Existing generator/provenance outputs; absent from the active README |
| `readme/heading-*.svg` | Four previous category titles, retained unused | Existing Frontend, Backend, Database and Tools outputs; absent from the active README |

[scripts/build-readme-banners.py](../scripts/build-readme-banners.py) creates responsive identity and continuous connection banners and retains eight previous slices. FontTools instantiates Open Sans at normal width and converts glyph outlines into paths. Local font, FontTools and retained Pillow dependencies are build-time only. No raster or font is embedded. Identity uses an eighteen-second loop with three five-second holds and one-second full-banner fades; reduced motion shows complete orange.

The connection builder places all four contacts inside each responsive banner. Facebook uses #1877f2, Instagram #a236b4, GitHub #232323 and smooth authored email #168bbd. A single picture element chooses the composition at 640px. Four centered text-only HTML links immediately below provide destinations and native keyboard focus. Banner icons are illustrative. No table, separate linked contact images or image-map interaction is used.

[scripts/build-readme-stack.py](../scripts/build-readme-stack.py) creates twelve modules, two enlarged qualification titles and retained unused category headings. Logo viewports begin at x=40, y=10 and labels at y=72; qualification lines begin at y=4 and y=37. One README paragraph wraps all technologies. Native h3 elements enlarge About and institution names; strong plus ins highlights QCU and TESDA. Transparent SVGs contain no embedded fonts, images, filters or network dependencies.

The supplied JPEGs remain `readme/orange-reference.jpg` and `readme/modular-reference.jpg`. Decoded pixels, sample text and watermarks are unchanged; origins and hashes are in [reference-provenance.json](readme/reference-provenance.json). No scene artwork or new raster was generated or used by README.md.

Fresh GitHub Markdown API-sanitized captures at 320px, 375px, 768px and 1280px show no broken images or overflow. Modules stay 128 x 94px, wrapping in two, five and six columns. About/institution text is 20px in the preview; bold/underline survives sanitization. Four exact destinations and keyboard focus were verified. All 23 tests pass, detector returned [], and hero source and contribution data are unchanged. Fresh review returned ship with no implementation fixes; documentation completes its pending obligation. Current evidence is in ignored `.impeccable/review/profile-readme/unified/`; earlier accepted motion evidence supports unchanged hero behavior.

## Retained assets

Earlier city/cat scenes, project strips, original reference JPEGs and contribution assets remain for their existing generators and attribution history. The corrected README does not reference the cat, project strips or legacy scenes. Contribution data and refresh files remain unchanged by this revision.

The dormant `fonts/silkscreen-latin.ttf` and [OFL-silkscreen.txt](fonts/OFL-silkscreen.txt) remain for legacy generators and provenance. Active README lettering uses Open Sans. The supplied reference JPEGs remain unchanged and no new raster asset is generated or used by the README.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets and contribution integrity.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) and [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) and [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. The README stack uses Devicon geometry through `icon_symbol(..., flat=True)` in the retained profile generator; this removes gradients and filters while preserving the upstream silhouettes. Available brand colors are retained, with display tints defined by `BRAND_TINT` where applicable. Retained portfolio and email mark files contain authored pixel geometry; the active connection builder replaces its email input with smooth authored envelope geometry. Other contact inputs use the attributed sources above.

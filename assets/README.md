# Profile assets

[README.md](../README.md) renders the whole profile directly on GitHub. A stationary identity beside a coded rotating geographic globe leads one group of twelve technology modules and two highlighted qualifications. One continuous connection image contains every social icon and label; a compact native text-link line below provides the destinations. About was removed by the approved redesign.

| Asset | Display | Source |
| --- | --- | --- |
| `readme/profile-globe.gif` | 1200 x 320 desktop identity; 2,945,664 bytes | White 670px identity field and blue 530px globe field; coded geographic rotation, stationary Geist/Geist Mono identity and supplied marks |
| `readme/profile-globe-mobile.gif` | 600 x 440 phone identity; 1,832,857 bytes | 220px white identity above a 220px globe field |
| `readme/profile-globe-still.png`, `readme/profile-globe-mobile-still.png` | Complete desktop/phone reduced-motion frames | First-frame code render with embedded source/generation provenance |
| `readme/habib-favicon.png`, `readme/habib-logo.svg` | Supplied favicon and Bitstream h geometry | Habib-owned brand inputs; h rendered as approved white variant on blue |
| `readme/globe-source/ne_110m_land.geojson` | Build-time geographic coordinates | Natural Earth public-domain land polygons; source/license URLs in [globe-provenance.json](readme/globe-provenance.json) |
| `fonts/geist-variable.ttf`, `fonts/geist-mono-variable.ttf` | Build-time identity lettering | Geist/Geist Mono; local OFL licenses. Supported reference match, exact JPEG face unconfirmed |
| `readme/connect-banner.gif` | Active 1200 x 240 desktop footer; 56,989 bytes | Electric blue (#001aff), cool pale (#eef2fe), white social silhouettes; one three-second pixel-edge ripple |
| `readme/connect-banner-mobile.gif` | Active 600 x 320 phone footer; 50,117 bytes | Invitation above two rows of two contacts; same bounded motion |
| `readme/connect-banner-still.png`, `readme/connect-banner-mobile-still.png` | Complete reduced-motion footer frames; 35,425 / 34,644 bytes | Resting edge and stationary Gruppo/Geist lettering; embedded provenance |
| `fonts/gruppo-regular.ttf` | Footer display lettering | Licensed visual match for thin rounded reference capitals; [SIL OFL license](fonts/OFL-gruppo.txt); exact reference font unconfirmed |
| `readme/connect-banner.svg` | Legacy 1200 x 310 connection image, retained unused | Earlier navy/white modular fields; absent from active README |
| `readme/connect-banner-mobile.svg` | Legacy 600 x 440 phone connection image, retained unused | Earlier modular two-by-two composition; absent from active README |
| `readme/tech-*.svg` | Twelve transparent 128 x 94px modules; 48px logos and 14px outlined labels | Attributed Devicon geometry: HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `readme/education-bscs.svg`, `readme/education-tesda.svg` | Two transparent 288 x 64px titles; both lines 24px | Orange BS COMPUTER / SCIENCE and cyan NC III / WEB DEVELOPMENT; highlighted institutions remain native README text |
| `fonts/open-sans-variable.ttf` | Build-time smooth Bezier lettering for existing SVG components | Open Sans variable font; [SIL OFL license](fonts/OFL-open-sans.txt) |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Retained contact inputs | Attributed brand geometry; connection builder supplies smooth authored email geometry |
| `readme/profile-banner*.svg` | Legacy square identity outputs, retained unused | Earlier orange/blue/purple Open Sans compositions and reduced-motion alternatives; absent from active README |
| `readme/connect-{facebook,instagram,github,email}.svg`, corresponding `-mobile.svg` | Eight previous contact slices, retained unused | Existing generator/provenance outputs; absent from active README |
| `readme/heading-*.svg` | Four previous category titles, retained unused | Existing Frontend, Backend, Database and Tools outputs; absent from active README |

[scripts/build-globe-banner.py](../scripts/build-globe-banner.py) renders staggered open-ring land points through a rotating orthographic projection. The supplied JPEG and MP4 are local design/motion references; no video frames ship. Desktop/phone GIFs loop one full rotation over 150 frames in exactly ten seconds, averaging 15 fps with 70/60/70ms delays. Geist name inputs are 68px desktop/60px phone at weight 600. Geist Mono role is 27px/23px, university 23px/18px and handle 19px, weight 400. Identity lettering, favicon and h stay still. Fixed palette entries preserve exact white, identity ink (#0a0a0a), reference blue (#2b4ff7) and brand blue (#5b6ef5).

Rebuild with `python -m pip install -r scripts/requirements-globe.txt`, then `python scripts/build-globe-banner.py`. Local fonts, Natural Earth geometry, Pillow, NumPy and Shapely are build-time inputs. [globe-provenance.json](readme/globe-provenance.json) records source URLs, licenses, frame duration and output hashes. All six shipping rasters carry embedded provenance. Reduced-motion PNG sources come first in the README picture; responsive phone selection is at 640px. GitHub renders the GIF directly without a Pages deployment.

[scripts/build-readme-banners.py](../scripts/build-readme-banners.py) creates the retained unused modular connection SVGs and retains earlier square identity outputs and eight contact slices. FontTools instantiates Open Sans at normal width and converts glyph outlines into paths. Local font, FontTools and retained Pillow dependencies are build-time only. These SVGs embed no raster or font. The old square identity eighteen-second fades and complete orange fallback remain legacy behavior, unused by the active README.

[scripts/build-connect-footer.py](../scripts/build-connect-footer.py) builds the active pixel footer from code. Rebuild with `python -m pip install -r scripts/requirements-footer.txt`, `python -m playwright install chromium`, then `python scripts/build-connect-footer.py`. Pillow draws licensed local Gruppo Regular (68px desktop / 64px phone) and Geist Regular (support 23px / 26px; labels 22px / 25px), while build-time Chromium rasterizes attributed social SVG silhouettes. Icon canvases are 48px desktop / 38px phone. No runtime browser or font download is needed in the README.

The blue/pale boundary uses 12px desktop or 10px phone cells and sparse crosshairs. Forty-five authored frames total exactly 3,000ms; optimization merges identical frames. The GIF has no loop extension and rests on its original boundary. Text and icons remain still. [footer-provenance.json](readme/footer-provenance.json) records the supplied local design reference, font/icon sources, output hashes, bytes and bounded motion. The reference JPEG is a design input; none of its pixels ship. All four footer rasters carry origin metadata.

One picture element selects the phone footer at 640px and gives reduced-motion PNG sources first priority. Four centered native text links immediately below provide destinations and keyboard focus. Banner icons are illustrative. The existing modular connection SVGs and their generator remain unused historical assets.

[scripts/build-readme-stack.py](../scripts/build-readme-stack.py) creates twelve modules, two qualification titles and retained unused category headings. Logo viewports begin at x=40, y=10 and labels at y=72; qualification lines begin at y=4 and y=37. One README paragraph wraps all technologies. Native h3 elements with strong plus ins highlight QCU and TESDA in Education. Transparent SVGs contain no embedded fonts, images, filters or network dependencies.

The earlier supplied JPEGs remain `readme/orange-reference.jpg` and `readme/modular-reference.jpg`. Decoded pixels, sample text and watermarks are unchanged; origins and hashes are in [reference-provenance.json](readme/reference-provenance.json). The new supplied identity JPEG and MP4 are local review inputs; their filenames and roles are recorded in globe provenance.

2026-11-22: GitHub Markdown API-sanitized browser checks at 320px, 390px, 768px and 1440px report loaded GIFs, no overflow and correct reduced-motion PNG selection. Eight captures cover animated and reduced states. The implementation handoff records all 25 tests passing, detector [] and zero rasters missing provenance. The final local verdict record (`.impeccable/review/globe-banner/verdict-review.md`) confirms the scored GIF-ground fix: exact white in refreshed captures and all 150 decoded frames of both GIFs, eight valid recaptures and no fix-induced regressions. Its ship disposition applies to that fix. Contribution data and lower sections are unchanged; live publication is not established by these local checks.

## Retained assets

Earlier city/cat scenes, project strips, square identity SVGs, original reference JPEGs and contribution assets remain for their existing generators and attribution history. The active README does not reference the cat, project strips or legacy scenes. Contribution data and refresh files remain unchanged by this revision.

The dormant `fonts/silkscreen-latin.ttf` and [OFL-silkscreen.txt](fonts/OFL-silkscreen.txt) remain for legacy generators and provenance. Active identity rasters use Geist/Geist Mono; active technology and qualification SVGs retain Open Sans outlines. Active footer rasters use Gruppo/Geist.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets and contribution integrity.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) and [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) and [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. The README stack uses Devicon geometry through `icon_symbol(..., flat=True)` in the retained profile generator; this removes gradients and filters while preserving the upstream silhouettes. Available brand colors are retained, with display tints defined by `BRAND_TINT` where applicable. Retained portfolio and email mark files contain authored pixel geometry; the active connection builder replaces its email input with smooth authored envelope geometry. Other contact inputs use the attributed sources above.


2026-11-22 compact-height refinement: the user requested a shorter GitHub hero. Desktop is now 1200 x 320 (53% less height) and phone is 600 x 440 (42% less height), with type sizes preserved and the complete globe fitting each blue field. The current eight local animated/reduced captures at 320px, 390px, 768px and 1440px show loaded assets, no overflow and correct PNG selection. All 25 tests pass; the single detector scan returned [] and provenance scan found 6 rasters, 0 missing. Delegated review task payloads were omitted, so the compact finish review was substituted using the degraded reviewer contract and records disposition: ship for this rendered refinement. This evidence is separate from the historical white-ground fix and prior live deployment. The compact publication is pending the subsequent publish step.


2026-11-22 footer checks: all 26 tests pass; GFM-sanitized previews at 320, 390, 768 and 1440px confirm responsive loading, visible bounded motion, rest, reduced PNGs, no overflow and all four keyboard-focusable links. The single footer detector returned []; scan found 8 rasters, 0 missing provenance, with GIF comments checked separately.

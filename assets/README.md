# Profile assets

[README.md](../README.md) renders the whole profile directly on GitHub. A stationary identity beside a coded rotating geographic globe leads one group of twelve technology modules and two highlighted qualifications. One continuous connection image contains every social icon and label; a compact native text-link line below provides the destinations. About was removed by the approved redesign.

| Asset | Display | Source |
| --- | --- | --- |
| `readme/profile-globe.gif` | 1200 x 675 desktop identity; 6,906,536 bytes | White 670px identity field and blue 530px globe field; coded geographic rotation, stationary Geist/Geist Mono identity and supplied marks |
| `readme/profile-globe-mobile.gif` | 600 x 760 phone identity; 5,539,054 bytes | 300px white identity above a 460px globe field |
| `readme/profile-globe-still.png`, `readme/profile-globe-mobile-still.png` | Complete desktop/phone reduced-motion frames | First-frame code render with embedded source/generation provenance |
| `readme/habib-favicon.png`, `readme/habib-logo.svg` | Supplied favicon and Bitstream h geometry | Habib-owned brand inputs; h rendered as approved white variant on blue |
| `readme/globe-source/ne_110m_land.geojson` | Build-time geographic coordinates | Natural Earth public-domain land polygons; source/license URLs in [globe-provenance.json](readme/globe-provenance.json) |
| `fonts/geist-variable.ttf`, `fonts/geist-mono-variable.ttf` | Build-time identity lettering | Geist/Geist Mono; local OFL licenses. Supported reference match, exact JPEG face unconfirmed |
| `readme/connect-banner.svg` | One 1200 x 310 connection image; four 72px icon canvases and 25px labels | Navy (#080b1a)/white fields with modular blue (#468cc8), cyan (#66c9f3) and indigo (#394586); Facebook, Instagram, GitHub and Email together |
| `readme/connect-banner-mobile.svg` | One 600 x 440 phone connection image; 80px icon canvases and 30px labels | Modular header above four contacts in a two-by-two layout inside one image |
| `readme/tech-*.svg` | Twelve transparent 128 x 94px modules; 48px logos and 14px outlined labels | Attributed Devicon geometry: HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `readme/education-bscs.svg`, `readme/education-tesda.svg` | Two transparent 288 x 64px titles; both lines 24px | Orange BS COMPUTER / SCIENCE and cyan NC III / WEB DEVELOPMENT; highlighted institutions remain native README text |
| `fonts/open-sans-variable.ttf` | Build-time smooth Bezier lettering for existing SVG components | Open Sans variable font; [SIL OFL license](fonts/OFL-open-sans.txt) |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Retained contact inputs | Attributed brand geometry; connection builder supplies smooth authored email geometry |
| `readme/profile-banner*.svg` | Legacy square identity outputs, retained unused | Earlier orange/blue/purple Open Sans compositions and reduced-motion alternatives; absent from active README |
| `readme/connect-{facebook,instagram,github,email}.svg`, corresponding `-mobile.svg` | Eight previous contact slices, retained unused | Existing generator/provenance outputs; absent from active README |
| `readme/heading-*.svg` | Four previous category titles, retained unused | Existing Frontend, Backend, Database and Tools outputs; absent from active README |

[scripts/build-globe-banner.py](../scripts/build-globe-banner.py) renders staggered open-ring land points through a rotating orthographic projection. The supplied JPEG and MP4 are local design/motion references; no video frames ship. Desktop/phone GIFs loop one full rotation over 150 frames in exactly ten seconds, averaging 15 fps with 70/60/70ms delays. Geist name inputs are 68px desktop/60px phone at weight 600. Geist Mono role is 27px/23px, university 23px/18px and handle 19px, weight 400. Identity lettering, favicon and h stay still. Fixed palette entries preserve exact white, identity ink (#0a0a0a), reference blue (#2b4ff7) and brand blue (#5b6ef5).

Rebuild with `python -m pip install -r scripts/requirements-globe.txt`, then `python scripts/build-globe-banner.py`. Local fonts, Natural Earth geometry, Pillow, NumPy and Shapely are build-time inputs. [globe-provenance.json](readme/globe-provenance.json) records source URLs, licenses, frame duration and output hashes. All six shipping rasters carry embedded provenance. Reduced-motion PNG sources come first in the README picture; responsive phone selection is at 640px. GitHub renders the GIF directly without a Pages deployment.

[scripts/build-readme-banners.py](../scripts/build-readme-banners.py) creates the unchanged continuous connection banners and retains earlier square identity outputs and eight contact slices. FontTools instantiates Open Sans at normal width and converts glyph outlines into paths. Local font, FontTools and retained Pillow dependencies are build-time only. These SVGs embed no raster or font. The old square identity eighteen-second fades and complete orange fallback remain legacy behavior, unused by the active README.

The connection builder places all four contacts inside each responsive banner. Facebook uses #1877f2, Instagram #a236b4, GitHub #232323 and smooth authored email #168bbd. A single picture element chooses the composition at 640px. Four centered text-only HTML links immediately below provide destinations and native keyboard focus. Banner icons are illustrative. No table, separate linked contact images or image-map interaction is used.

[scripts/build-readme-stack.py](../scripts/build-readme-stack.py) creates twelve modules, two qualification titles and retained unused category headings. Logo viewports begin at x=40, y=10 and labels at y=72; qualification lines begin at y=4 and y=37. One README paragraph wraps all technologies. Native h3 elements with strong plus ins highlight QCU and TESDA in Education. Transparent SVGs contain no embedded fonts, images, filters or network dependencies.

The earlier supplied JPEGs remain `readme/orange-reference.jpg` and `readme/modular-reference.jpg`. Decoded pixels, sample text and watermarks are unchanged; origins and hashes are in [reference-provenance.json](readme/reference-provenance.json). The new supplied identity JPEG and MP4 are local review inputs; their filenames and roles are recorded in globe provenance.

2026-11-22: GitHub Markdown API-sanitized browser checks at 320px, 390px, 768px and 1440px report loaded GIFs, no overflow and correct reduced-motion PNG selection. Eight captures cover animated and reduced states. The implementation handoff records all 25 tests passing, detector [] and zero rasters missing provenance. The final local verdict record (`.impeccable/review/globe-banner/verdict-review.md`) confirms the scored GIF-ground fix: exact white in refreshed captures and all 150 decoded frames of both GIFs, eight valid recaptures and no fix-induced regressions. Its ship disposition applies to that fix. Contribution data and lower sections are unchanged; live publication is not established by these local checks.

## Retained assets

Earlier city/cat scenes, project strips, square identity SVGs, original reference JPEGs and contribution assets remain for their existing generators and attribution history. The active README does not reference the cat, project strips or legacy scenes. Contribution data and refresh files remain unchanged by this revision.

The dormant `fonts/silkscreen-latin.ttf` and [OFL-silkscreen.txt](fonts/OFL-silkscreen.txt) remain for legacy generators and provenance. Active identity rasters use Geist/Geist Mono; active technology, qualification and connection SVGs retain Open Sans outlines.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets and contribution integrity.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) and [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) and [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. The README stack uses Devicon geometry through `icon_symbol(..., flat=True)` in the retained profile generator; this removes gradients and filters while preserving the upstream silhouettes. Available brand colors are retained, with display tints defined by `BRAND_TINT` where applicable. Retained portfolio and email mark files contain authored pixel geometry; the active connection builder replaces its email input with smooth authored envelope geometry. Other contact inputs use the attributed sources above.

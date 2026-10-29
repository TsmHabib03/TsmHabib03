# Profile assets

The current [README.md](../README.md) is a raw GitHub template with six sections, project cards, twelve Shields.io badges, and a city/cat footer. [profile.html](../profile.html) and [profile.css](../profile.css) supply the custom pixel font, dark banner crop, overlay text, hover transition, and three CSS motion options. GitHub strips those CSS capabilities.

| Asset | Source and display | Provenance |
| --- | --- | --- |
| `readme/orange-pixel-banner.jpg` | Explicit README placeholder, not a shipped file | Replace with a single orange banner; supplied references contain multiple samples |
| `readme/orange-reference.jpg` | Supplied 626 x 626 collage; companion CSS shows abstract pixels from the first sample | `330982eb338215bfe1379446458b8802.jpg`; decoded pixels unchanged |
| `readme/modular-reference.jpg` | Supplied 1000 x 1000 reference, retained for comparison | `789c8708e57ef4b55ea26df089f2bcee.jpg`; original sample text and watermarks retained |
| `readme/night-city-cat.jpg` | Supplied 736 x 414 image at footer, full column width | `0ae95a03469fe58971c9c2577579e7d9.jpg`; decoded pixels unchanged |
| `fonts/silkscreen-latin.ttf` | Self-hosted companion display face | Google Fonts Silkscreen; license beside file |
| Shields.io badges | Twelve external SVG badges at service height | HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Existing local contact marks, displayed at 32px | Devicon/Simple Icons sources and authored email geometry; attribution below |

No scene artwork was generated. JPEG origin comments were added without recompression or pixel changes. Origins and hashes are in [readme/provenance.json](readme/provenance.json) and [readme/reference-provenance.json](readme/reference-provenance.json). The source images' creator attribution was not supplied.

Badge backgrounds use the charcoal panel token. Logo colors follow the orange, cyan, lavender, amber and mint palette in [DESIGN.md](../DESIGN.md). Java and VS Code are text-only badges. README contact alternatives name each destination; companion icons have native linked labels.

The API repository destination remains an explicit placeholder after the proposed URL returned 404. ASJ Attendance Checker is the assumed full-stack selection, not a confirmed user preference. QCU and ASJ links were verified.

Local GitHub Markdown API-sanitized previews and the companion were checked at 320px, 375px, and 1280px, including image/font loading, no page/table overflow, keyboard focus, radio motion selections, and reduced-motion behavior. All 22 tests passed. Evidence lives in the ignored `.impeccable/review/orange-pixel/` folder. The README hero is the one intentionally unfilled image placeholder. The user authorized publishing this revision; `.github/workflows/publish-profile.yml` deploys the companion to https://tsmhabib03.github.io/TsmHabib03/ with only its referenced assets.

## Retained SVG artwork

Earlier generated heroes, section banners, project strips and contribution assets remain available but are unreferenced by the new README and companion. The existing generator supports legacy full generation, `--hero-only`, and `--profile-only`. The compact email mark's fill order was corrected to keep its pixel envelope fold visible. Do not regenerate scene artwork as part of this code-only revision.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets, and contribution integrity. Contribution refresh files remain unchanged by this revision.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) · [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) · [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. Display tints are defined by `BRAND_TINT` in the profile generator. The portfolio and email marks are authored pixel geometry; the other compact marks use the attributed sources above.

## Project sources

Public repository languages and README stack descriptions were checked on 2026-09-28:

- [QCU Schedule](https://github.com/TsmHabib03/QCU-Schedule-Web-App): student schedule platform. HTML, CSS, JavaScript (repository language data).
- [ASJ Attendance Checker](https://github.com/TsmHabib03/ASJ-Attendance-Checker): QR attendance and role-based dashboards. PHP, MySQL, JavaScript (README).
- [RepCore Fitness](https://github.com/TsmHabib03/Repcorefitness): membership and attendance workflows. PHP, MySQL, JavaScript (README).
- [Manila City Council HRIS](https://github.com/TsmHabib03/Manila-City-Council-HRIS): employee records and leave management. Java, Spring Boot, MySQL (README).

No employment, client relationship, adoption, or expert-level claims are inferred from repository names.

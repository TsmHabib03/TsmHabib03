# Profile assets

## Current README

The profile uses one user-supplied static black-cat city banner, twelve Shields.io technology badges, and four local contact marks. GitHub provides the surrounding page styles and native text. The approved composition and verification limits are recorded in [DESIGN.md](../DESIGN.md).

| Asset | Source and display | Provenance |
| --- | --- | --- |
| `readme/night-city-cat.jpg` | 736 ? 414 JPEG; full available column width | User-supplied `0ae95a03469fe58971c9c2577579e7d9.jpg`; decoded pixels unchanged; JPEG origin comment added |
| Shields.io badges | Twelve external SVG badges; service-standard 28px height | HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `marks/portfolio.svg`, `marks/email.svg` | Local 28 ? 28 source canvas; displayed at 32px | Authored pixel geometry |
| `marks/github.svg` | Local 28 ? 28 source canvas; displayed at 32px | Devicon source, established display tint |
| `icons/linkedin.svg` | Local source icon; displayed at 32px | Devicon source |

The banner is an existing image, not generated artwork. Its creator was not identified by the supplied source. Shipping SHA-256: `2652e77fadd3a4644d84628418c970e15a59bddd3b86a56c5b15614fb8a8ff5b`. Its provenance is recorded in the JPEG comment and in [readme/provenance.json](readme/provenance.json).

Badge backgrounds use `#1A1B26`; frontend logos use `#7AA2F7`, backend `#BB9AF7`, database `#7DCFFF`, and tools `#C0CAF5`. Java and VS Code have text-only badges. Local contact icons are decorative beside native linked labels. Two short centered contact rows fit narrow screens, with nonbreaking spaces joining icons and labels.

GitHub Markdown API-sanitized HTML was rendered locally at 320px, 375px, and 1280px. The checks cover image loading, wrapping, keyboard focus, and no page/table overflow. Twelve badge responses were retrieved successfully. These are local preview checks, not evidence that this README version has been published. Ignored review evidence lives in `.impeccable/review/simple-black-cat/`.

## Retained SVG artwork

Earlier calico heroes, three-cat Connect panoramas, section banners, project strips, footers, accents, and labeled technology/social assets remain available. They are unreferenced by the current README. The Python standard-library generator preserves their deterministic geometry and motion fallbacks.

```sh
python scripts/generate-profile-assets.py --profile-only
```

This regenerates the retained 28-asset set: four heroes, four Connect variants, and twenty compact marks. It does not generate the current JPEG or external badges. Current README contact marks are included in that retained set. The `ROOFTOP_NIGHT` and `CAT_COATS` palettes live in `scripts/profile_theme.py`; rooftop and motion geometry live in `scripts/pixel_city.py`. Legacy `AFTER_HOURS` and train helpers remain available.

```sh
python scripts/generate-profile-assets.py --hero-only
```

This regenerates only the four legacy hero variants. The full command also regenerates older section, project, footer, accent, and labeled assets:

```sh
python scripts/generate-profile-assets.py
```

Animated rooftop editions retain a 14-second discrete tail cycle and sparse 11-, 17-, and 23-second window cycles. Reduced-motion styles freeze them. Explicit visibility attributes provide resting tails when CSS is unavailable, and static editions contain no animation stylesheet. None of these animated scenes is referenced by the current README.

Run current README reference checks, retained generation/motion checks, and contribution integrity tests:

```sh
python -m unittest discover -s tests -v
```

## Contribution data

`.github/workflows/update-activity.yml` refreshes the calendar daily at 02:17 UTC, on relevant code changes, and through **Run workflow**. It uses GitHub's built-in `GITHUB_TOKEN` with repository contents write permission; no personal access token or third-party service is needed. The workflow starts after these files reach the repository's default `main` branch, with Actions enabled. Branch protection and repository workflow policies can prevent the generated commit; the workflow log reports any such failure.

The official GitHub GraphQL `contributionCalendar` supplies actual daily counts, intensity levels, and the rolling-year total. The generator checks the total against all daily counts, requires a complete consecutive calendar, and rejects stale or malformed responses. Failed refreshes leave the last successful images in place. Both images show their reporting dates and last update date.

- `assets/github-activity.svg`: full contribution calendar, total contributions, active days, and busiest-day count.
- `assets/github-activity-mobile.svg`: the same full year split into two chronological calendar blocks.
- `assets/activity-data.json`: the verified source snapshot used for both images.

The calendar uses the established navy frame and five discrete contribution levels. To redraw the saved snapshot after an artwork change without calling GitHub or changing its dates:

```sh
python scripts/update_activity.py --render-snapshot
```

The snapshot assets and refresh workflow are retained for optional use. The profile README omits the graphic because GitHub already displays contribution activity. The generated images show the saved snapshot's reporting and update dates. It is a dated, generated image, not a live embed. No count is hardcoded into the README or generator. Counts reflect data visible to the API; GitHub determines which contributions qualify. Statistics are computed only from those returned counts.

Refresh locally using existing GitHub CLI authentication:

```sh
python scripts/update_activity.py --github-cli
```

Or run the script with `GITHUB_TOKEN` already set in the environment. Do not place credentials in repository files.

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

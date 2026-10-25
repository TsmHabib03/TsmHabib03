# Profile assets

The profile uses a **Tokyo at Night** pixel-art identity: midnight indigo, muted blue buildings, pale lettering and windows, a lavender moon and cat rim light, cyan qualification text, and sparse warm lights. Displayed artwork is stored in this repository as self-contained SVG geometry.

## Profile artwork

Regenerate the 44 assets referenced by the current README:

```sh
python scripts/generate-profile-assets.py --profile-only
```

The generator uses the Python standard library. Current scene colors live in `ROOFTOP_NIGHT` in `scripts/profile_theme.py`; shared rooftop, skyline, moon, cat, tail, window, and terminal geometry live in `scripts/pixel_city.py`. Layout, bitmap lettering, and compact brand marks live in `scripts/generate-profile-assets.py`. The legacy `AFTER_HOURS` palette and city/rail/train helpers remain intact for older artwork and authored compact marks.

| Asset family | Desktop | Mobile | Editions |
| --- | --- | --- | --- |
| `hero.svg` / `hero-mobile.svg` | 1200 × 440 | 600 × 464 | Animated and `-still.svg` |
| `section-{about,focus,stack,projects,connect}.svg` and mobile equivalents | 1200 × 160 | 600 × 160 | Animated and `-still.svg` |
| `marks/*.svg` | 28 × 28 source canvas | Same source | 20 compact brand/contact marks |

The current hero has no train. Its name and qualification remain stationary above a three-layer indigo city. A lavender stepped crater moon, pixel clouds, dense cool window patterns, and a large seated back-view cat frame the checkered rooftop ledge. Each of the five native README sections has its own shallow panorama; Current Focus includes a small terminal and desk. All scenes share the palette and geometry helpers while using fixed seeds and deliberate section compositions.

Only the cat tail and selected window lights animate. Four tail groups switch visibility with `steps(1,end)` during a 14-second cycle, resting for most of the loop. Sparse windows briefly dim from opacity 1 to 0.22 during staggered 11-, 17-, and 23-second cycles. Lamps remain within their building layers so nearer architecture still occludes them. The name, city, moon, and clouds do not move.

All scene geometry uses integer coordinates and crisp edges, with no gradients, filters, external fonts, scripts, or image dependencies. Fixed local random seeds make generation deterministic. Desktop and mobile scenes are separately composed rather than relying on cropping.

Marks display at 24px beside native technology and contact names, or 18px beside project descriptions. Brand marks retain source colors or established display tints; they do not all use the rooftop palette. Names and links remain native text, and decorative panoramas have empty image alternatives. The compact PHP, Bootstrap, and VS Code marks flatten source gradients and remove filters while retaining upstream geometry. Raw inputs, legacy labeled icons, and their attribution are preserved.

The README's `<picture>` selects mobile at viewport widths up to 600px and animation-free variants for reduced-motion preference. Animated SVGs also include an internal reduced-motion query. Explicit visibility attributes show only the resting tail when CSS is unavailable, and windows stay illuminated. Static editions preserve complete scene geometry without an animation stylesheet.

Local Chromium previews were checked at 320px, 375px, and desktop widths, including source selection, image loading, page overflow, tail visibility, window opacity, and static/reduced-motion fallbacks. These results do not establish live GitHub rendering. GitHub sanitization, image proxying, and caching can affect SVG CSS and media selection; profile text and links stay in native Markdown outside the artwork.

To regenerate only the four hero variants:

```sh
python scripts/generate-profile-assets.py --hero-only
```

Older project strips, footer, labeled tech/social assets, and three small accents remain supported for compatibility but are no longer referenced by the profile. The full command regenerates those assets as well as the current profile; use it only when those legacy outputs need regeneration:

```sh
python scripts/generate-profile-assets.py
```

Run profile generation, reference, and animation contract tests:

```sh
python -m unittest discover -s tests -p test_profile_assets.py -v
```

Run all available tests, including contribution integrity:

```sh
python -m unittest discover -s tests -v
```

## Contribution data

`.github/workflows/update-activity.yml` refreshes the calendar daily at 02:17 UTC, on relevant code changes, and through **Run workflow**. It uses GitHub's built-in `GITHUB_TOKEN` with repository contents write permission; no personal access token or third-party service is needed. The workflow starts after these files reach the repository's default `main` branch, with Actions enabled. Branch protection and repository workflow policies can prevent the generated commit; the workflow log reports any such failure.

The official GitHub GraphQL `contributionCalendar` supplies actual daily counts, intensity levels, and the rolling-year total. The generator checks the total against all daily counts, requires a complete consecutive calendar, and rejects stale or malformed responses. Failed refreshes leave the last successful images in place. Both images show their reporting dates and last update date.

- `assets/github-activity.svg`: full contribution calendar, total contributions, active days, and busiest-day count.
- `assets/github-activity-mobile.svg`: the same full year split into two chronological calendar blocks.
- `assets/activity-data.json`: the verified source snapshot used for both images.

A muted pixel skyline sits behind the activity scene; opaque navy beneath the calendar keeps decorative windows separate from actual contribution cells. To redraw the saved snapshot after an artwork change without calling GitHub or changing its dates:

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

# Profile assets

The profile uses a **Tokyo at Night** pixel-art identity: midnight navy, slate-blue buildings, off-white lettering, cyan accents, and sparse warm windows. All displayed artwork is stored in this repository and uses self-contained SVG geometry.

## Profile artwork

Regenerate the 27 assets referenced by the current README:

```sh
python scripts/generate-profile-assets.py --profile-only
```

The generator uses the Python standard library. Shared colors live in `AFTER_HOURS` in `scripts/profile_theme.py`; authored skyline, Tokyo Tower, moon, cat, railway, train, and workstation geometry live in `scripts/pixel_city.py`. Layout, bitmap lettering, and compact brand marks live in `scripts/generate-profile-assets.py`. Legacy palette tokens and the original city helper are preserved for other artwork.

| Variant | Dimensions | Purpose |
| --- | --- | --- |
| `hero.svg` | 1200 × 440 | Desktop, animated train and occasional cat-tail movement |
| `hero-still.svg` | 1200 × 440 | Desktop, stationary train |
| `hero-mobile.svg` | 600 × 464 | Mobile, two-line name and restrained motion |
| `hero-mobile-still.svg` | 600 × 464 | Mobile, stationary train |

The name, moon, city, and windows stay stationary. Three linked train carriages share doors, windows, wheels, roof equipment, and a continuous cyan stripe. The cat's stepped tail lifts two source pixels briefly during a 12-second cycle. All scene geometry uses integer coordinates and crisp edges, without gradients, filters, external fonts, scripts, or image dependencies. Building positions are authored; window placement uses a fixed random seed.

The remaining assets are 20 transparent brand/contact marks in `marks/`, a thin skyline divider, a small workstation, and a static cat accent. Marks use a 28 × 28 source canvas and display at 24px in the stack and contact sections or 18px beside project descriptions. Names and links remain native text; decorative accents have empty image alternatives. The compact PHP, Bootstrap, and VS Code marks flatten source gradients and remove filters while retaining the upstream geometry. Raw icon inputs and legacy labeled icons are preserved.

The train travels from `-TRAIN_WIDTH - TRAIN_MARGIN` to `scene_width + TRAIN_MARGIN`, then waits outside the clip for the final 12% of each loop before resetting. Desktop loops take 28 seconds; mobile loops take 24 seconds. The negative delay starts with the whole train visible. The static transform also shows all three carriages when SVG CSS animation is unavailable.

The README's `<picture>` selects mobile at viewport widths up to 600px and animation-free variants for reduced-motion preference. Animated SVGs also contain an internal reduced-motion media query. Browser and GitHub sanitization/caching can affect media selection; local preview validation does not establish live GitHub compatibility. GitHub embeds SVGs as images, so links and profile text remain native Markdown outside the artwork.

To regenerate only the four hero variants, the existing command remains available:

```sh
python scripts/generate-profile-assets.py --hero-only
```

The older project strips, footer, tech, and social assets are retained for compatibility but no longer referenced by the profile. To regenerate every asset supported by the existing profile generator:

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

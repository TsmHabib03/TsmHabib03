# Profile assets

All artwork uses a TokyoNight Storm palette: navy panels, blue/cyan accents, muted purple, and pale text. Images are stored in this repository; visitors do not depend on a third-party statistics or icon service.

## Static artwork

Edit `scripts/generate-profile-assets.py` and regenerate:

```sh
python scripts/generate-profile-assets.py
```

Shared SVG helpers and colors live in `scripts/profile_theme.py`. The pixel-art hero, centered technology icon wall, project cards, and portfolio CTA have no animation. Mobile picture sources preserve readable type and icons. Card images wrap from two columns to one without tables.

## Contribution data

`.github/workflows/update-activity.yml` refreshes the calendar daily at 02:17 UTC, on relevant code changes, and through **Run workflow**. It uses GitHub's built-in `GITHUB_TOKEN` with repository contents write permission; no personal access token or third-party service is needed. The workflow starts after these files reach the repository's default `main` branch, with Actions enabled. Branch protection and repository workflow policies can prevent the generated commit; the workflow log reports any such failure.

The official GitHub GraphQL `contributionCalendar` supplies actual daily counts, intensity levels, and the rolling-year total. The generator checks the total against all daily counts, requires a complete consecutive calendar, and rejects stale or malformed responses. Failed refreshes leave the last successful images in place. Both images show their reporting dates and last update date.

- `assets/github-activity.svg`: full contribution calendar, total contributions, active days, and busiest-day count.
- `assets/github-activity-mobile.svg`: the same full year split into two chronological calendar blocks.
- `assets/activity-data.json`: the verified source snapshot used for both images.

The graphic complements the native GitHub profile contribution UI. It is a dated, generated image, not a live embed. No count is hardcoded into the README or generator. Counts reflect data visible to the API; GitHub determines which contributions qualify. Statistics are computed only from those returned counts.

Refresh locally using existing GitHub CLI authentication:

```sh
python scripts/update_activity.py --github-cli
```

Or run the script with `GITHUB_TOKEN` already set in the environment. Do not place credentials in repository files.

## Icon attribution

The 14 local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) · [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) · [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining them into the technology wall. Laragon and Google Apps Script icons are tinted to `#0E83CD` and `#4285F4` (Simple Icons brand colors) inside the generator, because Simple Icons ships single-path glyphs without colors.

## Project sources

Public repositories and links were checked on 2026-09-27:

- [QCU Schedule](https://github.com/TsmHabib03/QCU-Schedule-Web-App): student schedule platform.
- [ASJ Attendance Checker](https://github.com/TsmHabib03/ASJ-Attendance-Checker): QR attendance and role-based dashboards.
- [RepCore Fitness](https://github.com/TsmHabib03/Repcorefitness): membership and attendance workflows.
- [Manila City Council HRIS](https://github.com/TsmHabib03/Manila-City-Council-HRIS): employee records and leave management, documented in its README.

No employment, client relationship, adoption, or expert-level claims are inferred from repository names.

# Profile artwork

Regenerate the SVGs after editing their text or layout:

```sh
python scripts/generate-profile-assets.py
```

The generator uses only Python's standard library. All assets are local, with no external fonts, scripts, trackers, or statistics services.

## GitHub presentation

- `hero.svg` and `hero-mobile.svg`: identity, terminal detail, and a slow cursor pulse.
- `tech-stack.svg` and `tech-stack-mobile.svg`: a 42-second CSS animation moves two identical icon sequences horizontally. Local SVG symbols keep the image self-contained and the loop seamless.
- `tech-stack-static.svg` and `tech-stack-static-mobile.svg`: all 13 icons remain visible for visitors who prefer reduced motion. The README selects these through `<picture>`; animations also honor reduced motion inside the SVG.
- `project-*.svg`: four cards wrapped in ordinary repository links. Their 400px display width allows two columns on a wide profile and one on a narrow screen, without tables.
- `portfolio.svg` and `portfolio-mobile.svg`: linked portfolio call to action.

GitHub-compatible image markup carries the visuals. README text provides the introduction, study topics, web development areas, and status. Every image has alternative text. No JavaScript runs in the README. SVG animations run when the client supports animated SVG images; static clients retain a readable first frame.

## Icon sources

The icons in `icons/` are the generator's inputs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, Tailwind CSS, Bootstrap, PHP, MySQL, Java, Git, GitHub, and VS Code. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) · [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Google Apps Script and Google Sheets. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) · [CC0 license](icons/LICENSE-simple-icons.txt).

The icons use pale backplates for contrast. Simple Icons marks use brand colors. SVG definition IDs are namespaced when combining icons.

## Content sources

Project links and the portfolio were rechecked on 2026-09-27. Descriptions come from the public repository documentation and source inspected in this session:

- [QCU Schedule](https://github.com/TsmHabib03/QCU-Schedule-Web-App): landing page, architecture, and Google integration documentation.
- [RepCore Fitness](https://github.com/TsmHabib03/Repcorefitness): membership and QR attendance workflows.
- [ASJ Attendance Checker](https://github.com/TsmHabib03/ASJ-Attendance-Checker): QR attendance, PHP, and MySQL.
- [Event Registration](https://github.com/TsmHabib03/Event-Registration-with-QR-Tickets-System): JavaScript, Google Apps Script, Google Sheets, and QR registration.

Update age and year level in the README as needed. Project-card text lives in `PROJECTS` in the generator; repository links live in the README. No employment, client relationships, usage numbers, or expert-level claims are inferred from project names.

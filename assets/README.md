# Profile assets

[README.md](../README.md) renders the entire profile directly on GitHub. Two abstract pixel banners frame About, twelve technology badges, Education and four contact links.

| Asset | Display | Source |
| --- | --- | --- |
| `readme/profile-banner.svg` | 1200 x 340 orange name banner | Authored square geometry inspired by reference 1; outlined Silkscreen letters |
| `readme/profile-banner-mobile.svg` | 600 x 360 mobile name banner | Separate two-line name composition |
| `readme/connect-banner.svg` | 1200 x 220 blue/cyan connection banner | Authored modular squares inspired by reference 2 |
| `readme/connect-banner-mobile.svg` | 600 x 240 mobile connection banner | Separate narrow-screen composition |
| `fonts/silkscreen-latin.ttf` | Build-time source for pixel letters | Google Fonts Silkscreen; SIL OFL license beside file |
| Shields.io badges | Twelve charcoal SVG badges | HTML, CSS, JavaScript, Tailwind CSS, Bootstrap, PHP, Java, MySQL, Git, GitHub, Docker, VS Code |
| `marks/facebook.svg`, `instagram.svg`, `github.svg`, `email.svg` | Linked contact marks at 32 x 32px | Attributed brand inputs and authored email geometry |

[scripts/build-readme-banners.py](../scripts/build-readme-banners.py) creates all four self-contained SVG files. Pillow and the local font are build-time dependencies only. Letters are paths; abstract geometry uses rectangles. The hero gently moves a few decorative squares over nine seconds; reduced-motion disables animation and all text remains visible.

The supplied `330982eb338215bfe1379446458b8802.jpg` and `789c8708e57ef4b55ea26df089f2bcee.jpg` are composition references, retained as `readme/orange-reference.jpg` and `readme/modular-reference.jpg`. Their decoded pixels, sample text and watermarks remain unchanged. Origins and hashes are in [reference-provenance.json](readme/reference-provenance.json). No scene artwork was generated and no new raster is used by the README.

GitHub Markdown API-sanitized output was checked at 320px, 375px and 1280px: correct responsive SVG selection, badge wrapping, no broken images and no page overflow. All 22 relevant tests pass. Evidence lives in the ignored `.impeccable/review/profile-readme/` directory.

## Retained assets

Earlier city/cat scenes, project strips, original reference JPEGs and contribution assets remain for their existing generators and attribution history. The corrected README does not reference the cat, project strips or legacy scenes. Contribution data and refresh files remain unchanged by this revision.

`python -m unittest discover -s tests -q` checks current README references, retained deterministic assets and contribution integrity.

## Icon attribution

Local icon inputs are in `assets/icons/`, stored as raw brand SVGs. Brand marks belong to their respective owners.

- **Devicon:** HTML5, CSS3, JavaScript, PHP, Java, Tailwind CSS, Bootstrap, MySQL, Git, GitHub, VS Code, Docker, LinkedIn, Facebook. [Pinned source](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons) and [MIT license](icons/LICENSE-devicon.txt).
- **Simple Icons:** Laragon, Google Apps Script, Spring Boot, Instagram, TikTok. [Pinned source](https://github.com/simple-icons/simple-icons/tree/d4e6ba93e48f178898707f0145ec285f28b64b38/icons) and [CC0 license](icons/LICENSE-simple-icons.txt).

Definition IDs are namespaced when combining icons. Display tints are defined by `BRAND_TINT` in the retained profile generator. Portfolio and email marks are authored pixel geometry; other compact marks use the attributed sources above.

"""Build the profile's self-contained SVG artwork with Python's standard library."""

from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY, PANEL, BORDER = "#091426", "#102039", "#233D5B"
WHITE, MUTED, BLUE, CYAN = "#F3F7FF", "#A6B8D0", "#5795FF", "#76D9EF"
SANS = "'Segoe UI', Arial, sans-serif"
MONO = "Consolas, 'Liberation Mono', monospace"
TECH = [
    ("html5", "HTML5"), ("css3", "CSS3"), ("javascript", "JavaScript"),
    ("tailwindcss", "Tailwind CSS"), ("bootstrap", "Bootstrap"),
    ("php", "PHP"), ("mysql", "MySQL"), ("java", "Java"),
    ("googleappsscript", "Google Apps Script"), ("googlesheets", "Google Sheets"),
    ("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code"),
]


def text(x, y, value, size=20, color=WHITE, mono=False, weight=400, **attrs):
    extras = " ".join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k, v in attrs.items())
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" font-weight="{weight}" {extras}>{escape(value)}</text>')


def rect(x, y, w, h, fill=PANEL, radius=12, stroke=BORDER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def document(name, width, height, title, body, description=""):
    source = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
              f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
              'role="img" aria-labelledby="title description">\n'
              f'<title id="title">{escape(title)}</title>\n'
              f'<desc id="description">{escape(description or title)}</desc>\n'
              + body + '\n</svg>\n')
    ET.fromstring(source)
    (ASSETS / name).write_text(source, encoding="utf-8")


def frame(width, height):
    return rect(1, 1, width - 2, height - 2, NAVY, 18)


def hero(mobile=False):
    w, h = (600, 376) if mobile else (1200, 312)
    parts = [frame(w, h), '''<defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#172B45" stroke-width="1"/>
    </pattern></defs>''', f'<rect x="{w * .58}" y="18" width="{w * .4}" height="{h - 36}" rx="12" fill="url(#grid)"/>',
        '<style>@keyframes breathe{0%,100%{opacity:.3}50%{opacity:1}}.cursor{animation:breathe 3s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.cursor{animation:none}}</style>',
        f'<path d="M32 1H140" stroke="{BLUE}" stroke-width="3"/>',
        text(36, 44, "QCU / COMPUTER SCIENCE / PHILIPPINES", 14, MUTED, True, letter_spacing=1)]
    if mobile:
        parts += [text(34, 119, "HABIB D.", 57, weight=700), text(34, 183, "JAUDIAN", 57, weight=700),
                  text(36, 227, "BSCS STUDENT // WEB DEVELOPER", 18, CYAN, True),
                  text(36, 254, "ASPIRING SOFTWARE ENGINEER", 18, CYAN, True),
                  text(36, 329, "> building_web_apps();", 23, WHITE, True),
                  '<rect class="cursor" x="340" y="310" width="10" height="24" fill="#5795FF"/>']
    else:
        parts += [text(44, 138, "HABIB D. JAUDIAN", 68, weight=700),
                  text(46, 188, "BSCS STUDENT // WEB DEVELOPER // ASPIRING SOFTWARE ENGINEER", 20, CYAN, True),
                  text(46, 261, "> building_web_apps();", 25, WHITE, True),
                  '<rect class="cursor" x="376" y="240" width="12" height="27" fill="#5795FF"/>',
                  rect(1010, 66, 134, 86, "#112848", 14, "#335A86"),
                  text(1077, 123, "</>", 44, BLUE, True, text_anchor="middle")]
    document("hero-mobile.svg" if mobile else "hero.svg", w, h, "Habib D. Jaudian", "\n".join(parts),
             "BSCS student, web developer, and aspiring software engineer. Quezon City University, Philippines. Building web apps.")


def icon_symbols():
    symbols = []
    for slug, label in TECH:
        raw = (ASSETS / "icons" / f"{slug}.svg").read_text(encoding="utf-8")
        inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
        inner = re.sub(r'</svg>\s*$', '', inner)
        # Each source has its own gradient IDs; namespace them before combining icons.
        for ident in re.findall(r'\bid="([^"]+)"', inner):
            inner = inner.replace(f'id="{ident}"', f'id="{slug}-{ident}"')
            inner = inner.replace(f'url(#{ident})', f'url(#{slug}-{ident})')
            inner = inner.replace(f'href="#{ident}"', f'href="#{slug}-{ident}"')
        symbols.append(f'<symbol id="icon-{slug}" viewBox="0 0 64 64">{inner}</symbol>')
    return "\n".join(symbols)


def tech_tile(slug, label, x, y):
    return (f'<g transform="translate({x} {y})">' + rect(0, 0, 140, 116, PANEL, 12)
            + f'<use href="#icon-{slug}" x="40" y="13" width="60" height="60"/>'
            + text(70, 99, label, 14 if len(label) > 14 else 17, MUTED, text_anchor="middle") + '</g>')


def ticker(mobile=False, static=False):
    w = 480 if mobile else 1200
    columns = 3 if mobile else 7
    h = (68 + ((len(TECH) + columns - 1) // columns) * 130 + 14) if static else 216
    parts = [frame(w, h), '<defs>' + icon_symbols() + '</defs>',
             text(28, 38, "// TECH STACK", 18, BLUE, True)]
    if not mobile:
        parts.append(text(w - 28, 38, "TOOLS I BUILD WITH", 14, MUTED, True, text_anchor="end"))
    if static:
        for i, (slug, label) in enumerate(TECH):
            parts.append(tech_tile(slug, label, 20 + (i % columns) * ((w - 40) / columns), 64 + (i // columns) * 130))
    else:
        distance = 154 * len(TECH)
        tiles = "\n".join(tech_tile(slug, label, i * 154, 0) for i, (slug, label) in enumerate(TECH))
        parts += [f'''<defs>
          <clipPath id="window"><rect x="24" y="64" width="{w - 48}" height="120"/></clipPath>
          <g id="sequence">{tiles}</g>
          <linearGradient id="edge"><stop stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>
        </defs>
        <style>
          @keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{distance}px)}}}}
          .track{{animation:scroll 42s linear infinite}}
          @media(prefers-reduced-motion:reduce){{.track{{animation:none}}}}
        </style>
        <g clip-path="url(#window)"><g transform="translate(24 64)"><g class="track">
          <use href="#sequence"/><use href="#sequence" x="{distance}"/>
        </g></g></g>
        <rect x="24" y="63" width="28" height="122" fill="url(#edge)"/>
        <rect x="{w - 52}" y="63" width="28" height="122" fill="url(#edge)" transform="rotate(180 {w - 38} 124)"/>''']
    suffix = ("-static" if static else "") + ("-mobile" if mobile else "")
    document(f"tech-stack{suffix}.svg", w, h, "Technologies I work with", "\n".join(parts),
             ", ".join(label for _, label in TECH) + "." + ("" if static else " A continuous horizontal ticker; static alternative available for reduced motion."))


PROJECTS = [
    ("qcu-schedule", "01 / STUDENT PLATFORM", "QCU Schedule", ["Student-focused web platform for", "Quezon City University."], "JavaScript / Apps Script / Sheets", "calendar"),
    ("repcore-fitness", "02 / MEMBERSHIP SYSTEM", "RepCore Fitness", ["PHP/MySQL fitness membership", "and QR attendance system."], "PHP / MySQL / JavaScript", "qr"),
    ("asj-attendance", "03 / ATTENDANCE SYSTEM", "ASJ Attendance Checker", ["QR-based attendance management", "using PHP and MySQL."], "PHP / MySQL / JavaScript", "qr"),
    ("event-registration", "04 / EVENT WORKFLOWS", "Event Registration", ["QR event registration with", "Google Apps Script and Sheets."], "JavaScript / Apps Script / Sheets", "ticket"),
]


def project_card(slug, eyebrow, title, lines, stack, glyph):
    body = [frame(600, 264), text(28, 37, eyebrow, 15, BLUE, True, letter_spacing=1),
            text(28, 91, title, 32, weight=600), text(28, 133, lines[0], 22, MUTED),
            text(28, 163, lines[1], 22, MUTED), f'<path d="M28 191H572" stroke="{BORDER}"/>',
            text(28, 228, stack, 16, CYAN, True), text(558, 231, "↗", 26, BLUE)]
    if glyph == "calendar":
        shape = '<rect x="0" y="0" width="26" height="24" rx="4"/><path d="M0 7H26M7 -3V3M19 -3V3M6 13H10M16 13H20M6 19H10"/>'
    elif glyph == "qr":
        shape = '<path d="M0 0H10V10H0ZM16 0H26V10H16ZM0 16H10V26H0ZM16 16H20V20H26V26H16Z"/>'
    else:
        shape = '<path d="M0 1H26V7C20 7 20 17 26 17V23H0V17C6 17 6 7 0 7ZM17 4V8M17 11V14M17 17V20"/>'
    body.append(f'<g transform="translate(544 23)" fill="none" stroke="{BLUE}" stroke-width="1.6">{shape}</g>')
    # Transparent space below each card preserves a gutter when inline images wrap.
    document(f"project-{slug}.svg", 600, 280, title, "\n".join(body), " ".join(lines) + " " + stack)


def portfolio():
    body = [frame(1200, 160), '<path d="M1 25V135" stroke="#5795FF" stroke-width="4"/>',
            text(38, 64, ">_ EXPLORE MY WORK", 34, WHITE, True, weight=700),
            text(39, 115, "Interactive Portfolio", 25, CYAN),
            '<circle cx="1110" cy="80" r="36" fill="#152F52" stroke="#5795FF"/>',
            '<path d="M1097 93L1123 67M1097 67H1123V93" fill="none" stroke="#76D9EF" stroke-width="3"/>']
    document("portfolio.svg", 1200, 160, "Explore my work — Interactive Portfolio", "\n".join(body))
    mobile = [frame(480, 148), '<path d="M1 25V123" stroke="#5795FF" stroke-width="4"/>',
              text(24, 59, ">_ EXPLORE MY WORK", 25, WHITE, True, weight=700),
              text(25, 105, "Interactive Portfolio", 22, CYAN),
              '<circle cx="423" cy="74" r="25" fill="#152F52" stroke="#5795FF"/>',
              '<path d="M414 83L432 65M414 65H432V83" fill="none" stroke="#76D9EF" stroke-width="2"/>']
    document("portfolio-mobile.svg", 480, 148, "Explore my work — Interactive Portfolio", "\n".join(mobile))


if __name__ == "__main__":
    hero()
    hero(mobile=True)
    for mobile in (False, True):
        for static in (False, True):
            ticker(mobile, static)
    for project in PROJECTS:
        project_card(*project)
    portfolio()
    print("Generated 12 self-contained profile SVGs.")

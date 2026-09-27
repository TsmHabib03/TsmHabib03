"""Generate the profile's static TokyoNight artwork. No external dependencies."""
import re
from profile_theme import ASSETS, NAVY, PANEL, BORDER, WHITE, MUTED, BLUE, CYAN, PURPLE, text, rect, frame, svg, write_assets

GROUPS = [
    ("Languages", [("html5", "HTML5"), ("css3", "CSS3"), ("javascript", "JavaScript"), ("php", "PHP"), ("java", "Java")]),
    ("Frameworks / UI", [("tailwindcss", "Tailwind CSS"), ("bootstrap", "Bootstrap")]),
    ("Database", [("mysql", "MySQL")]),
    ("Tools", [("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code"), ("xampp", "XAMPP"), ("powershell", "PowerShell")]),
]
PROJECTS = [
    ("qcu-schedule", "01 / STUDENT PLATFORM", "QCU Schedule", "Class schedules and student tools for QCU."),
    ("asj-attendance", "02 / ATTENDANCE SYSTEM", "ASJ Attendance Checker", "QR attendance with role-based dashboards."),
    ("repcore-fitness", "03 / MEMBERSHIP SYSTEM", "RepCore Fitness", "Fitness membership and QR attendance."),
    ("manila-hris", "04 / INFORMATION SYSTEM", "Manila City Council HRIS", "Employee records and leave management."),
]


def hero(mobile=False):
    w, h = (600, 264) if mobile else (1200, 242)
    body = [frame(w, h), '''<defs>
      <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
        <path d="M28 0H0V28" fill="none" stroke="#3B4261" stroke-width="1"/>
      </pattern>
      <filter id="glow"><feGaussianBlur stdDeviation="14"/></filter>
    </defs>''', f'<rect x="{w*.59}" y="18" width="{w*.39}" height="{h-36}" rx="12" fill="url(#grid)" opacity=".5"/>',
            text(32, 39, "QCU / COMPUTER SCIENCE / PHILIPPINES", 14, MUTED, True, letter_spacing=1),
            f'<path d="M32 1H146" stroke="{PURPLE}" stroke-width="3"/>']
    if mobile:
        body += [text(30, 107, "Habib D.", 59, weight=700), text(30, 172, "Jaudian", 59, weight=700),
                 text(32, 227, "> building_web_systems();", 21, CYAN, True)]
    else:
        body += [text(42, 129, "Habib D. Jaudian", 68, weight=700),
                 text(44, 196, "> building_web_systems();", 25, CYAN, True),
                 '<circle cx="1073" cy="126" r="49" fill="#7AA2F7" opacity=".13" filter="url(#glow)"/>',
                 rect(1007, 70, 132, 104, "#293758", 16, "#565F89"),
                 text(1073, 138, "{ }", 42, PURPLE, True, text_anchor="middle")]
    return svg(w, h, "Habib D. Jaudian", "\n".join(body))


def icon_symbols():
    symbols = []
    for _, icons in GROUPS:
        for slug, _ in icons:
            raw = (ASSETS / "icons" / f"{slug}.svg").read_text(encoding="utf-8")
            inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
            inner = re.sub(r'</svg>\s*$', '', inner)
            for ident in re.findall(r'\bid="([^"]+)"', inner):
                inner = inner.replace(f'id="{ident}"', f'id="{slug}-{ident}"')
                inner = inner.replace(f'url(#{ident})', f'url(#{slug}-{ident})')
                inner = inner.replace(f'href="#{ident}"', f'href="#{slug}-{ident}"')
            symbols.append(f'<symbol id="icon-{slug}" viewBox="0 0 64 64">{inner}</symbol>')
    return "\n".join(symbols)


def tech_wall(mobile=False):
    w = 600 if mobile else 1200
    h = 1020 if mobile else 570
    body = [frame(w, h), "<defs>" + icon_symbols() + "</defs>"]
    y = 28
    for index, (label, icons) in enumerate(GROUPS):
        if mobile:
            body.append(text(30, y + 22, label.upper(), 21, PURPLE, True))
            top = y + 42
            for i, (slug, name) in enumerate(icons):
                x, row = 34 + (i % 3) * 184, i // 3
                body += [rect(x, top + row * 126, 164, 114, PANEL, 12),
                         f'<use href="#icon-{slug}" x="{x+44}" y="{top+row*126+8}" width="76" height="76"/>',
                         text(x + 82, top + row * 126 + 103, name, 19, MUTED, text_anchor="middle")]
            y = top + ((len(icons) + 2) // 3) * 126 + 12
        else:
            top = 24 + index * 136
            body += [text(32, top + 55, label.upper(), 18, PURPLE, True),
                     f'<path d="M220 {top+4}V{top+108}" stroke="{BORDER}"/>']
            for i, (slug, name) in enumerate(icons):
                x = 250 + i * 178
                body += [rect(x, top, 158, 118, PANEL, 12),
                         f'<use href="#icon-{slug}" x="{x+39}" y="{top+9}" width="80" height="80"/>',
                         text(x + 79, top + 107, name, 18, MUTED, text_anchor="middle")]
    # The mobile height follows the groups so all icons remain visible without motion.
    if mobile:
        h = y + 12
        body[0] = frame(w, h)
    description = "; ".join(label + ": " + ", ".join(name for _, name in icons) for label, icons in GROUPS)
    return svg(w, h, "Tech Stack", "\n".join(body), description)


def project_card(eyebrow, title, description):
    body = [frame(600, 188), text(28, 33, eyebrow, 14, PURPLE, True, letter_spacing=1),
            text(28, 77, title, 30, weight=600), text(28, 115, description, 21, MUTED),
            text(28, 162, "VIEW REPOSITORY", 14, CYAN, True), text(558, 164, "↗", 26, BLUE)]
    return svg(600, 204, title, "\n".join(body), description)


def portfolio(mobile=False):
    w, h = (480, 148) if mobile else (1200, 154)
    x = 423 if mobile else 1110
    body = [frame(w, h), f'<path d="M1 25V{h-25}" stroke="{PURPLE}" stroke-width="4"/>',
            text(24 if mobile else 38, 59 if mobile else 64, ">_ VIEW PORTFOLIO", 25 if mobile else 34, WHITE, True, weight=700),
            text(25 if mobile else 39, 105 if mobile else 111, "Explore my work", 22 if mobile else 25, CYAN),
            f'<circle cx="{x}" cy="74" r="{25 if mobile else 34}" fill="#293758" stroke="{BLUE}"/>',
            f'<path d="M{x-9} 83L{x+9} 65M{x-9} 65H{x+9}V83" fill="none" stroke="{CYAN}" stroke-width="2"/>']
    return svg(w, h, "View portfolio — explore my work", "\n".join(body))


if __name__ == "__main__":
    outputs = {}
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        outputs[f"hero{suffix}.svg"] = hero(mobile)
        outputs[f"tech-stack{suffix}.svg"] = tech_wall(mobile)
        outputs[f"portfolio{suffix}.svg"] = portfolio(mobile)
    for slug, eyebrow, title, description in PROJECTS:
        outputs[f"project-{slug}.svg"] = project_card(eyebrow, title, description)
    write_assets(outputs)
    print("Generated 10 static TokyoNight profile assets.")

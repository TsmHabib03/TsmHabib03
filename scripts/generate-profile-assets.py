"""Generate self-contained TokyoNight SVG artwork. No external dependencies."""
import random
import re
from profile_theme import ASSETS, NAVY, BORDER, WHITE, MUTED, BLUE, CYAN, PURPLE, text, rect, frame, svg, write_assets
from pixel_city import Pixels, city, step_outline

GROUPS = [
    ("Languages", [("html5", "HTML5"), ("css3", "CSS3"), ("javascript", "JavaScript"), ("php", "PHP"), ("java", "Java")]),
    ("Frameworks / UI", [("tailwindcss", "Tailwind CSS"), ("bootstrap", "Bootstrap")]),
    ("Database", [("mysql", "MySQL")]),
    ("Tools", [("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code"), ("docker", "Docker"), ("laragon", "Laragon"), ("googleappsscript", "Google Apps Script")]),
]
# The same 14 technologies, grouped by purpose without tiles or containers.
WALL_ROWS = [
    ("LANGUAGES", ["html5", "css3", "javascript", "php", "java"]),
    ("UI & DATA", ["tailwindcss", "bootstrap", "mysql"]),
    ("TOOLS & AUTOMATION", ["git", "github", "vscode", "docker", "laragon", "googleappsscript"]),
]
# Stacks checked against public repository languages and READMEs, 2026-09-28.
PROJECTS = [
    ("qcu-schedule", "QCU Schedule", "Class schedules and student tools for QCU.", "HTML · CSS · JavaScript"),
    ("asj-attendance", "ASJ Attendance Checker", "QR attendance with role-based dashboards.", "PHP · MySQL · JavaScript"),
    ("repcore-fitness", "RepCore Fitness", "Fitness membership and QR attendance.", "PHP · MySQL · JavaScript"),
    ("manila-hris", "Manila City Council HRIS", "Employee records and leave management.", "Java · Spring Boot · MySQL"),
]

NAME = "HABIB JAUDIAN D."
PIXEL_FONT = {
    " ": ["000"],
    ".": ["00", "00", "00", "00", "11"],
    "-": ["000", "000", "111", "000", "000"],
    "A": ["01110", "10001", "11111", "10001", "10001"],
    "B": ["11110", "10001", "11110", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "11110", "10000", "11111"],
    "F": ["11111", "10000", "11110", "10000", "10000"],
    "G": ["01111", "10000", "10011", "10001", "01111"],
    "H": ["10001", "10001", "11111", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "11100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001"],
    "O": ["01110", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "11110", "10000", "10000"],
    "R": ["11110", "10001", "11110", "10010", "10001"],
    "S": ["01111", "10000", "01110", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10101", "11011", "10001"],
    "X": ["10001", "01010", "00100", "01010", "10001"],
    "Y": ["10001", "01010", "00100", "00100", "00100"],
    "Z": ["11111", "00010", "00100", "01000", "11111"],
}


def pixel_width(value, cell):
    return sum(len(PIXEL_FONT[ch][0]) + 1 for ch in value) * cell - cell


def pixel_text(value, x, y, cell, color=WHITE):
    parts = Pixels()
    cursor = x
    for ch in value:
        glyph = PIXEL_FONT[ch]
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit != "0":
                    parts.box(cursor + c * cell, y + r * cell, cell, cell, color)
        cursor += (len(glyph[0]) + 1) * cell
    return parts.draw()


def stars(w, y_min, y_max, avoid, seed=11):
    rng = random.Random(seed)
    parts = []
    attempts = 0
    while len(parts) < 14 and attempts < 200:
        attempts += 1
        x, y = rng.randint(6, w - 8), rng.randint(y_min, y_max)
        if any(x >= ax0 and x <= ax1 and y >= ay0 and y <= ay1 for ax0, ay0, ax1, ay1 in avoid):
            continue
        shade = rng.random()
        color = "#3E4A6B" if shade < 0.55 else "#565F89" if shade < 0.85 else CYAN
        size = 3 if w > 600 else 2
        opacity = ' opacity=".55"' if color == CYAN else ""
        parts.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"{opacity}/>')
    return "\n".join(parts)


def hero(mobile=False, animated=True):
    if mobile:
        w, h, name_cell = 600, 320, 6
        sky_y, name_y = 96, 52
        eyebrow_size, eyebrow_y, role_size, role_y = 12, 30, 15, 304
    else:
        w, h, name_cell = 1200, 420, 12
        sky_y, name_y = 142, 64
        eyebrow_size, eyebrow_y, role_size, role_y = 14, 38, 21, 404
    outline = step_outline(1, 1, w-2, h-2)
    body = [f'<path d="{outline}" fill="{NAVY}" stroke="{BORDER}"/>']
    body.append(text(32, eyebrow_y, "~/computer-science · web · software-engineering", eyebrow_size, "#565F89", True))
    body.append(text(w - 32, eyebrow_y, "</>", eyebrow_size, "#565F89", True, text_anchor="end"))
    avoid = [(24, name_y - 4, 32 + pixel_width(NAME, name_cell) + 34, name_y + 5 * name_cell + 4)]
    body.append(stars(w, eyebrow_y + 12, sky_y - 8, avoid))
    body.append(pixel_text(NAME, 32, name_y, name_cell, WHITE))
    cursor_x = 32 + pixel_width(NAME, name_cell) + name_cell
    body.append(f'<rect x="{cursor_x}" y="{name_y}" width="{2 * name_cell}" height="{5 * name_cell}" fill="{CYAN}"/>')
    scene_h = 186 if mobile else 244
    body.append(f'<g transform="translate(8 {sky_y})">'
                + city(w-16, scene_h, seed=20260927, animated=animated, pace=28)
                + '</g>')
    body.append(text(w / 2, role_y, "BSCS STUDENT · WEB DEVELOPER · ASPIRING SOFTWARE ENGINEER", role_size, CYAN, True, letter_spacing=1, text_anchor="middle"))
    return svg(w, h, "Habib Jaudian D.", "\n".join(body),
               "Habib Jaudian D. — BSCS Student, Web Developer, Aspiring Software Engineer. "
               "Tokyo-inspired pixel city with layered buildings, rooftop tanks, an observation tower, lit windows, a moon, clouds, an elevated train, traffic and wet-street reflections. "
               + ("Subtle looping city motion." if animated else "Static reduced-motion edition."))


# Simple Icons ships single-path glyphs without colors; tint them to their brand colors here.
# GitHub and MySQL get their on-dark renderings for contrast on navy.
BRAND_TINT = {"laragon": "#0E83CD", "googleappsscript": "#4285F4", "github": "#D5DEFB", "mysql": "#4479A1"}


def icon_symbols():
    symbols = []
    for _, icons in GROUPS:
        for slug, _ in icons:
            raw = (ASSETS / "icons" / f"{slug}.svg").read_text(encoding="utf-8")
            view = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', raw)
            size = view.group(1).split(".")[0]
            inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
            inner = re.sub(r'</svg>\s*$', '', inner)
            if slug in BRAND_TINT:
                inner = re.sub(r'fill="[^"]*"', f'fill="{BRAND_TINT[slug]}"', inner)
                if 'fill="' not in inner:
                    inner = f'<g fill="{BRAND_TINT[slug]}">{inner}</g>'
            for ident in re.findall(r'\bid="([^"]+)"', inner):
                inner = inner.replace(f'id="{ident}"', f'id="{slug}-{ident}"')
                inner = inner.replace(f'url(#{ident})', f'url(#{slug}-{ident})')
                inner = inner.replace(f'href="#{ident}"', f'href="#{slug}-{ident}"')
            symbols.append(f'<symbol id="icon-{slug}" viewBox="0 0 {size} {size}">{inner}</symbol>')
    return "\n".join(symbols)


def tech_wall(mobile=False):
    names = {slug: name for _, icons in GROUPS for slug, name in icons}
    w, h = (360, 252) if mobile else (480, 252)
    icon_size, step = (36, 54) if mobile else (40, 68)
    body = ["<defs>" + icon_symbols() + "</defs>"]
    for index, (label, row) in enumerate(WALL_ROWS):
        y = 16 + index * 84
        body.append(text(w / 2, y, label, 11, MUTED, True, text_anchor="middle", letter_spacing=1.2))
        x = (w - ((len(row) - 1) * step + icon_size)) / 2
        for slug in row:
            body.append(f'<use href="#icon-{slug}" x="{x}" y="{y + 16}" width="{icon_size}" height="{icon_size}"/>')
            x += step
    description = ", ".join(names[slug] for _, row in WALL_ROWS for slug in row)
    return svg(w, h, "Tech Stack", "\n".join(body), "Technologies: " + description)


PROJECT_LOCATIONS = [("campus", BLUE), ("gate", CYAN), ("gym", PURPLE), ("civic", "#9DAEF4")]


def project_card(title, description, stack, index, mobile=False, animated=True):
    w, h = (480, 240) if mobile else (840, 184)
    location, accent = PROJECT_LOCATIONS[index]
    outline = step_outline(1, 1, w-2, h-10)
    body = [f'<defs><clipPath id="card-clip"><path d="{outline}"/></clipPath></defs>',
            f'<path d="{outline}" fill="{NAVY}"/>', '<g clip-path="url(#card-clip)">']
    if mobile:
        body.append('<g transform="translate(0 106)">'
                    + city(w, h-114, seed=80+index*17, accent=accent, location=location,
                           quiet_left=220, animated=animated, atmosphere=False, pace=30+index*3)
                    + '</g>')
    else:
        body.append(city(w, h-8, seed=80+index*17, accent=accent, location=location,
                         quiet_left=488, animated=animated, atmosphere=False, pace=30+index*3))
        # Solid sky behind the copy, while the city and railway continue below it.
        body.append(rect(16, 12, 480, 112, NAVY, 0, "none"))
    body += [text(24, 38, title, 28 if mobile else 26, weight=600),
             text(24, 70, description, 21 if mobile else 16, MUTED),
             text(24, 100, stack, 18 if mobile else 14, accent, True),
             text(24, 134 if mobile else 120, "Repository", 16 if mobile else 14, MUTED)]
    x, y = (122, 122) if mobile else (112, 108)
    body.append(f'<path d="M{x} {y+12}h3v-3h3v-3h3V{y+3}h-9V{y}h15v15h-3v-9h-3v3h-3v3h-3v3h-3Z" fill="{accent}"/>')
    body += ['</g>', f'<path d="{outline}" fill="none" stroke="{BORDER}" stroke-width="2"/>',
             f'<path d="M9 1h48" stroke="{accent}" stroke-width="2"/>']
    return svg(w, h, title, "\n".join(body), f"{description} Built with {stack}. View repository. "
               + "Illustrative pixel-city location with " + ("gentle train, traffic and window animation." if animated else "no animation."))


def portfolio(mobile=False, animated=True):
    w, h = (480, 208) if mobile else (840, 200)
    body = [frame(w, h), city(w, h, seed=104, accent=CYAN, animated=animated, pace=32)]
    # Image embeds keep native link behavior. These states only activate when the
    # SVG is viewed directly; GitHub does not forward pointer events into images.
    if animated:
        body.append('<style>'
                    '.button-face { transition:transform 120ms ease-out }'
                    'a:hover .button-face,a:focus .button-face { transform:translateY(2px) }'
                    'a:active .button-face { transform:translateY(6px) }'
                    '@media (prefers-reduced-motion:reduce) { .button-face { transition:none } }'
                    '</style>')
    bw, bh, top = (376, 112, 28) if mobile else (512, 104, 32)
    left = (w-bw)//2
    outline = step_outline(left, top, bw, bh)
    body += [f'<path d="{step_outline(left+6, top+8, bw, bh)}" fill="#12182A"/>',
             f'<path d="{step_outline(left, top+6, bw, bh)}" fill="#4B517D" stroke="#151B30" stroke-width="2"/>',
             '<a href="https://my-portfolio.jaudianhabib879.workers.dev/" aria-label="View my portfolio">',
             '<g class="button-face" shape-rendering="crispEdges">',
             f'<path d="{outline}" fill="#2D3451" stroke="{BLUE}" stroke-width="4"/>',
             f'<path d="M{left+12} {top+4}H{left+bw-12}M{left+4} {top+12}V{top+bh-12}" fill="none" stroke="{CYAN}" stroke-width="2"/>']
    if mobile:
        body.append(pixel_text("VIEW MY", (w-pixel_width("VIEW MY", 3))//2-12, top+18, 3, MUTED))
        body.append(pixel_text("PORTFOLIO", (w-pixel_width("PORTFOLIO", 4))//2-12, top+44, 4))
    else:
        body.append(pixel_text("VIEW MY PORTFOLIO", (w-pixel_width("VIEW MY PORTFOLIO", 4))//2-12, top+26, 4))
    body.append(text(w/2, top+bh-20, "Explore my work", 18, CYAN, text_anchor="middle"))
    x, y = (w//2+126, top+48) if mobile else (w//2+214, top+26)
    body.append(f'<path d="M{x} {y}h4v4h4v4h4v4h4v4h-4v4h-4v4h-4v4h-4Z" fill="{CYAN}"/>')
    body += ['</g></a>']
    return svg(w, h, "View my portfolio — explore my work", "\n".join(body),
               "Raised arcade button with pixel lettering, a night skyline, a passing train and traffic. "
               + ("The label stays still. A static picture source supports reduced-motion preferences." if animated else "Static reduced-motion edition."))


if __name__ == "__main__":
    outputs = {}
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        outputs[f"hero{suffix}.svg"] = hero(mobile)
        outputs[f"hero{suffix}-still.svg"] = hero(mobile, animated=False)
        outputs[f"tech-stack{suffix}.svg"] = tech_wall(mobile)
        outputs[f"portfolio{suffix}.svg"] = portfolio(mobile)
        outputs[f"portfolio{suffix}-still.svg"] = portfolio(mobile, animated=False)
    for index, (slug, title, description, stack) in enumerate(PROJECTS):
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            outputs[f"project-{slug}{suffix}.svg"] = project_card(title, description, stack, index, mobile)
            outputs[f"project-{slug}{suffix}-still.svg"] = project_card(title, description, stack, index, mobile, animated=False)
    write_assets(outputs)
    print(f"Generated {len(outputs)} TokyoNight profile assets.")

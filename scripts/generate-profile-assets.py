"""Generate self-contained TokyoNight SVG artwork. No external dependencies."""
import random
import re
from profile_theme import ASSETS, NAVY, BORDER, WHITE, MUTED, BLUE, CYAN, PURPLE, text, rect, frame, svg, write_assets, city_tile

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
    parts = []
    cursor = x
    for ch in value:
        glyph = PIXEL_FONT[ch]
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit != "0":
                    parts.append(f'<rect x="{cursor + c * cell}" y="{y + r * cell}" width="{cell}" height="{cell}" fill="{color}"/>')
        cursor += (len(glyph[0]) + 1) * cell
    return "\n".join(parts)


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


def skyline(w_cells, rows, cell, x0, y0, seed=20260927):
    """Deterministic pixel night skyline: navy towers, lit windows, ground line."""
    rng = random.Random(seed)
    back_fill, front_fill = "#2F3956", "#3B4666"
    back, front, lights = [], [], []
    x, towers = -3, []
    while x < w_cells + 3:
        bw, bh = rng.randint(8, 14), rng.randint(max(8, rows // 3), rows - 5)
        back.append(rect(x0 + x * cell, y0 + (rows - bh) * cell, bw * cell, bh * cell, back_fill, 0, "none"))
        towers.append((x, bw, rows - bh))
        x += bw + rng.randint(1, 3)
    for tx, tbw, top in sorted(towers, key=lambda t: t[2])[:2]:  # antenna beacons on the tallest
        cx = tx + tbw // 2
        for dy in range(1, 5):
            back.append(rect(x0 + cx * cell, y0 + (top - dy) * cell, cell, cell, back_fill, 0, "none"))
        lights.append(rect(x0 + cx * cell, y0 + (top - 5) * cell, cell, cell, CYAN, 0, "none"))
    x = -4
    while x < w_cells + 4:
        bw, bh = rng.randint(9, 17), rng.randint(max(5, rows // 4), rows - 10)
        fx, fy = x0 + x * cell, y0 + (rows - bh) * cell
        front.append(rect(fx, fy, bw * cell, bh * cell, front_fill, 0, "none"))
        for wy in range(2, bh - 2, 3):
            for wx in range(2, bw - 2, 3):
                if rng.random() < 0.18:
                    color = rng.choices((BLUE, CYAN, PURPLE, WHITE), weights=(10, 5, 3, 2))[0]
                    lights.append(rect(fx + wx * cell, fy + wy * cell, cell, cell, color, 0, "none"))
        x += bw + rng.randint(1, 2)
    ground = [rect(x0, y0 + (rows - 2) * cell, w_cells * cell, 2 * cell, "#414868", 0, "none")]
    for _ in range(max(4, w_cells // 30)):
        gx = rng.randint(0, w_cells - 6)
        ground.append(rect(x0 + gx * cell, y0 + (rows - 2) * cell, rng.randint(3, 6) * cell, cell, "#565F89", 0, "none"))
    return "\n".join(back + front + ground + lights)


def hero(mobile=False):
    if mobile:
        w, h, cell, name_cell = 600, 216, 4, 6
        sky_y, sky_cells, name_y = 104, 150, 52
        eyebrow_size, eyebrow_y, role_size, role_y = 12, 30, 15, 196
    else:
        w, h, cell, name_cell = 1200, 336, 7, 12
        sky_y, sky_cells, name_y = 152, 171, 64
        eyebrow_size, eyebrow_y, role_size, role_y = 14, 38, 21, 318
    body = ['<defs><linearGradient id="background" x2="1" y2="1">'
            '<stop stop-color="#24283B"/><stop offset="1" stop-color="#1A2130"/>'
            '</linearGradient></defs>' + rect(1, 1, w - 2, h - 2, "url(#background)", 18, BORDER)]
    body.append(text(32, eyebrow_y, "~/computer-science · web · software-engineering", eyebrow_size, "#565F89", True))
    body.append(text(w - 32, eyebrow_y, "</>", eyebrow_size, "#565F89", True, text_anchor="end"))
    avoid = [(24, name_y - 4, 32 + pixel_width(NAME, name_cell) + 34, name_y + 5 * name_cell + 4)]
    body.append(stars(w, eyebrow_y + 12, sky_y - 8, avoid))
    body.append(pixel_text(NAME, 32, name_y, name_cell, WHITE))
    cursor_x = 32 + pixel_width(NAME, name_cell) + name_cell
    body.append(f'<rect x="{cursor_x}" y="{name_y}" width="{2 * name_cell}" height="{5 * name_cell}" fill="{CYAN}"/>')
    body.append(skyline(sky_cells, 18, cell, (w - sky_cells * cell) // 2, sky_y))
    body.append(text(w / 2, role_y, "BSCS STUDENT · WEB DEVELOPER · ASPIRING SOFTWARE ENGINEER", role_size, CYAN, True, letter_spacing=1, text_anchor="middle"))
    return svg(w, h, "Habib Jaudian D.", "\n".join(body),
               "Pixel-art night skyline banner. Habib Jaudian D. — BSCS Student, Web Developer, Aspiring Software Engineer.")


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


def project_row(title, description, stack, mobile=False):
    w, h = (480, 164) if mobile else (840, 118)
    body = [text(24, 38, title, 28 if mobile else 25, weight=600),
            text(24, 76 if mobile else 67, description, 21 if mobile else 16, MUTED),
            text(24, 112 if mobile else 96, stack, 18 if mobile else 13, CYAN, True)]
    # A thin rule and a few pixels carry the city motif without making a card.
    body.append(f'<path d="M24 {h - 1}H{w - 24}" stroke="{BORDER}"/>')
    body.append(text(24 if mobile else w - 155, 144 if mobile else 96, "Repository", 16 if mobile else 13, MUTED))
    x, y = (118, 132) if mobile else (w - 55, 84)
    body.append(f'<path d="M{x} {y + 12}l12 -12m-12 0h12v12" fill="none" stroke="{CYAN}" stroke-width="2"/>')
    body.append(f'<path d="M{w - 71} {h - 1}v-8h8v-8h8v16h8v-24h8v24" fill="none" stroke="{BORDER}" stroke-width="2" shape-rendering="crispEdges"/>')
    return svg(w, h, title, "\n".join(body), f"{description} Built with {stack}. View repository.")


def portfolio(mobile=False, animated=True):
    w, h = (480, 152) if mobile else (840, 140)
    tile_width = 420
    body = [frame(w, h)]
    if animated:
        body.append('<style>'
            '@keyframes city-run { to { transform: translateX(-420px); } }'
            '.city-run { animation: city-run 42s linear infinite; }'
            '@media (prefers-reduced-motion: reduce) { .city-run { animation: none; } }'
                    '</style>')
    body += [f'<defs><clipPath id="city-clip"><rect width="{w}" height="{h}"/></clipPath>'
            f'<g id="city-tile">{city_tile()}</g></defs>',
            '<g clip-path="url(#city-clip)" aria-hidden="true">',
            f'<g transform="translate(0 {h - 116})" opacity=".65" shape-rendering="crispEdges">',
            '<g class="city-run">']
    for x in range(0, w + tile_width, tile_width):
        body.append(f'<use href="#city-tile" x="{x}"/>')
    body += ['</g></g></g>', rect(0, h - 4, w, 4, BORDER, 0, "none")]
    left, right = (w - 344) / 2, (w + 344) / 2
    body.append(f'<path d="M{left + 8} 20H{right - 8}v8h8v64h-8v8H{left + 8}v-8h-8V28h8Z" fill="{NAVY}" stroke="{BLUE}" stroke-width="2"/>')
    body.append(text(w / 2 - 12, 55, "VIEW PORTFOLIO", 24, WHITE, True, weight=700, text_anchor="middle"))
    body.append(text(w / 2, 82, "Explore my work", 18, CYAN, text_anchor="middle"))
    x = w / 2 + 125
    body.append(f'<path d="M{x} 56h4v-4h4v-4h4v-4h-12v-4h20v20h-4V48h-4v4h-4v4h-4v4h-4Z" fill="{CYAN}"/>')
    return svg(w, h, "View portfolio — explore my work", "\n".join(body),
               "View portfolio. A pixel skyline with a stationary label. "
               + ("The city scrolls softly; a static picture source supports reduced-motion preferences." if animated else "Static version for reduced-motion preferences."))


if __name__ == "__main__":
    outputs = {}
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        outputs[f"hero{suffix}.svg"] = hero(mobile)
        outputs[f"tech-stack{suffix}.svg"] = tech_wall(mobile)
        outputs[f"portfolio{suffix}.svg"] = portfolio(mobile)
        outputs[f"portfolio{suffix}-still.svg"] = portfolio(mobile, animated=False)
    for slug, title, description, stack in PROJECTS:
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            outputs[f"project-{slug}{suffix}.svg"] = project_row(title, description, stack, mobile)
    write_assets(outputs)
    print(f"Generated {len(outputs)} TokyoNight profile assets.")

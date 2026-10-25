"""Generate self-contained profile SVG artwork. No external dependencies."""
import argparse
import random
import re
from profile_theme import ASSETS, NAVY, BORDER, WHITE, MUTED, BLUE, CYAN, PURPLE, AFTER_HOURS, text, rect, frame, svg, write_assets
from pixel_city import Pixels, city, step_outline, after_hours_city

GROUPS = [
    ("Languages", [("html5", "HTML5"), ("css3", "CSS3"), ("javascript", "JavaScript"), ("php", "PHP"), ("java", "Java")]),
    ("Frameworks / UI", [("springboot", "Spring Boot"), ("tailwindcss", "Tailwind CSS"), ("bootstrap", "Bootstrap")]),
    ("Database", [("mysql", "MySQL")]),
    ("Tools", [("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code"), ("docker", "Docker"), ("laragon", "Laragon"), ("googleappsscript", "Google Apps Script")]),
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
    c = AFTER_HOURS
    if mobile:
        w, h, sky_y = 600, 464, 188
        names = [("HABIB", 32, 32, 9), ("JAUDIAN D.", 32, 98, 9)]
        label_y, label_cell = 160, 3
    else:
        w, h, sky_y = 1200, 440, 140
        names = [(NAME, 32, 36, 10)]
        label_y, label_cell = 104, 3
    body = [f'<path d="{step_outline(0, 0, w, h)}" fill="{c["sky"]}"/>',
            '<g shape-rendering="crispEdges">']
    for value, x, y, cell in names:
        body.append(pixel_text(value, x, y, cell, c["text"]))
    body.append(pixel_text("TOKYO AFTER HOURS", 32, label_y, label_cell, c["cyan"]))
    body.append(f'<g transform="translate(0 {sky_y})">'
                + after_hours_city(w, h-sky_y, mobile=mobile, animated=animated)
                + '</g>')
    body.append('</g>')
    return svg(w, h, "Habib Jaudian D.", "\n".join(body),
               "Tokyo After Hours. Stationary pixel lettering above a layered dark-blue skyline, "
               "Tokyo Tower, sparse warm windows and an elevated three-car train with a cyan stripe. "
               + ("Only the train moves; reduced motion shows the complete stationary train."
                  if animated else "Static edition with the complete train visible."))


# Local source icons retain their provenance. Display tints improve dark contrast.
BRAND_TINT = {"laragon": "#7DCFFF", "googleappsscript": "#7AA2F7",
              "github": WHITE, "mysql": CYAN, "springboot": "#9ECE6A",
              "instagram": PURPLE, "tiktok": CYAN, "linkedin": BLUE}


def icon_symbol(slug):
    raw = (ASSETS / "icons" / f"{slug}.svg").read_text(encoding="utf-8")
    view = re.search(r'viewBox="([^"]+)"', raw).group(1)
    inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner)
    if slug in BRAND_TINT:
        inner = re.sub(r'fill="[^"]*"', f'fill="{BRAND_TINT[slug]}"', inner)
        inner = f'<g fill="{BRAND_TINT[slug]}">{inner}</g>'
    for ident in re.findall(r'\bid="([^"]+)"', inner):
        inner = inner.replace(f'id="{ident}"', f'id="{slug}-{ident}"')
        inner = inner.replace(f'url(#{ident})', f'url(#{slug}-{ident})')
        inner = inner.replace(f'href="#{ident}"', f'href="#{slug}-{ident}"')
    return f'<symbol id="icon-{slug}" viewBox="{view}">{inner}</symbol>'


def labeled_icon(slug, label, social=False):
    # A real label accompanies each brand mark; independent images wrap in Markdown.
    height, size = (36, 20) if social else (30, 18)
    width = 40 + len(label) * 8
    body = [f'<path d="{step_outline(1, 1, width-2, height-2, 3)}" fill="{NAVY}"/>']
    if slug == "email":
        body.append(f'<path d="M9 11h20v14H9z M9 11l10 8 10-8" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
    else:
        body += ["<defs>" + icon_symbol(slug) + "</defs>",
                 f'<use href="#icon-{slug}" x="9" y="{(height-size)/2}" width="{size}" height="{size}"/>']
    body.append(text(36, height/2+5, label, 14, WHITE))
    return svg(width, height, label, "\n".join(body))


def project_card(title, mobile=False):
    w, h = (480, 64) if mobile else (840, 64)
    outline = step_outline(1, 1, w-2, h-2, 5)
    body = [f'<path d="{outline}" fill="{NAVY}" stroke="{BORDER}"/>',
            text(20, 41, title, 25 if mobile else 28, WHITE, weight=600)]
    # A small pixel corner is the only decoration; project prose lives in Markdown.
    body.append(f'<path d="M{w-31} 22h10v10h-4v-6h-6z" fill="{BLUE}"/>')
    return svg(w, h, title, "\n".join(body))


def footer(mobile=False):
    w = 480 if mobile else 840
    body = [frame(w, 68),
            f'<g transform="translate(0 -26)">{city(w, 96, seed=104, animated=False, atmosphere=False)}</g>',
            f'<path d="M0 67H{w}" stroke="{BORDER}"/>']
    return svg(w, 68, "Tokyo night skyline divider", "\n".join(body))


def generate_assets(hero_only=False):
    outputs = {}
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        outputs[f"hero{suffix}.svg"] = hero(mobile)
        outputs[f"hero{suffix}-still.svg"] = hero(mobile, animated=False)
        if hero_only:
            continue
        outputs[f"footer{suffix}.svg"] = footer(mobile)
        for slug, title, _, _ in PROJECTS:
            outputs[f"project-{slug}{suffix}.svg"] = project_card(title, mobile)
    if not hero_only:
        for _, icons in GROUPS:
            for slug, label in icons:
                outputs[f"tech/{slug}.svg"] = labeled_icon(slug, label)
        for slug, label in [("github", "GitHub"), ("linkedin", "LinkedIn"),
                            ("instagram", "Instagram"), ("tiktok", "TikTok"), ("email", "Email")]:
            outputs[f"social-{slug}.svg"] = labeled_icon(slug, label, social=True)
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hero-only", action="store_true", help="Regenerate only the four Tokyo After Hours hero variants")
    args = parser.parse_args()
    outputs = generate_assets(hero_only=args.hero_only)
    write_assets(outputs)
    print(f"Generated {len(outputs)} profile assets.")

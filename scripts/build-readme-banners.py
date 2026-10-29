"""Build raw, self-contained SVG geometry for the GitHub profile README.

The supplied collages guide composition; their JPEG pixels and watermarks are
not edited or embedded. Silkscreen's bitmap lettering is converted into paths.
"""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/readme"
FONT = ROOT / "assets/fonts/silkscreen-latin.ttf"
GROUND = "#0d1117"
INK = "#edf2f7"
ORANGE = "#ff8a00"
CYAN = "#76d8f0"


def lettering(value, x, y, size, color=INK):
    font = ImageFont.truetype(str(FONT), size)
    bounds = font.getbbox(value)
    mask = Image.new("L", (int(font.getlength(value)) + 2, bounds[3] - bounds[1] + 2))
    ImageDraw.Draw(mask).text((0, -bounds[1]), value, font=font, fill=255)
    runs = []
    for row in range(mask.height):
        start = None
        for col in range(mask.width + 1):
            on = col < mask.width and mask.getpixel((col, row)) > 127
            if on and start is None:
                start = col
            if not on and start is not None:
                runs.append(f"M{x+start} {y+row}h{col-start}v1h-{col-start}z")
                start = None
    return f'<path fill="{color}" d="{"".join(runs)}" aria-label="{escape(value)}"/>'


def box(x, y, size, color, opacity=1):
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" opacity="{opacity}"/>'


def document(width, height, title, description, body, motion=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="description">{escape(description)}</desc>\n'
            '<!-- Authored SVG source. Abstract square composition inspired by user-supplied references. '
            'Lettering derived from Silkscreen under SIL OFL; see assets/fonts/OFL-silkscreen.txt. -->\n'
            + motion + f'<rect width="{width}" height="{height}" fill="{GROUND}"/>\n'
            + body + '\n</svg>\n')


def hero(mobile=False):
    w, h = (600, 360) if mobile else (1200, 340)
    edge = 400 if mobile else 860
    grid = 40 if mobile else 48
    parts = [f'<rect x="{edge}" width="{w-edge}" height="{h}" fill="{ORANGE}"/>']
    # Dense orange dissolves into separated amber squares toward the dark text.
    palette = ["#ffb02e", "#ff6300", "#e34800", "#ffc65a", "#f99617"]
    for row in range(8):
        for col in range(5):
            x = edge + (col - 3) * grid
            y = row * grid
            if x < (350 if mobile else 710) or y >= h:
                continue
            if (row + col) % 4 == 0 or (col == 0 and row % 2):
                continue
            opacity = [0.15, 0.45, 0.72, 1, 1][col]
            parts.append(box(x, y, grid, palette[(row * 3 + col) % len(palette)], opacity))
    parts.append('<g class="pixels">')
    for x, y, size, shade in ([(320, 48, 20, "#ffb02e"), (360, 288, 24, "#ff6300")]
                             if mobile else [(644, 58, 24, "#ffb02e"), (686, 240, 24, "#ff6300"), (620, 282, 16, "#ffc65a")]):
        parts.append(box(x, y, size, shade, .62))
    parts.append('</g>')
    parts.append('<g shape-rendering="crispEdges">')
    if mobile:
        parts += [lettering("HABIB", 32, 64, 48), lettering("JAUDIAN D.", 32, 126, 40),
                  lettering("BSCS QCU", 32, 206, 22, CYAN), lettering("WEBDEVELOPER", 32, 244, 22, CYAN)]
    else:
        parts += [lettering("HABIB JAUDIAN D.", 56, 106, 48),
                  lettering("BSCS QCU WEBDEVELOPER", 56, 182, 22, CYAN)]
    parts.append('</g>')
    motion = ('<style>.pixels{animation:pixel-shift 9s ease-in-out infinite alternate}'
              '@keyframes pixel-shift{from{opacity:.7;transform:translateY(0)}to{opacity:1;transform:translateY(6px)}}'
              '@media(prefers-reduced-motion:reduce){.pixels{animation:none}}</style>\n')
    return document(w, h, "Habib Jaudian D. | BSCS QCU WEBDEVELOPER",
                    "Dark orange abstract pixel banner inspired by the first supplied reference. "
                    "Habib Jaudian D., BSCS student at Quezon City University and web developer.",
                    '\n'.join(parts), motion)


def connection(mobile=False):
    w, h = (600, 240) if mobile else (1200, 220)
    edge, unit = (100, 40) if mobile else (320, 44)
    parts = [f'<rect width="{edge}" height="{h}" fill="#101c30"/>']
    for row, col, shade, alpha in [(0,0,"#3f83bf",1),(0,1,"#67c7ef",1),(1,1,"#29437c",1),
                                   (1,2,"#3f83bf",.8),(2,2,"#76d8f0",.68),(3,1,"#67c7ef",.9),
                                   (4,0,"#29437c",1),(4,1,"#3f83bf",1),(4,2,"#67c7ef",.4)]:
        parts.append(box(edge + (col - 1) * unit, row * unit, unit, shade, alpha))
    parts.append('<g shape-rendering="crispEdges">')
    x = 220 if mobile else 590
    parts += [lettering("CONNECT", x, 72, 36, CYAN),
              lettering("LET'S BUILD", x, 134, 18), lettering("SOMETHING USEFUL.", x, 162, 18)]
    parts.append('</g>')
    return document(w, h, "Connect with Habib Jaudian D.",
                    "Blue and cyan modular squares inspired by the second supplied reference. "
                    "Connect. Let's build something useful. Contact links follow below.", '\n'.join(parts))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, source in {"profile-banner.svg": hero(), "profile-banner-mobile.svg": hero(True),
                         "connect-banner.svg": connection(), "connect-banner-mobile.svg": connection(True)}.items():
        (OUT / name).write_text(source, encoding="utf-8")
        print(name)

"""Build transparent, labeled brand logos and pixel headings for the README."""
import importlib.util
from html import escape
from pathlib import Path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


banners = module("readme_banners", "build-readme-banners.py")
brands = module("profile_brands", "generate-profile-assets.py")
GROUPS = [
    ("Frontend", "#76d8f0", [("html5", "HTML"), ("css3", "CSS"),
        ("javascript", "JavaScript"), ("tailwindcss", "Tailwind CSS"), ("bootstrap", "Bootstrap")]),
    ("Backend", "#ff8a00", [("php", "PHP"), ("java", "Java")]),
    ("Database", "#f4cd70", [("mysql", "MySQL")]),
    ("Tools", "#c5a0ef", [("git", "Git"), ("github", "GitHub"),
        ("docker", "Docker"), ("vscode", "VS Code")]),
]


def svg(width, height, title, description, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">\n'
            f'<title id="title">{escape(title)}</title><desc id="description">{escape(description)}</desc>\n'
            '<!-- Transparent SVG. Brand sources: assets/icons; attribution: assets/README.md. '
            'Silkscreen lettering is outlined under SIL OFL. -->\n'
            + body + '\n</svg>\n')


def label_width(label, size):
    return ImageFont.truetype(str(banners.FONT), size).getlength(label)


def technology(slug, label):
    width, height = 128, 94
    # Exactly 48px logo viewport; the 128px module never scales in the README.
    symbol = brands.icon_symbol(slug, flat=True)
    lettering = banners.lettering(label, round((width-label_width(label, 14))/2), 72, 14)
    return svg(width, height, label, f"{label} brand logo with pixel lettering.",
               f'<defs>{symbol}</defs><use href="#icon-{slug}" x="40" y="10" width="48" height="48"/>\n'
               f'<g shape-rendering="crispEdges">{lettering}</g>')


def heading(label, color):
    width = int(label_width(label, 20)) + 4
    return svg(width, 24, label, f"{label} technology group.",
               '<g shape-rendering="crispEdges">' + banners.lettering(label, 0, 4, 20, color) + '</g>')


def qualification(title, first, second, color):
    return svg(264, 48, title, title,
               '<g shape-rendering="crispEdges">'
               + banners.lettering(first, 0, 4, 20, color)
               + banners.lettering(second, 0, 30, 18, color) + '</g>')


def assets():
    output = {}
    for name, color, entries in GROUPS:
        output[f'heading-{name.lower()}.svg'] = heading(name, color)
        for slug, label in entries:
            output[f'tech-{slug}.svg'] = technology(slug, label)
    output['education-bscs.svg'] = qualification('BS Computer Science', 'BS COMPUTER', 'SCIENCE', '#ff8a00')
    output['education-tesda.svg'] = qualification('NC III — Web Development', 'NC III', 'WEB DEVELOPMENT', '#76d8f0')
    return output


if __name__ == '__main__':
    for name, source in assets().items():
        (ROOT / 'assets/readme' / name).write_text(source, encoding='utf-8')
        print(name)

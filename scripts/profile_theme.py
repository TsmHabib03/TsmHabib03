"""Shared TokyoNight Storm palette and SVG helpers."""
from html import escape
from pathlib import Path
import random
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY, PANEL, BORDER = "#24283B", "#292E42", "#414868"
WHITE, MUTED, BLUE, CYAN, PURPLE = "#D5DEFB", "#A9B1D6", "#7AA2F7", "#7DCFFF", "#BB9AF7"
SANS = "'Segoe UI', Arial, sans-serif"
MONO = "Consolas, 'Liberation Mono', monospace"


def text(x, y, value, size=20, color=WHITE, mono=False, weight=400, **attrs):
    extras = " ".join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k, v in attrs.items())
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" font-weight="{weight}" {extras}>{escape(str(value))}</text>')


def rect(x, y, w, h, fill=PANEL, radius=12, stroke=BORDER):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def frame(w, h):
    return rect(0, 0, w, h, NAVY, 0, "none")


def city_tile(width=420, height=112, seed=27):
    """A repeatable pixel skyline. Flat colors; all geometry stays inside the tile."""
    rng = random.Random(seed)
    parts = []
    for layer, fill in enumerate(("#2F3956", "#3B4666")):
        x = 0
        while x < width - 12:
            bw = min(rng.randrange(24, 49, 4), width - x)
            bh = rng.randrange(32, 81 if layer else 101, 4)
            top = height - bh
            parts.append(rect(x, top, bw, bh, fill, 0, "none"))
            if not layer and bw >= 32:
                parts.append(rect(x + 12, top - 12, 4, 12, fill, 0, "none"))
                parts.append(rect(x + 12, top - 16, 4, 4, BLUE, 0, "none"))
            if layer:
                for wy in range(top + 8, height - 8, 12):
                    for wx in range(x + 8, x + bw - 4, 12):
                        if rng.random() < .22:
                            parts.append(rect(wx, wy, 4, 4, rng.choice((BLUE, CYAN, PURPLE)), 0, "none"))
            x += bw + rng.choice((4, 8))
    return "\n".join(parts)


def city_scene(w, baseline, opacity=.3):
    tile = city_tile()
    return (f'<g opacity="{opacity}" shape-rendering="crispEdges" aria-hidden="true">'
            + "".join(f'<g transform="translate({x} {baseline - 112})">{tile}</g>'
                      for x in range(0, w, 420)) + '</g>')


def svg(w, h, title, body, description=""):
    source = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
              f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title description">\n'
              f'<title id="title">{escape(title)}</title>\n<desc id="description">{escape(description or title)}</desc>\n'
              + body + '\n</svg>\n')
    ET.fromstring(source)
    return source


def write_assets(files):
    # Validate every output before replacing any existing, known-good artwork.
    for source in files.values():
        ET.fromstring(source)
    for name, source in files.items():
        destination = ASSETS / name
        temporary = destination.with_suffix(".svg.tmp")
        temporary.write_text(source, encoding="utf-8")
        temporary.replace(destination)

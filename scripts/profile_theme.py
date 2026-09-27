"""Shared TokyoNight Storm palette and SVG helpers."""
from html import escape
from pathlib import Path
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
    return ('<defs><linearGradient id="background" x2="1" y2="1">'
            '<stop stop-color="#24283B"/><stop offset="1" stop-color="#263151"/>'
            '</linearGradient></defs>' + rect(1, 1, w - 2, h - 2, "url(#background)", 18))


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

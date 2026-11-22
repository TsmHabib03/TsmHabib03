"""Build the compact pixel footer. Install requirements-footer.txt and Chromium.

Pillow draws licensed local Gruppo/Geist lettering. Chromium rasterizes attributed
social SVG silhouettes at build time. The GIF plays once, then holds its final frame.
"""
from functools import lru_cache
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/readme'
FONTS = ROOT / 'assets/fonts'
BLUE = (0, 26, 255)
PALE = (238, 242, 254)
WHITE = (255, 255, 255)
SCALE = 2
FRAMES = 45
DELAYS = [70, 60, 70] * 15
CONTACTS = [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('github', 'GitHub'), ('email', 'Email')]
ORIGIN = ('Code-rendered by scripts/build-connect-footer.py. Design reference: Habib-supplied '
          '3a1c06422d22325cff077bd3ba93e87b.jpg. Original computed pixel-boundary motion. '
          'Gruppo and Geist: Google Fonts, SIL OFL. Facebook/GitHub silhouettes: Devicon, MIT. '
          'Instagram: Simple Icons, CC0. Email envelope authored in this generator.')


@lru_cache
def font(size, display=False):
    face = ImageFont.truetype(str(FONTS / ('gruppo-regular.ttf' if display else 'geist-variable.ttf')), size * SCALE)
    if not display:
        face.set_variation_by_axes([400])
    return face


def text(draw, value, xy, size, display=False):
    draw.text(tuple(v * SCALE for v in xy), value, font=font(size, display), fill=WHITE, anchor='lt')


def icon_source(slug):
    if slug == 'email':
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
                '<rect x="2" y="5" width="24" height="18" rx="2" fill="white"/>'
                '<path d="M3 6l11 9L25 6" fill="none" stroke="#001aff" stroke-width="1.7"/></svg>')
    raw = (ROOT / f'assets/marks/{slug}.svg').read_text(encoding='utf-8')
    raw = re.sub(r'fill="#[0-9a-fA-F]{6}"', 'fill="white"', raw)
    if slug == 'facebook':
        raw = raw.replace('fill="#fff"', 'fill="#001aff"')
    return raw


def social_icons():
    icons = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 128, 'height': 128}, device_scale_factor=2)
        for slug, _ in CONTACTS:
            page.set_content('<style>html,body{margin:0;background:transparent}svg{display:block;width:128px;height:128px}</style>' + icon_source(slug))
            icons[slug] = Image.open(BytesIO(page.screenshot(omit_background=True))).convert('RGBA')
        browser.close()
    return icons


def layout(mobile=False):
    return (600, 320) if mobile else (1200, 240)


def base_image(mobile, icons):
    w, h = layout(mobile)
    im = Image.new('RGB', (w * SCALE, h * SCALE), BLUE)
    draw = ImageDraw.Draw(im)
    if mobile:
        text(draw, "LET'S CONNECT", (30, 103), 64, display=True)
        text(draw, 'Build something useful.', (32, 165), 26)
        positions = [(52, 216), (332, 216), (52, 274), (332, 274)]
        icon_size, label_size = 38, 25
    else:
        text(draw, "LET'S CONNECT", (48, 110), 68, display=True)
        text(draw, 'Build something useful.', (52, 187), 23)
        positions = [(652, 116), (808, 116), (956, 116), (1108, 116)]
        icon_size, label_size = 48, 22
    for (slug, label), (x, y) in zip(CONTACTS, positions):
        icon = icons[slug].resize((icon_size * SCALE, icon_size * SCALE), Image.Resampling.LANCZOS)
        left = x if mobile else x - icon_size / 2
        im.paste(icon, (int(left * SCALE), y * SCALE), icon)
        if mobile:
            text(draw, label, (x + icon_size + 14, y + 8), label_size)
        else:
            label_width = draw.textlength(label, font=font(label_size)) / SCALE
            text(draw, label, (x - label_width / 2, 184), label_size)
    return im.resize((w, h), Image.Resampling.LANCZOS)


def frame(index, mobile, base):
    im = base.copy()
    draw = ImageDraw.Draw(im)
    w, _ = im.size
    cell = 10 if mobile else 12
    cols = math.ceil(w / cell)
    t = index / (FRAMES - 1)
    front = -0.15 + 1.30 * t
    for col in range(cols):
        hash_value = (col * 173 + col * col * 37 + 91) % 101
        row = 4 + int(hash_value > 25) + int(hash_value > 66)
        distance = (col / cols - front) / .055
        pulse = math.exp(-distance * distance) * math.sin(math.pi * t)
        row -= int(pulse > .38)
        top = row * cell
        x = col * cell
        draw.rectangle((x, 0, x + cell - 1, top - 1), fill=PALE)
        if hash_value % 4 == 0:
            draw.rectangle((x, top - 2 * cell, x + cell - 1, top - cell - 1), fill=BLUE)
        if hash_value % 7 == 0:
            draw.rectangle((x, top + cell, x + cell - 1, top + 2 * cell - 1), fill=PALE)
    for x in (22, w // 2, w - 22):
        y, r = (17, 5)
        draw.line((x - r, y, x - 2, y), fill=BLUE)
        draw.line((x + 2, y, x + r, y), fill=BLUE)
        draw.line((x, y - r, x, y - 2), fill=BLUE)
        draw.line((x, y + 2, x, y + r), fill=BLUE)
        draw.point((x, y), fill=BLUE)
    return im


def palette():
    colors = [BLUE, PALE, WHITE]
    colors += [tuple(round(c + (255 - c) * t) for c in BLUE) for t in np.linspace(0, 1, 253)]
    im = Image.new('P', (1, 1))
    im.putpalette([int(c) for color in colors for c in color])
    return im


def quantize(rgb, pal):
    result = rgb.quantize(palette=pal, dither=Image.Dither.NONE)
    pixels = np.array(result)
    source = np.asarray(rgb)
    for index, color in enumerate((BLUE, PALE, WHITE)):
        pixels[np.all(source == color, axis=2)] = index
    exact = Image.fromarray(pixels)
    exact.putpalette(pal.getpalette())
    return exact


def build():
    OUT.mkdir(exist_ok=True)
    icons, pal, outputs = social_icons(), palette(), []
    for mobile in (False, True):
        name = 'connect-banner' + ('-mobile' if mobile else '')
        base = base_image(mobile, icons)
        frames = [quantize(frame(i, mobile, base), pal) for i in range(FRAMES)]
        gif = OUT / f'{name}.gif'
        # Omitting the Netscape loop extension makes the animation play once.
        frames[0].save(gif, save_all=True, append_images=frames[1:], duration=DELAYS,
                       optimize=True, disposal=1, comment=ORIGIN.encode('utf-8'))
        metadata = PngImagePlugin.PngInfo()
        for key in ('Description', 'generation_prompt', 'impeccable:prompt'):
            metadata.add_text(key, ORIGIN)
        still = OUT / f'{name}-still.png'
        frame(FRAMES - 1, mobile, base).save(still, pnginfo=metadata, optimize=True)
        for path in (gif, still):
            outputs.append({'file': path.name, 'bytes': path.stat().st_size,
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        print(name, gif.stat().st_size, flush=True)
    (OUT / 'footer-provenance.json').write_text(json.dumps({
        'generator': 'scripts/build-connect-footer.py', 'origin': ORIGIN,
        'reference': 'User-supplied 3a1c06422d22325cff077bd3ba93e87b.jpg; design only, no reference pixels ship',
        'font_source': 'https://github.com/google/fonts/tree/main/ofl/gruppo',
        'font_identification': 'Gruppo is a licensed visual match; exact reference face is unconfirmed.',
        'support_font_source': 'https://github.com/google/fonts/tree/main/ofl/geist',
        'icon_attribution': 'assets/icons/LICENSE-devicon.txt (MIT), assets/icons/LICENSE-simple-icons.txt (CC0)',
        'duration_ms': sum(DELAYS), 'repeat': False, 'outputs': outputs,
    }, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    build()

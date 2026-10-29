"""Build reference-led SVG banners with portable smooth vector lettering.

Install fonttools and Pillow to rebuild. Open Sans is licensed under SIL OFL.
Contact slices are individually linked in supported GitHub HTML because links
inside SVG images cannot act as interactive image maps on a GitHub profile.
"""
from functools import lru_cache
from html import escape
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/readme'
FONT = ROOT / 'assets/fonts/open-sans-variable.ttf'
INK = '#edf2f7'
WHITE = '#ffffff'
BLACK = '#232323'
PALETTES = [
    ('orange', '#ff8000', ['#ffe269', '#ffb528', '#ff9700', '#ff5b00', '#ed2400']),
    ('blue', '#4098f3', ['#92e4fc', '#58c9f7', '#00dbe7', '#397ae4', '#7154ef']),
    ('purple', '#a000d9', ['#f290f6', '#da5deb', '#b02ddd', '#8500c3', '#5e0098']),
]


@lru_cache(maxsize=4)
def face(weight=600):
    font = instantiateVariableFont(TTFont(FONT), {'wght': weight, 'wdth': 100}, inplace=True)
    return font, font.getGlyphSet(), font.getBestCmap()


def label_width(value, size, weight=600):
    font, glyphs, cmap = face(weight)
    return sum(glyphs[cmap[ord(c)]].width for c in value) * size / font['head'].unitsPerEm


def lettering(value, x, y, size, color=INK, weight=600):
    """Place true Bezier glyph outlines; y is the top of visible lettering."""
    font, glyphs, cmap = face(weight)
    scale = size / font['head'].unitsPerEm
    top = 0
    for c in value:
        bounds = BoundsPen(glyphs)
        glyphs[cmap[ord(c)]].draw(bounds)
        if bounds.bounds:
            top = max(top, bounds.bounds[3])
    pen = SVGPathPen(glyphs)
    cursor = x
    for c in value:
        glyph = glyphs[cmap[ord(c)]]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, y + top * scale)))
        cursor += glyph.width * scale
    return f'<path fill="{color}" d="{pen.getCommands()}" aria-label="{escape(value)}"/>'


def document(width, height, title, description, body, motion=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">\n'
            f'<title id="title">{escape(title)}</title><desc id="description">{escape(description)}</desc>\n'
            '<!-- Authored rectangular geometry; user reference JPEGs are not embedded or edited. '
            'Open Sans glyph outlines: SIL OFL, assets/fonts/OFL-open-sans.txt. -->\n'
            + motion + body + '\n</svg>\n')


def scatter(width, height, index):
    """Overlapping squares from reference 1, mirrored in the blue variation."""
    name, field, colors = PALETTES[index]
    unit = height / 8
    edge = width * .50
    parts = [f'<rect width="{width}" height="{height}" fill="white"/>',
             f'<rect x="{edge}" width="{width-edge}" height="{height}" fill="{field}"/>']
    for row in range(8):
        for col in range(8):
            x = edge + (col - 3) * unit
            if col == 0 and row not in (2, 5, 6):
                continue
            if col == 1 and row in (0, 3, 7):
                continue
            if (col + row * 3) % 7 == 0:
                continue
            opacity = (.38, .58, .72, 1, .9, .8, .5, .25)[col]
            parts.append(f'<rect x="{x:.2f}" y="{row*unit:.2f}" width="{unit:.2f}" '
                         f'height="{unit:.2f}" fill="{colors[(row*3+col)%5]}" opacity="{opacity}"/>')
    shapes = ''.join(parts)
    return f'<g transform="translate({width} 0) scale(-1 1)">{shapes}</g>' if index == 1 else shapes


def hero(mobile=False):
    w, h = (600, 400) if mobile else (1200, 384)
    layers = []
    for index, (name, field, colors) in enumerate(PALETTES):
        parts = [scatter(w, h, index)]
        if mobile:
            parts = [f'<rect width="{w}" height="{h}" fill="white"/>',
                     '<g transform="translate(0 210)">' + scatter(w, 190, index) + '</g>']
            parts += [lettering('HABIB JAUDIAN D.', 32, 38, 43, BLACK, 700),
                      lettering('BSCS QCU', 34, 106, 26, BLACK, 400),
                      lettering('Building useful software,', 34, 154, 20, BLACK, 400),
                      lettering('one project at a time.', 34, 181, 20, BLACK, 400)]
            tx = 32 if index == 1 else 350
            parts += [lettering('WEB', tx, 267, 42, WHITE if index == 2 else BLACK, 700),
                      lettering('DEVELOPER', tx, 321, 25, WHITE if index == 2 else BLACK, 400)]
        else:
            x = 678 if index == 1 else 56
            tx = 56 if index == 1 else 960
            parts += [lettering('HABIB JAUDIAN D.', x, 76, 40, BLACK, 700),
                      lettering('BSCS QCU', x, 137, 25, BLACK, 400),
                      lettering('Building useful software,', x, 203, 19, BLACK, 400),
                      lettering('one project at a time.', x, 231, 19, BLACK, 400),
                      lettering('WEB', tx, 179, 46, WHITE if index == 2 else BLACK, 700),
                      lettering('DEVELOPER', tx, 239, 27, WHITE if index == 2 else BLACK, 400)]
        layers.append(f'<g class="variation {name}" opacity="{1 if index == 0 else 0}">'
                      + ''.join(parts) + '</g>')
    motion = ('<style>.orange{animation:orange-fade 18s ease-in-out infinite}'
              '.blue{animation:blue-fade 18s ease-in-out infinite}'
              '.purple{animation:purple-fade 18s ease-in-out infinite}'
              '@keyframes orange-fade{0%,27.778%,100%{opacity:1}33.333%,94.444%{opacity:0}}'
              '@keyframes blue-fade{0%,27.778%,66.667%,100%{opacity:0}33.333%,61.111%{opacity:1}}'
              '@keyframes purple-fade{0%,61.111%,100%{opacity:0}66.667%,94.444%{opacity:1}}'
              '@media(prefers-reduced-motion:reduce){.variation{animation:none}.orange{opacity:1}'
              '.blue,.purple{opacity:0}}</style>\n')
    return document(w, h, 'HABIB JAUDIAN D. | BSCS QCU WEBDEVELOPER',
                    'Orange, blue and purple square-banner variations fade every six seconds. '
                    'Habib Jaudian D., BSCS QCU web developer. Building useful software, one project at a time. '
                    'Reduced motion shows the complete orange variation.', ''.join(layers), motion)


def connect_ground(height=560):
    parts = [f'<rect width="1200" height="{height}" fill="white"/>',
             f'<rect width="380" height="{height}" fill="#080b1a"/>']
    pattern = [(0,0,'#468cc8'),(0,1,'#66c9f3'),(1,1,'#394586'),(1,2,'#468cc8'),
               (2,2,'#66c9f3'),(3,0,'#394586'),(3,1,'#468cc8'),
               (4,-1,'#394586'),(4,0,'#468cc8'),(4,2,'#468cc8')]
    for offset in range(0, height, 300):
        for row, col, color in pattern:
            parts.append(f'<rect x="{308+col*72}" y="{offset+row*60}" width="72" height="60" fill="{color}"/>')
    return ''.join(parts)


def connection(mobile=False):
    if mobile:
        width, height = 600, 440
        body = '<rect width="600" height="440" fill="white"/>'
        body += '<g transform="scale(.5)">' + connect_ground(240) + '</g>'
        body += lettering("LET'S", 22, 25, 35, WHITE, 700)
        body += lettering('CONNECT', 22, 73, 29, WHITE, 700)
        body += lettering('BUILD SOMETHING', 282, 31, 25, BLACK, 600)
        body += lettering('USEFUL.', 282, 70, 25, BLACK, 600)
        positions = [(170, 153), (450, 153), (170, 295), (450, 295)]
        icon_size, label_size, label_offset = 80, 30, 92
    else:
        width, height = 1200, 310
        body = connect_ground(height)
        body += lettering("LET'S", 44, 78, 49, WHITE, 700)
        body += lettering('CONNECT', 44, 148, 45, WHITE, 700)
        body += lettering('BUILD SOMETHING USEFUL.', 570, 42, 31, BLACK, 600)
        body += lettering('Choose a channel and say hello.', 570, 92, 21, BLACK, 400)
        positions = [(620, 153), (780, 153), (940, 153), (1100, 153)]
        icon_size, label_size, label_offset = 72, 25, 88
    for (slug, label), (center, top) in zip(CONTACTS, positions):
        body += contact_mark(slug, center-icon_size/2, top, icon_size)
        body += lettering(label, center-label_width(label, label_size)/2,
                          top+label_offset, label_size, BLACK)
    return document(width, height, 'Connect with Habib Jaudian D.',
                    "Let's connect. Build something useful. Facebook, Instagram, GitHub and Email "
                    'are together in this banner. Use the text links immediately below.', body)


CONTACTS = [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('github', 'GitHub'), ('email', 'Email')]


def contact_mark(slug, x, y, size):
    import re
    raw = (ROOT / 'assets/marks' / f'{slug}.svg').read_text(encoding='utf-8')
    inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
    inner = re.sub(r'<(?:title|desc)\b.*?</(?:title|desc)>', '', inner, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner)
    if slug == 'email':
        inner = '<rect x="3" y="6" width="22" height="16" rx="2" fill="#168bbd"/><path d="M4 7l10 8L24 7" fill="none" stroke="white" stroke-width="1.8"/>'
    else:
        tint = {'facebook': '#1877f2', 'instagram': '#a236b4', 'github': BLACK}[slug]
        inner = re.sub(r'fill="#[0-9a-fA-F]{6}"', f'fill="{tint}"', inner)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 28 28">{inner}</svg>'


def contact(slug, label, column, row, mobile=False):
    import re
    raw = (ROOT / 'assets/marks' / f'{slug}.svg').read_text(encoding='utf-8')
    inner = re.sub(r'^.*?<svg\b[^>]*>', '', raw, count=1, flags=re.S)
    inner = re.sub(r'<(?:title|desc)\b.*?</(?:title|desc)>', '', inner, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner)
    color = WHITE if column == 0 else BLACK
    crop_height = 300 if mobile else 170
    x, y = column * 600, 220 + row * crop_height
    center = 178 if column == 0 else 880
    body = connect_ground(820 if mobile else 560)
    if slug == 'email':
        inner = '<rect x="3" y="6" width="22" height="16" rx="2" fill="#168bbd"/><path d="M4 7l10 8L24 7" fill="none" stroke="white" stroke-width="1.8"/>'
    icon_size, font_size = (140, 64) if mobile else (56, 27)
    center = (178 if column == 0 else 900) if mobile else center
    body += f'<svg x="{center-icon_size/2}" y="{y+20}" width="{icon_size}" height="{icon_size}" viewBox="0 0 28 28">{inner}</svg>'
    body += lettering(label, center-label_width(label, font_size)/2, y+190 if mobile else y+97, font_size, color)
    return (document(600, crop_height, label, f'Contact Habib on {label}.', body)
            .replace(f'viewBox="0 0 600 {crop_height}"', f'viewBox="{x} {y} 600 {crop_height}"'))


def assets():
    result = {'profile-banner.svg': hero(), 'profile-banner-mobile.svg': hero(True),
              'connect-banner.svg': connection(), 'connect-banner-mobile.svg': connection(True)}
    for slug, label, column, row in [('facebook','Facebook',0,0), ('instagram','Instagram',1,0),
                                      ('github','GitHub',0,1), ('email','Email',1,1)]:
        result[f'connect-{slug}.svg'] = contact(slug, label, column, row)
        result[f'connect-{slug}-mobile.svg'] = contact(slug, label, column, row, True)
    return result


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for name, source in assets().items():
        (OUT / name).write_text(source, encoding='utf-8')
        print(name)

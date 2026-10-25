"""Small, deterministic pixel-city scenes for the profile's image-only SVGs.

Geometry is batched by color; motion uses SVG-local CSS, never scripts or filters.
"""
from collections import defaultdict
import random

from profile_theme import NAVY, BLUE, CYAN, PURPLE, WHITE, AFTER_HOURS

SKY = NAVY
DISTANT, MID, FRONT = "#29314B", "#303B58", "#394563"
SIDE, EDGE, DIM = "#212A40", "#526081", "#4A5779"


class Pixels:
    """Merge same-color rectangles into paths to keep detailed scenes small."""

    def __init__(self):
        self.paths = defaultdict(list)

    def box(self, x, y, w, h, color):
        x, y, w, h = (round(n) for n in (x, y, w, h))
        if w > 0 and h > 0:
            self.paths[color].append(f"M{x} {y}h{w}v{h}h{-w}z")

    def draw(self):
        return "".join(f'<path fill="{color}" d="{"".join(paths)}"/>'
                       for color, paths in self.paths.items())


def step_outline(x, y, w, h, cut=8):
    return (f"M{x+cut} {y}H{x+w-cut}V{y+cut}H{x+w}V{y+h-cut}"
            f"H{x+w-cut}V{y+h}H{x+cut}V{y+h-cut}H{x}V{y+cut}H{x+cut}Z")


def motion_css(w, animated, pace=24):
    if not animated:
        return ""
    return f'''<style>
@keyframes rail-pass {{ from {{ transform:translateX(-180px) }} to {{ transform:translateX({w+180}px) }} }}
@keyframes street-pass {{ from {{ transform:translateX({w+60}px) }} to {{ transform:translateX(-60px) }} }}
@keyframes cloud-drift {{ from {{ transform:translateX(-12px) }} to {{ transform:translateX(18px) }} }}
@keyframes window-light {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:.85 }} }}
@keyframes wet-light {{ from {{ opacity:.14 }} to {{ opacity:.3 }} }}
.train {{ animation:rail-pass {pace}s linear infinite; animation-delay:-7s }}
.car {{ animation:street-pass {pace+9}s linear infinite; animation-delay:-12s }}
.clouds {{ animation:cloud-drift 32s ease-in-out infinite alternate }}
.window-light {{ animation:window-light {pace/2:g}s ease-in-out infinite }}
.reflection {{ animation:wet-light 8s ease-in-out infinite alternate }}
@media (prefers-reduced-motion:reduce) {{ .train,.car,.clouds,.window-light,.reflection {{ animation:none }} }}
</style>'''


def moon(x, y):
    p = Pixels()
    # Stepped crescent, without a circular vector edge or a glow filter.
    p.box(x+8, y, 16, 4, "#8897BB")
    p.box(x+4, y+4, 24, 4, "#8897BB")
    p.box(x, y+8, 28, 16, "#8897BB")
    p.box(x+4, y+24, 24, 4, "#8897BB")
    p.box(x+8, y+28, 16, 4, "#8897BB")
    p.box(x+14, y, 14, 20, SKY)
    p.box(x+10, y+4, 18, 12, SKY)
    p.box(x+18, y+20, 10, 4, SKY)
    return p.draw()


def windows(p, rng, x, top, w, h, layer, accent, changing):
    stride = 10 if layer == 0 else 12
    for wy in range(int(top)+10, int(top+h)-6, stride):
        for wx in range(int(x)+8, int(x+w)-8, stride):
            chance = rng.random()
            color = DIM if chance < .35 else accent if chance < .55 else "#617396"
            if layer == 0:
                color = "#384565" if chance < .65 else "#4B597A"
            if chance < .76:
                p.box(wx, wy, 3 if layer == 0 else 4, 3 if layer == 0 else 5, color)
            if layer > 0 and .72 < chance < .79:
                changing.box(wx, wy, 4, 5, accent)


def architecture(w, h, seed, quiet_left, accent):
    rng = random.Random(seed)
    layers = []
    ground = h-40
    for layer, fill in enumerate((DISTANT, MID, FRONT)):
        p, changing = Pixels(), Pixels()
        x = -18 if layer == 0 else -8
        while x < w:
            bw = rng.randrange(36, 77, 4) if layer == 0 else rng.randrange(44, 89, 4)
            max_h = max(42, int(h*(.73 if layer == 0 else .59 if layer == 1 else .38)))
            bh = rng.randrange(24, max_h, 4)
            if quiet_left and x < quiet_left:
                bh = min(bh, 22 if layer == 2 else 32)
            top = ground-bh
            p.box(x, top, bw, bh, fill)
            p.box(x+bw-8, top+4, 8, bh-4, SIDE if layer else "#252E45")
            p.box(x+4, top-4, bw-12, 4, EDGE if layer == 2 else "#3E4A69")
            # Roof tanks, service rooms, railings, masts and stepped setbacks.
            kind = rng.randrange(4)
            if kind == 0:
                p.box(x+12, top-14, 18, 10, fill)
                p.box(x+10, top-16, 22, 3, EDGE)
                p.box(x+14, top-4, 3, 4, DIM)
            elif kind == 1:
                p.box(x+12, top-18, 2, 14, EDGE)
                p.box(x+8, top-14, 10, 2, DIM)
                changing.box(x+12, top-20, 2, 2, accent)
            elif kind == 2:
                p.box(x+8, top-10, bw-24, 6, fill)
                p.box(x+12, top-12, bw-32, 2, DIM)
            else:
                p.box(x+10, top-10, 12, 6, SIDE)
                p.box(x+26, top-10, 12, 6, SIDE)
            windows(p, rng, x, top, bw, bh, layer, accent, changing)
            if layer == 2 and bh > 36:
                # Window ledges and storefronts make foreground blocks feel inhabited.
                p.box(x+4, ground-16, bw-14, 3, EDGE)
                p.box(x+8, ground-12, 12, 12, "#63789B")
                p.box(x+10, ground-10, 8, 9, "#A0B2CE")
                p.box(x+24, ground-11, 16, 9, SIDE)
                p.box(x+26, ground-9, 12, 3, accent)
                if kind == 1:
                    # A small projecting neon sign: pixel strokes, no blurred halo.
                    p.box(x+bw-10, top+10, 10, 24, accent)
                    p.box(x+bw-8, top+12, 6, 20, SIDE)
                    for offset in (0, 6, 12):
                        p.box(x+bw-7, top+15+offset, 4, 2, PURPLE)
            x += bw+rng.choice((4, 8, 12))
        layers.append(p.draw() + f'<g class="window-light" opacity=".65">{changing.draw()}</g>')
    return "".join(layers)


def landmark_building(kind, x, ground, accent):
    """Illustrative locations, not depictions of a project's real premises."""
    p, lit = Pixels(), Pixels()
    if kind == "tower":
        # Lattice observation tower: stepped spire, decks and tapered supports.
        p.box(x+36, ground-152, 2, 34, EDGE)
        lit.box(x+36, ground-156, 2, 4, CYAN)
        for index in range(11):
            y = ground-120+index*10
            spread = 4+index*2
            p.box(x+36-spread, y, 3, 12, "#6E6599")
            p.box(x+36+spread, y, 3, 12, "#6E6599")
            if index % 2 == 0:
                p.box(x+36-spread, y+7, spread*2, 2, DIM)
        for y, width in ((ground-104, 34), (ground-56, 54)):
            p.box(x+38-width/2, y, width, 8, EDGE)
            p.box(x+40-width/2, y+2, width-4, 3, accent)
        p.box(x, ground-6, 80, 6, MID)
    else:
        height = {"campus":96, "gate":108, "gym":76, "civic":90}[kind]
        top = ground-height
        p.box(x, top, 124, height, FRONT)
        p.box(x+112, top+4, 12, height-4, SIDE)
        p.box(x-4, top-4, 128, 4, EDGE)
        p.box(x+8, ground-5, 104, 5, DIM)
        for row in range(3):
            for col in range(6):
                p.box(x+10+col*16, top+26+row*16, 8, 7, "#7388AD" if (row+col)%3 else accent)
                p.box(x+10+col*16, top+34+row*16, 10, 2, SIDE)
        p.box(x+8, top+4, 102, 16, SIDE)
        # Large storefront sign uses abstract pixel bars; project names remain in real text.
        if kind == "campus":
            p.box(x+14, top-18, 44, 14, MID)
            p.box(x+20, top-14, 32, 3, accent)
            p.box(x+96, top-28, 2, 24, DIM)
            p.box(x+98, top-28, 14, 8, PURPLE)
            for i in range(4):
                p.box(x+18+i*20, top+9, 12, 5, accent)
        elif kind == "gate":
            p.box(x+38, top-20, 44, 16, MID)
            # Pixel clock above a bright entrance, with a small scanner-style sign.
            p.box(x+52, top-18, 12, 12, DIM)
            p.box(x+57, top-16, 2, 5, WHITE)
            p.box(x+59, top-13, 3, 2, WHITE)
            for dx, dy in ((0,0),(8,0),(0,8),(10,10)):
                p.box(x+14+dx, top+7+dy, 4, 4, accent)
            p.box(x+42, ground-24, 34, 24, SIDE)
            p.box(x+46, ground-20, 26, 4, accent)
        elif kind == "gym":
            p.box(x+20, top-24, 84, 20, SIDE)
            p.box(x+20, top-24, 84, 2, accent)
            p.box(x+36, top-18, 4, 12, accent)
            p.box(x+42, top-20, 6, 16, accent)
            p.box(x+48, top-14, 24, 4, accent)
            p.box(x+72, top-20, 6, 16, accent)
            p.box(x+80, top-18, 4, 12, accent)
            p.box(x+14, top+8, 82, 3, accent)
            p.box(x+12, ground-26, 96, 16, SIDE)
            for col in range(5):
                p.box(x+16+col*18, ground-24, 12, 14, "#7891AD")
        else:
            # Civic arcade: stepped roofline and lit columns, without a literal seal.
            for i in range(4):
                p.box(x+8+i*12, top-4-i*4, 104-i*24, 4, EDGE)
            for col in range(5):
                p.box(x+14+col*20, top+30, 6, height-38, "#7082A1")
                p.box(x+12+col*20, top+26, 10, 4, accent)
            p.box(x+38, top+7, 44, 3, accent)
        lit.box(x+9, top+3, 100, 2, accent)
        p.box(x-8, ground, 140, 4, EDGE)
    return p.draw(), lit.draw()


def train_shape(accent):
    p = Pixels()
    p.box(0, 4, 142, 12, "#93A5C4")
    p.box(4, 0, 130, 4, "#677B9D")
    p.box(142, 8, 8, 8, "#93A5C4")
    p.box(0, 13, 148, 3, accent)
    for x in range(8, 134, 16):
        p.box(x, 5, 10, 5, "#263954")
        p.box(x, 5, 8, 2, "#B2C8D9")
    for x in (44, 92):
        p.box(x, 1, 3, 15, SIDE)
    for x in (12, 40, 68, 100, 126):
        p.box(x, 16, 6, 3, SIDE)
    p.box(146, 9, 4, 3, WHITE)
    return p.draw()


def city(w, h, *, seed=27, accent=CYAN, location="tower", quiet_left=0,
         animated=True, atmosphere=True, pace=24):
    """One clipped city stage with an elevated railway, wet street and a landmark."""
    rng = random.Random(seed+400)
    ground, rail_y, street_y = h-40, h-32, h-16
    body = [motion_css(w, animated, pace),
            f'<defs><clipPath id="scene-clip"><path d="M0 0H{w}V{h}H0Z"/></clipPath></defs>',
            '<g clip-path="url(#scene-clip)" shape-rendering="crispEdges" aria-hidden="true">']
    if atmosphere:
        body.append(moon(w-60, 8))
        clouds = Pixels()
        for x, y in ((w*.13, 14), (w*.5, 6), (w*.78, 26)):
            clouds.box(x+12, y, 54, 4, "#313B55")
            clouds.box(x, y+4, 90, 4, "#313B55")
            clouds.box(x+22, y+8, 94, 3, "#2C354E")
        body.append(f'<g class="clouds" opacity=".7">{clouds.draw()}</g>')
    distant_stars = Pixels()
    for _ in range(max(5, w//70)):
        x, y = rng.randrange(8, w-8), rng.randrange(4, max(8, h//3))
        if not quiet_left or x > quiet_left:
            distant_stars.box(x, y, 2, 2, DIM)
    body.append(distant_stars.draw())
    body.append(architecture(w, h, seed, quiet_left, accent))
    mark_x = round(w*.69) if location == "tower" else w-184
    roof_height = {"tower":156, "campus":124, "gate":128, "gym":100, "civic":110}[location]
    scale = min(1, (h-48)/roof_height)
    landmark, landmark_lights = landmark_building(location, 0, 0, accent)
    body.append(f'<g transform="translate({mark_x} {ground}) scale({scale:.3f})">{landmark}'
                f'<g class="window-light" opacity=".65">{landmark_lights}</g></g>')
    street = Pixels()
    street.box(0, ground+4, w, 5, "#1C253A")
    street.box(0, rail_y, w, 3, EDGE)
    street.box(0, rail_y+3, w, 5, "#20283D")
    for x in range(18, w, 82):
        street.box(x, rail_y+8, 4, 14, "#3F4D6C")
    street.box(0, street_y, w, 16, "#1B2235")
    street.box(0, street_y, w, 2, "#4D5A7B")
    for x in range(0, w, 42):
        street.box(x, h-7, 16, 1, "#434F6D")
    for x in range(28, w, 142):
        street.box(x, ground-16, 2, 28, EDGE)
        street.box(x-4, ground-18, 12, 2, DIM)
        street.box(x-2, ground-16, 8, 2, "#99B4C9")
    body.append(street.draw())
    # The static transform leaves a complete, visible train in the still assets.
    body.append(f'<g transform="translate(0 {rail_y-19})"><g class="train" transform="translate({w//4} 0)">{train_shape(accent)}</g></g>')
    car = Pixels()
    car.box(4, 0, 18, 4, "#7585AB")
    car.box(0, 4, 30, 7, "#526488")
    car.box(8, 1, 10, 3, "#B1C6D8")
    car.box(2, 10, 5, 3, SIDE)
    car.box(22, 10, 5, 3, SIDE)
    car.box(0, 5, 3, 3, WHITE)
    car.box(28, 5, 2, 3, PURPLE)
    body.append(f'<g transform="translate(0 {street_y+1})"><g class="car" transform="translate({w*3//4} 0)">{car.draw()}</g></g>')
    reflections = Pixels()
    for x in range(18, w, 44):
        reflections.box(x, h-4, rng.randrange(6, 22, 2), 1, accent)
        reflections.box(x+4, h-2, rng.randrange(4, 12, 2), 1, BLUE)
    body.append(f'<g class="reflection" opacity=".2">{reflections.draw()}</g></g>')
    return "\n".join(body)


# One train model drives all hero variants and the motion endpoints.
CARRIAGE_WIDTH, CARRIAGE_GAP, CARRIAGE_COUNT = 116, 8, 3
TRAIN_WIDTH = CARRIAGE_COUNT * CARRIAGE_WIDTH + (CARRIAGE_COUNT - 1) * CARRIAGE_GAP
TRAIN_HEIGHT, TRAIN_MARGIN, TRAIN_TRAVEL_PERCENT = 48, 12, 88


def train_positions(width):
    """Start and end are fully outside the clip; still position shows all cars."""
    if width < TRAIN_WIDTH + 2 * TRAIN_MARGIN:
        raise ValueError("Scene must fit the complete static train")
    return -TRAIN_WIDTH - TRAIN_MARGIN, width + TRAIN_MARGIN, (width - TRAIN_WIDTH) // 2


def commuter_train():
    """Three linked carriages, integer geometry, both cabs facing outward."""
    c = AFTER_HOURS
    cars = []
    for index in range(CARRIAGE_COUNT):
        p = Pixels()
        p.box(4, 6, 108, 32, c["steel"])
        p.box(0, 10, 116, 24, c["steel"])
        p.box(4, 4, 108, 4, c["roof"])
        for x in (24, 78):
            p.box(x, 0, 14, 4, c["roof"])
            p.box(x + 2, 0, 10, 2, c["edge"])
        # Door outlines and paired leaves are readable at mobile image scale.
        for x in (28, 76):
            p.box(x, 10, 14, 26, c["roof"])
            p.box(x + 2, 12, 10, 22, c["steel"])
            p.box(x + 6, 12, 2, 22, c["roof"])
            p.box(x + 2, 12, 4, 8, c["glass"])
            p.box(x + 8, 12, 4, 8, c["glass"])
        for x in (8, 46, 60, 96):
            p.box(x, 12, 12, 12, c["glass"])
            p.box(x + 2, 12, 8, 2, c["warm"])
        p.box(0, 28, 116, 4, c["cyan"])
        p.box(4, 36, 108, 4, c["roof"])
        p.box(14, 40, 88, 4, c["glass"])
        for x in (16, 24, 86, 94):
            p.box(x, 42, 8, 6, c["sky"])
            p.box(x + 2, 44, 4, 2, c["edge"])
        if index in (0, 2):
            cab_x = 0 if index == 0 else 110
            p.box(cab_x, 12, 6, 12, c["glass"])
            p.box(cab_x, 24, 4, 2, c["warm"] if index == 2 else c["edge"])
        cars.append(f'<g class="carriage" transform="translate({index * (CARRIAGE_WIDTH + CARRIAGE_GAP)} 0)">{p.draw()}</g>')
        if index < CARRIAGE_COUNT - 1:
            cars.append(f'<path fill="{c["glass"]}" d="M{(index+1)*CARRIAGE_WIDTH+index*CARRIAGE_GAP} 32h{CARRIAGE_GAP}v4h{-CARRIAGE_GAP}z"/>')
    return "".join(cars)


def tokyo_tower(center, ground):
    """Stepped Tokyo Tower: antenna, two decks, tapered lattice and splayed feet."""
    c, p = AFTER_HOURS, Pixels()
    top = ground - 192
    p.box(center - 2, top, 4, 32, c["warm"])
    p.box(center - 4, top + 30, 8, 12, c["text"])
    # Pixel lattice follows the taper, opening out below the main deck.
    for row in range(15):
        y = top + 42 + row * 10
        spread = 4 + row * 2 if row < 8 else 20 + (row - 8) * 4
        p.box(center - spread - 2, y, 4, 10, c["warm"])
        p.box(center + spread - 2, y, 4, 10, c["warm"])
        p.box(center - spread, y + 8, spread * 2, 2, c["roof"])
        # Cross-braces made from square pixels, avoiding smoothed diagonals.
        for step in range(0, spread * 2, 4):
            brace_y = y + round(step / (spread * 2) * 4) * 2
            p.box(center - spread + step, brace_y, 2, 2, c["warm"])
            p.box(center - spread + step, y + 8 - (brace_y - y), 2, 2, c["warm"])
    for y, width in ((top + 62, 28), (top + 116, 64)):
        p.box(center - width // 2, y, width, 8, c["warm"])
        p.box(center - width // 2 + 4, y + 2, width - 8, 2, c["text"])
        p.box(center - width // 2 + 4, y + 6, width - 8, 2, c["glass"])
    p.box(center - 52, ground - 4, 20, 4, c["warm"])
    p.box(center + 32, ground - 4, 20, 4, c["warm"])
    return p.draw()


def after_hours_skyline(w, ground, mobile):
    """Authored roof rhythm; seeded windows only, never random composition."""
    c, rng = AFTER_HOURS, random.Random(20261025)
    # x, width, height, rooftop kind. Values are on the same two-pixel grid.
    distant = [(0, 56, 100, 0), (68, 76, 140, 1), (156, 54, 108, 2),
               (222, 88, 168, 0), (324, 60, 116, 1), (402, 68, 148, 2),
               (488, 88, 100, 0)] if mobile else [
               (0, 70, 116, 0), (86, 90, 144, 1), (192, 64, 110, 2),
               (272, 82, 174, 0), (374, 72, 132, 1), (466, 94, 156, 2),
               (580, 60, 120, 0), (660, 100, 164, 1), (784, 66, 138, 2),
               (872, 58, 92, 0), (1060, 82, 148, 1), (1158, 60, 118, 0)]
    mid = [(0, 84, 80, 2), (110, 94, 106, 0), (232, 78, 88, 1),
           (342, 82, 74, 2), (494, 106, 78, 0)] if mobile else [
           (0, 112, 92, 2), (136, 90, 106, 0), (252, 112, 84, 1),
           (390, 80, 110, 2), (496, 120, 82, 0), (642, 100, 106, 1),
           (766, 110, 86, 2), (902, 70, 68, 0), (1080, 120, 98, 1)]
    front = [(0, 122, 48, 0), (154, 110, 58, 2), (302, 98, 42, 0),
             (498, 102, 50, 2)] if mobile else [
             (0, 132, 54, 0), (162, 114, 64, 2), (308, 144, 48, 0),
             (486, 124, 60, 2), (642, 132, 50, 0), (810, 104, 56, 2),
             (1080, 120, 52, 0)]
    layers = []
    for layer, (buildings, fill) in enumerate(zip((distant, mid, front), (c["distant"], c["mid"], c["front"]))):
        p = Pixels()
        for x, width, height, roof in buildings:
            top = ground - height
            p.box(x, top, width, height, fill)
            p.box(x + width - 8, top + 4, 8, height - 4, c["distant"])
            p.box(x + 4, top - 2, width - 8, 2, c["dim"] if layer == 2 else fill)
            if roof == 1:
                p.box(x + 14, top - 14, 2, 14, c["dim"])
                p.box(x + 10, top - 10, 10, 2, c["dim"])
            elif roof == 2:
                p.box(x + 12, top - 10, 22, 10, fill)
                p.box(x + 10, top - 12, 26, 2, c["dim"])
            for wy in range(top + 12, ground - 8, 14):
                for wx in range(x + 10, min(x + width - 10, w - 4), 14):
                    chance = rng.random()
                    if chance < .5:
                        p.box(wx, wy, 4, 6, c["warm"] if layer > 0 and chance < .12 else c["dim"])
        layers.append(p.draw())
    # Tower is behind the low foreground but in front of middle silhouettes.
    return layers[0] + layers[1] + tokyo_tower(456 if mobile else 996, ground) + layers[2]


def after_hours_city(w, h, *, mobile=False, animated=True):
    c = AFTER_HOURS
    start, end, still = train_positions(w)
    duration = 24 if mobile else 28
    # Start with the whole train visible; move linearly, then wait outside the clip.
    delay = -duration * (TRAIN_TRAVEL_PERCENT / 100) * (still - start) / (end - start)
    rail_y, ground = h - 44, h - 62
    body = []
    if animated:
        body.append(f'''<style>
@keyframes tokyo-rail-pass {{
  0% {{ transform:translateX({start}px) }}
  {TRAIN_TRAVEL_PERCENT}%,100% {{ transform:translateX({end}px) }}
}}
.tokyo-train {{ animation:tokyo-rail-pass {duration}s linear infinite; animation-delay:{delay:.6f}s }}
@media (prefers-reduced-motion:reduce) {{ .tokyo-train {{ animation:none }} }}
</style>''')
    body += [f'<defs><clipPath id="tokyo-scene-clip"><path d="M0 0H{w}V{h}H0Z"/></clipPath></defs>',
             '<g clip-path="url(#tokyo-scene-clip)" shape-rendering="crispEdges" aria-hidden="true">',
             after_hours_skyline(w, ground, mobile)]
    rail = Pixels()
    rail.box(0, rail_y, w, 4, c["roof"])
    rail.box(0, rail_y + 4, w, 10, c["mid"])
    rail.box(0, rail_y + 14, w, 2, c["edge"])
    rail.box(0, h - 8, w, 8, c["distant"])
    for x in range(28, w, 148):
        rail.box(x, rail_y + 16, 10, h - rail_y - 24, c["front"])
        rail.box(x - 8, rail_y + 16, 26, 4, c["front"])
    body += [rail.draw(), f'<g transform="translate(0 {rail_y - TRAIN_HEIGHT})"><g class="tokyo-train" transform="translate({still} 0)">{commuter_train()}</g></g>']
    # Static overhead line and sparse masts frame, rather than obscure, the train.
    masts = Pixels()
    masts.box(0, rail_y - 60, w, 2, c["dim"])
    for x in range(12, w, 296):
        masts.box(x, rail_y - 68, 4, 68, c["edge"])
        masts.box(x, rail_y - 68, 26, 2, c["edge"])
        masts.box(x + 24, rail_y - 68, 2, 10, c["dim"])
    body += [masts.draw(), '</g>']
    return "\n".join(body)

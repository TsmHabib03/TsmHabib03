"""Small, deterministic pixel-city scenes for the profile's image-only SVGs.

Geometry is batched by color; motion uses SVG-local CSS, never scripts or filters.
"""
from collections import defaultdict
import random

from profile_theme import NAVY, BLUE, CYAN, PURPLE, WHITE, AFTER_HOURS, ROOFTOP_NIGHT, CAT_COATS

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


# Rooftop profile scenes: each source cell is an integer rectangle.
ROOFTOP_SECTIONS = ("about", "focus", "stack", "projects", "connect")
PROFILE_SECTIONS = ("connect",)
TAIL_CYCLE = 14
WINDOW_CYCLES = (11, 17, 23)


def rooftop_motion(animated):
    if not animated:
        return ""
    return f'''<style>
@keyframes rooftop-tail {{
  0%,64%,100% {{ visibility:visible }}
  65%,99% {{ visibility:hidden }}
}}
@keyframes rooftop-tail-rise {{
  0%,64%,73%,90%,100% {{ visibility:hidden }}
  65%,72%,91%,99% {{ visibility:visible }}
}}
@keyframes rooftop-tail-curl {{
  0%,72%,81%,100% {{ visibility:hidden }}
  73%,80% {{ visibility:visible }}
}}
@keyframes rooftop-tail-return {{
  0%,80%,91%,100% {{ visibility:hidden }}
  81%,90% {{ visibility:visible }}
}}
.tail-rest {{ animation:rooftop-tail {TAIL_CYCLE}s steps(1,end) infinite }}
.tail-rise {{ animation:rooftop-tail-rise {TAIL_CYCLE}s steps(1,end) infinite }}
.tail-curl {{ animation:rooftop-tail-curl {TAIL_CYCLE}s steps(1,end) infinite }}
.tail-return {{ animation:rooftop-tail-return {TAIL_CYCLE}s steps(1,end) infinite }}
@keyframes rooftop-window {{ 0%,38%,44%,100% {{ opacity:1 }} 39%,43% {{ opacity:.22 }} }}
.lights-0 {{ animation:rooftop-window {WINDOW_CYCLES[0]}s steps(1,end) infinite; animation-delay:-3s }}
.lights-1 {{ animation:rooftop-window {WINDOW_CYCLES[1]}s steps(1,end) infinite; animation-delay:-9s }}
.lights-2 {{ animation:rooftop-window {WINDOW_CYCLES[2]}s steps(1,end) infinite; animation-delay:-15s }}
@media (prefers-reduced-motion:reduce) {{
 .cat-tail-pose,.flicker-window {{ animation:none }}
}}
</style>'''


def night_moon(x, y, cell):
    c, p = ROOFTOP_NIGHT, Pixels()
    spans = ((6,18),(4,20),(3,21),(2,22),(1,23),(1,23),
             (0,24),(0,24),(0,24),(0,24),(0,24),(0,24),
             (0,24),(0,24),(0,24),(0,24),(1,23),(1,23),
             (2,22),(3,21),(4,20),(6,18),(8,16),(10,14))
    for row,(left,right) in enumerate(spans):
        p.box(x+left*cell,y+row*cell,(right-left)*cell,cell,c["moon"])
    for col,row,width,height in ((3,5,2,11),(5,17,3,3),(8,20,8,2),(17,6,3,2),
                                  (16,9,3,3),(13,12,4,3),(9,15,4,3),(6,14,2,2)):
        p.box(x+col*cell,y+row*cell,width*cell,height*cell,c["moon-light"])
    for col,row,width,height in ((5,4,3,2),(8,6,2,2),(12,17,3,2),(18,14,2,3),(16,19,2,2)):
        p.box(x+col*cell,y+row*cell,width*cell,height*cell,c["moon-shade"])
    return p.draw()


def night_cat(x, floor, cell=3, coat="black"):
    """Seated back-view cat; shared silhouette and connected tail for each coat."""
    c, fur, p = ROOFTOP_NIGHT, CAT_COATS[coat], Pixels()
    top = floor-48*cell
    # Bands form the head, narrow neck, shoulders, broad haunches and paws.
    bands = ((0,4,12,14),(2,5,25,27),(4,8,11,28),(8,16,9,30),
             (16,20,11,28),(20,24,13,26),(24,28,11,28),(28,32,9,30),
             (32,36,7,32),(36,40,5,33),(40,43,4,34),(43,46,5,34),(46,48,9,31))
    for y0,y1,left,right in bands:
        p.box(x+left*cell,top+y0*cell,(right-left)*cell,(y1-y0)*cell,fur["base"])
    # Hand-placed patches stay inside the stepped body bands, without masks.
    if coat == "calico":
        patches = ((12,4,6,4),(10,8,9,7),(12,15,7,4),(14,20,8,4),
                   (11,25,9,5),(8,30,12,8),(6,38,13,5),(9,43,9,3))
        darks = ((23,4,4,4),(22,8,7,8),(21,16,6,3),(24,27,4,5),
                 (23,32,8,8),(25,40,7,5))
        for color, patches_for_color in ((fur["patch"], patches),(fur["dark"],darks)):
            for col,row,width,height in patches_for_color:
                p.box(x+col*cell,top+row*cell,width*cell,height*cell,color)
    elif coat == "orange":
        for col,row,width,height in ((14,7,3,7),(22,7,3,7),(12,17,14,2),
                                      (14,23,11,2),(10,29,8,2),(24,31,5,2),
                                      (7,36,10,2),(23,38,8,2)):
            p.box(x+col*cell,top+row*cell,width*cell,height*cell,fur["patch"])
        p.box(x+12*cell,top+45*cell,17*cell,2*cell,fur["rim"])
    for col,row,width,height in ((12,0,1,4),(11,4,1,4),(9,8,1,8),(10,16,1,3),
                                  (12,20,1,4),(10,24,1,4),(8,28,1,4),(6,32,1,4),
                                  (4,36,1,6),(5,43,2,2),(25,2,1,2),(26,4,1,1)):
        p.box(x+col*cell,top+row*cell,width*cell,height*cell,fur["rim"])
    for col,row,width,height in ((13,5,1,9),(11,15,1,3),(13,23,1,7),(9,32,1,9),
                                  (7,42,3,3),(28,37,2,7),(13,46,16,1)):
        p.box(x+col*cell,top+row*cell,width*cell,height*cell,fur["shade"])
    # Ear interiors, shoulder fur and split rear paws read at small display sizes.
    for col,row,width,height in ((12,4,2,2),(25,5,2,2)):
        p.box(x+col*cell,top+row*cell,width*cell,height*cell,fur["ear"])
    p.box(x+19*cell,top+44*cell,cell,3*cell,fur["shade"])
    shadow = Pixels()
    for col,row,width,height in ((8,48,26,2),(13,50,26,2),(20,52,23,2)):
        shadow.box(x+col*cell,top+row*cell,width*cell,height*cell,c["cat-shade"])
    body = [shadow.draw(), p.draw()]
    # The tail curls left along the ledge. Every pose connects to the same haunch.
    for index, name in enumerate(("rest", "rise", "curl", "return")):
        tail = Pixels()
        points = [(-18,44),(-14,46),(-10,48),(-6,50),(-2,51),(2,51),(6,50),(10,48),(14,46)]
        lifts = ((0,0,0,0,0,0,0,0,0),(-4,-3,-2,-1,0,0,0,0,0),
                 (-8,-7,-5,-3,-1,0,0,0,0),(-3,-4,-4,-3,-2,-1,0,0,0))[index]
        # Join steps before rim pixels so lifted poses stay a continuous tail.
        posed = [(col,row+lift) for (col,row),lift in zip(points,lifts)]
        for (_,y0),(right,y1) in zip(posed,posed[1:]):
            tail.box(x+right*cell,top+min(y0,y1)*cell,cell,(abs(y1-y0)+2)*cell,fur["base"])
        for segment, ((col,row),lift) in enumerate(zip(points,lifts)):
            tail.box(x+col*cell,top+(row+lift)*cell,5*cell,2*cell,fur["base"])
            if coat != "black" and segment%3 == 1:
                tail.box(x+(col+2)*cell,top+(row+lift)*cell,2*cell,2*cell,
                         fur["dark"] if coat == "calico" and segment == 4 else fur["patch"])
            tail.box(x+col*cell,top+(row+lift)*cell,2*cell,cell,fur["rim"])
        visibility = "visible" if index == 0 else "hidden"
        body.append(f'<g class="cat-tail-pose tail-{name}" visibility="{visibility}">{tail.draw()}</g>')
    return f'<g class="night-cat" data-coat="{coat}">'+"".join(body)+'</g>'


def cat_rooftop(x, floor, width, height):
    """A raised building roof with coping, deck seams and a shallow windowed facade."""
    c, p = ROOFTOP_NIGHT, Pixels()
    p.box(x,floor-6,width,height-floor+6,c["ledge"])
    p.box(x,floor-6,width,4,c["rail"])
    p.box(x+4,floor-2,width-8,22,c["cat-shade"])
    p.box(x,floor+20,width,4,c["edge"])
    p.box(x,floor+24,width,4,c["sky"])
    for seam in range(x+16,x+width-16,56):
        p.box(seam,floor+16,24,2,c["mid"])
        p.box(seam+12,floor+30,2,max(0,height-floor-30),c["mid"])
    if height-floor >= 40:
        for wx in range(x+22,x+width-22,48):
            p.box(wx,floor+32,16,8,c["sky"])
            p.box(wx+2,floor+34,4,4,c["warm"])
            p.box(wx+10,floor+34,4,4,c["window-dim"])
    return '<g class="cat-rooftop">'+p.draw()+'</g>'


def night_skyline(w, floor, height, seed):
    c = ROOFTOP_NIGHT
    rng = random.Random(seed)
    body = []
    for layer, color in enumerate((c["distant"],c["mid"],c["front"])):
        lamps = [Pixels() for _ in WINDOW_CYCLES]
        p, x = Pixels(), -20
        while x < w:
            width = rng.randrange(32,73,4)
            building_h = rng.randrange(max(20,height//3),max(24,height),4)
            top = floor-building_h + layer*8
            p.box(x,top,width,building_h,color)
            p.box(x+4,top-4,width-12,4,color)
            if rng.random()<.25:
                p.box(x+width-12,top-12,4,8,color)
            if layer:
                pattern = rng.randrange(4)
                for row,y in enumerate(range(top+8,floor-5,12)):
                    for col,wx in enumerate(range(max(2,x+8),min(w-4,x+width-4),10)):
                        if rng.random()>.55:
                            continue
                        bright = rng.random()<.7
                        shade = (c["warm"] if rng.random()<.035 else c["window"]) if bright else c["window-dim"]
                        ww,hh = (6,3) if pattern==0 else (3,6) if pattern==1 else (4,4)
                        if bright and rng.random()<.085:
                            lamps[(row+col+layer)%3].box(wx,y,ww,hh,shade)
                        else:
                            p.box(wx,y,ww,hh,shade)
                if pattern==3:
                    for y in range(top+9,min(top+38,floor-4),8):
                        p.box(x+width//3,y,width//2,2,c["window"])
            x += width+rng.randrange(0,9,4)
        body.append(p.draw())
        # Animate within the layer so nearer buildings still occlude its lamps.
        body.extend(f'<g class="flicker-window lights-{i}">{lamp.draw()}</g>' for i,lamp in enumerate(lamps))
    return "".join(body)


def rooftop_scene(w, h, *, mobile=False, animated=True, section=None):
    """Shared reference-led geometry, with deliberate compositions per section."""
    c, p = ROOFTOP_NIGHT, Pixels()
    index = ROOFTOP_SECTIONS.index(section)+1 if section else 0
    floor = h-(24 if section else 40)
    city_floor = floor-(10 if section else 26)
    city_height = (78 if mobile else 100) if section else (110 if mobile else 150)
    p.box(0,0,w,h,c["sky"])
    # Flat lower-sky band comes from the reference's tonal depth, not a gradient.
    band_y = 38 if section else (208 if mobile else 142)
    p.box(0,band_y,w,h-band_y,c["sky-low"])
    if section:
        moon_x = (w-94 if index%2 else 68)
        moon_y, moon_cell = 8,2
        cat_x = {"about":int(w*.57),"focus":int(w*.78),"stack":int(w*.24),
                 "projects":int(w*.70),"connect":int(w*.47)}[section]
        cat_cell = 2
    else:
        moon_x,moon_y,moon_cell = (w-96,24,3) if mobile else (w-160,24,4)
        cat_x,cat_cell = (int(w*.53),3) if mobile else (int(w*.52),3)
    # Pixel clouds stay clear of identity lettering; they do not drift.
    cloud_positions = ((w//3,16),(w*3//4,34)) if section else ((w//4,204 if mobile else 154),(w*3//4,190 if mobile else 138))
    for x,y in cloud_positions:
        p.box(x,y,38,4,c["distant"])
        p.box(x-12,y+4,72,4,c["mid"])
        p.box(x+16,y+8,76,4,c["distant"])
    rng = random.Random(300+index)
    star_min = 8 if section else (196 if mobile else 138)
    for _ in range(10 if section else 18):
        x,y = rng.randrange(12,w-12,4),rng.randrange(star_min,max(star_min+4,city_floor-city_height),4)
        p.box(x,y,2,2,c["window-dim"])
    body = [rooftop_motion(animated),p.draw(),night_moon(moon_x,moon_y,moon_cell),
            night_skyline(w,city_floor,city_height,seed=620+index)]
    ledge = Pixels()
    ledge.box(0,city_floor,w,4,c["rail"])
    ledge.box(0,city_floor+4,w,4,c["cat-shade"])
    ledge.box(0,city_floor+8,w,h-city_floor-8,c["ledge"])
    ledge.box(0,h-4,w,4,c["sky"])
    # Checker-like parapet edge and perspective seams, all actual pixels.
    for x in range(0,w,8):
        ledge.box(x,city_floor+4,4,2,c["sky"])
    for x in range(32,w,180):
        ledge.box(x,floor+12,104,2,c["cat-shade"])
    body.append(ledge.draw())
    if section == "focus":
        desk = Pixels()
        mx,my = (72 if mobile else 260),floor-82
        desk.box(mx,my,92,56,c["edge"])
        desk.box(mx+4,my+4,84,46,c["cat"])
        for dx,dy in ((14,16),(18,20),(14,24)):
            desk.box(mx+dx,my+dy,4,4,c["cyan"])
        desk.box(mx+32,my+28,24,2,c["window"])
        desk.box(mx+42,my+56,12,12,c["edge"])
        desk.box(mx+24,my+68,48,4,c["mid"])
        desk.box(mx-24,my+78,156,4,c["edge"])
        body.append(desk.draw())
    if section is None:
        cat_floor = h-60
        body.append(cat_rooftop(cat_x-92,cat_floor,284 if mobile else 340,h))
        body.append(night_cat(cat_x,cat_floor,cat_cell,coat="calico"))
    elif section == "connect":
        # Three distinct coats share one roof, with enough space for every tail.
        cat_floor = h-44
        trio_x = w//2-154
        body.append(cat_rooftop(trio_x-48,cat_floor,400,h))
        for offset, coat in ((0,"black"),(110,"orange"),(220,"calico")):
            body.append(night_cat(trio_x+offset,cat_floor,2,coat=coat))
    else:
        body.append(night_cat(cat_x,floor,cat_cell))
    return f'<g class="rooftop-scene" shape-rendering="crispEdges">'+"".join(body)+'</g>'


# One train model drives all hero variants and the motion endpoints.
CARRIAGE_WIDTH, CARRIAGE_GAP, CARRIAGE_COUNT = 116, 8, 3
TRAIN_WIDTH = CARRIAGE_COUNT * CARRIAGE_WIDTH + (CARRIAGE_COUNT - 1) * CARRIAGE_GAP
TRAIN_HEIGHT, TRAIN_MARGIN, TRAIN_TRAVEL_PERCENT = 48, 12, 88
CAT_TAIL_DURATION = 12


def pixel_moon(x, y, cell=4):
    """An authored stepped disc with a small cluster of crater pixels."""
    c, p = AFTER_HOURS, Pixels()
    spans = [(6, 10), (4, 12), (3, 13), (2, 14), (1, 15), (1, 15),
             (0, 16), (0, 16), (0, 16), (0, 16), (1, 15), (1, 15),
             (2, 14), (3, 13), (4, 12), (6, 10)]
    for row, (left, right) in enumerate(spans):
        p.box(x + left * cell, y + row * cell, (right-left) * cell, cell, c["moon"])
    for col, row, width, height in ((3, 8, 2, 3), (5, 11, 3, 2), (9, 12, 2, 1), (11, 4, 2, 2)):
        p.box(x + col * cell, y + row * cell, width * cell, height * cell, c["moon-shade"])
    return p.draw()


def rooftop_cat():
    """68px seated cat: pointed ears, haunches, paws and a separate stepped tail."""
    c, p = AFTER_HOURS, Pixels()
    # Back view: the cat looks across the city, with a moonlit silhouette.
    for x, y, width, height in ((20, 0, 6, 14), (42, 0, 6, 14), (24, 8, 20, 4),
                              (16, 12, 36, 18), (20, 30, 28, 12), (16, 42, 36, 14),
                              (12, 56, 44, 8), (12, 64, 48, 4)):
        p.box(x, y, width, height, c["cat"])
    for x, y, width, height in ((20, 0, 4, 12), (16, 12, 4, 16), (20, 30, 4, 12),
                              (16, 42, 4, 14), (12, 56, 4, 8), (44, 0, 4, 12),
                              (48, 12, 4, 16), (44, 30, 4, 12), (48, 42, 4, 14),
                              (26, 8, 16, 4)):
        p.box(x, y, width, height, c["moon-shade"])
    p.box(28, 44, 2, 20, c["glass"])
    tail = Pixels()
    for x, y, width, height in ((-10, 54, 6, 4), (-6, 58, 8, 4), (0, 62, 10, 4), (8, 64, 12, 4)):
        tail.box(x, y, width, height, c["cat"])
        tail.box(x, y, width, 2, c["roof"])
    return p.draw() + f'<g class="cat-tail">{tail.draw()}</g>'


def workstation():
    """Small pixel workstation, used once beside the engineering context."""
    c, p = AFTER_HOURS, Pixels()
    p.box(24, 4, 88, 52, c["edge"])
    p.box(28, 8, 80, 44, c["sky"])
    p.box(34, 16, 4, 4, c["cyan"])
    p.box(38, 20, 4, 4, c["cyan"])
    p.box(34, 24, 4, 4, c["cyan"])
    p.box(48, 26, 18, 2, c["text"])
    for x, y, width in ((34, 36, 28), (68, 36, 18), (34, 42, 46)):
        p.box(x, y, width, 2, c["roof"])
    p.box(62, 56, 12, 8, c["roof"])
    p.box(48, 64, 40, 4, c["edge"])
    p.box(12, 72, 120, 4, c["edge"])
    p.box(28, 68, 28, 4, c["roof"])
    p.box(116, 52, 12, 16, c["warm"])
    p.box(128, 56, 4, 8, c["warm"])
    return p.draw()


def skyline_accent(w=600, h=24):
    """A low, quiet roof rhythm: decorative divider, never a content panel."""
    c, p = AFTER_HOURS, Pixels()
    for x, width, height in ((0, 24, 8), (32, 18, 14), (58, 28, 10), (94, 20, 20),
                             (122, 26, 12), (158, 18, 8), (184, 30, 16)):
        p.box(x, h-height-2, width, height, c["front"])
    p.box(0, h-2, w, 2, c["edge"])
    p.box(98, h-16, 2, 4, c["warm"])
    return p.draw()


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
@keyframes cat-tail-rest {{
  0%,72%,100% {{ transform:translateY(0) }}
  80%,88% {{ transform:translateY(-2px) }}
}}
.cat-tail {{ animation:cat-tail-rest {CAT_TAIL_DURATION}s steps(1,end) infinite }}
@media (prefers-reduced-motion:reduce) {{ .tokyo-train,.cat-tail {{ animation:none }} }}
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
    # Cat sits on a low foreground rooftop, clear of the train and tower.
    cat_x, cat_ground = (340, ground-42) if mobile else (826, ground-56)
    body.insert(-1, f'<g class="rooftop-cat" transform="translate({cat_x} {cat_ground-68})">{rooftop_cat()}</g>')
    return "\n".join(body)

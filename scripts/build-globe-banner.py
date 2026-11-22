"""Render a reference-led identity with a seamless, coded geographic globe.

Build: python -m pip install -r scripts/requirements-globe.txt
       python scripts/build-globe-banner.py
Geist: SIL OFL. Natural Earth geography: public domain. No reference video
frames ship: ring coordinates, depth fading and rotation are calculated here.
"""
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from shapely import contains_xy
from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/readme"
FONT = ROOT / "assets/fonts"
BLUE = (43, 79, 247)
BRAND = (91, 110, 245)
INK = (10, 10, 10)
FRAMES = 150
DURATION_MS = [70, 60, 70] * 50  # GIF's 10ms clock; exactly 10 seconds.
SCALE = 2
PROVENANCE = (
    "Code-rendered by scripts/build-globe-banner.py. Design reference: user-supplied "
    "c03cb1d108749ec829ba93a8baa211d9.jpg. Motion reference: user-supplied "
    "7b0ab1b067f947787f822ff863e9a0eb.mp4. Geographic coordinates: Natural Earth "
    "ne_110m_land, public domain. Geist/Geist Mono: Google Fonts, SIL OFL. "
    "Bitstream h logo and favicon supplied by Habib."
)


@lru_cache
def font(size, mono=False, weight=400):
    face = ImageFont.truetype(str(FONT / ("geist-mono-variable.ttf" if mono else "geist-variable.ttf")), size * SCALE)
    face.set_variation_by_axes([weight])
    return face


def text(draw, value, xy, size, mono=False, weight=400):
    draw.text(tuple(v * SCALE for v in xy), value, font=font(size, mono, weight), fill=INK, anchor="lt")


def brand_mark(draw, x, y, size, color):
    """Exact 256-unit supplied habib-icon.svg geometry, approved white variant."""
    factor = size * SCALE / 256
    def pts(values):
        return [((x * SCALE + a * factor), (y * SCALE + b * factor)) for a, b in values]
    draw.polygon(pts([(52,28),(100,28),(100,104),(132,104),(132,88),(180,88),
                       (180,104),(204,104),(204,228),(156,228),(156,140),(100,140),(100,228),(52,228)]), fill=color)
    for a,b,w,r in [(120,52,24,3),(156,28,16,2),(188,56,12,2)]:
        draw.rounded_rectangle(pts([(a,b),(a+w,b+w)]), radius=r*factor, fill=color)


def layout(mobile=False):
    return ((600,760), (0,300,600,460), (300,530), 194) if mobile else ((1200,675),(670,0,530,675),(935,337.5),226)


def base_image(mobile=False):
    (w,h),(bx,by,bw,bh),_,_ = layout(mobile)
    im = Image.new("RGB", (w*SCALE,h*SCALE), "white")
    draw = ImageDraw.Draw(im)
    draw.rectangle((bx*SCALE,by*SCALE,w*SCALE,h*SCALE),fill=BLUE)
    favicon = Image.open(OUT / "habib-favicon.png").convert("RGB")
    fx,fy,fs = (36,38,28) if mobile else (60,116,28)
    im.paste(favicon.resize((fs*SCALE,fs*SCALE), Image.Resampling.LANCZOS),(fx*SCALE,fy*SCALE))
    text(draw,"TSMHABIB03",(fx+42,fy+5),19,mono=True)
    if mobile:
        text(draw,"Habib Jaudian D.",(34,111),60,weight=600)
        text(draw,"WEB DEVELOPER",(36,205),23,mono=True)
        text(draw,"BSCS · QUEZON CITY UNIVERSITY",(36,245),18,mono=True)
        brand_mark(draw,538,710,36,"white")
    else:
        text(draw,"Habib Jaudian D.",(58,249),68,weight=600)
        text(draw,"WEB DEVELOPER",(62,383),27,mono=True)
        text(draw,"BSCS · QUEZON CITY UNIVERSITY",(62,428),23,mono=True)
        brand_mark(draw,1137,606,36,"white")
    return im


@lru_cache
def land_points():
    data=json.loads((OUT / "globe-source/ne_110m_land.geojson").read_text(encoding="utf-8"))
    land=unary_union([shape(f["geometry"]) for f in data["features"]])
    # Staggered equal-distance rows reproduce the reference's open ring mesh.
    rows=[]
    for row,lat in enumerate(np.arange(-math.pi/2+.018,math.pi/2,.034)):
        count=max(1,round(2*math.pi*math.cos(lat)/.039))
        rows.extend((lat,-math.pi+2*math.pi*(col+.5*(row%2))/count) for col in range(count))
    latitude,longitude=np.array(rows).T
    keep=contains_xy(land,np.degrees(longitude),np.degrees(latitude))
    return latitude[keep],longitude[keep]


def frame(index, mobile=False, base=None):
    im=(base if base is not None else base_image(mobile)).copy()
    draw=ImageDraw.Draw(im)
    _,_,(cx,cy),radius=layout(mobile)
    latitude,longitude=land_points()
    angle=2*math.pi*(index % FRAMES)/FRAMES
    lon=longitude-angle+math.radians(15)
    x=np.cos(latitude)*np.sin(lon)
    y=np.sin(latitude)
    z=np.cos(latitude)*np.cos(lon)
    tilt=math.radians(-8)
    yt=y*math.cos(tilt)-z*math.sin(tilt)
    depth=y*math.sin(tilt)+z*math.cos(tilt)
    for p in np.argsort(depth):
        alpha=(.10+.90*float(depth[p])**.65) if depth[p] > 0 else .075
        color=tuple(round(c+(255-c)*alpha) for c in BLUE)
        px,py=(cx+radius*x[p])*SCALE,(cy-radius*yt[p])*SCALE
        rr=(1.85+.48*max(0,depth[p]))*SCALE*(radius/226)
        draw.ellipse((px-rr,py-rr,px+rr,py+rr),outline=color,width=SCALE)
    return im.resize((im.width//SCALE,im.height//SCALE),Image.Resampling.LANCZOS)


def fixed_palette():
    colors=[(255,255,255),INK,BLUE,BRAND]
    colors += [(v,v,v) for v in np.linspace(0,255,60).astype(int)]
    colors += [tuple(round(c+(255-c)*a) for c in BLUE) for a in np.linspace(0,1,120)]
    colors += [tuple(round(c+(255-c)*a) for c in BRAND) for a in np.linspace(0,1,40)]
    colors += [(int(v),int(v),int(v)) for v in np.linspace(0,255,32)]
    palette=Image.new("P",(1,1))
    palette.putpalette([int(c) for color in colors for c in color])
    return palette


def quantize_frame(rgb, palette):
    result = rgb.quantize(palette=palette, dither=Image.Dither.NONE)
    pixels = np.array(result)
    source = np.asarray(rgb)
    # Pillow's palette lookup approximates near-white cells. Preserve the
    # authored flat fields and brand colors exactly, including identity white.
    for index, color in enumerate([(255,255,255),INK,BLUE,BRAND]):
        pixels[np.all(source == color, axis=2)] = index
    exact = Image.fromarray(pixels)
    exact.putpalette(palette.getpalette())
    return exact


def build():
    OUT.mkdir(exist_ok=True)
    palette=fixed_palette()
    outputs=[]
    for mobile in (False,True):
        name="profile-globe"+("-mobile" if mobile else "")
        base=base_image(mobile)
        frames=[]
        for i in range(FRAMES):
            rgb=frame(i,mobile,base)
            if i==0:
                metadata=PngImagePlugin.PngInfo()
                metadata.add_text("Description",PROVENANCE)
                metadata.add_text("generation_prompt",PROVENANCE)
                metadata.add_text("impeccable:prompt",PROVENANCE)
                rgb.save(OUT/f"{name}-still.png",pnginfo=metadata,optimize=True)
            frames.append(quantize_frame(rgb,palette))
        gif=OUT/f"{name}.gif"
        frames[0].save(gif,save_all=True,append_images=frames[1:],duration=DURATION_MS,
                       loop=0,optimize=True,disposal=1,comment=PROVENANCE.encode("utf-8"))
        for path in [gif,OUT/f"{name}-still.png"]:
            outputs.append({"file":path.name,"bytes":path.stat().st_size,
                            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
        print(name, gif.stat().st_size,flush=True)
    (OUT/"globe-provenance.json").write_text(json.dumps({
        "generator":"scripts/build-globe-banner.py","origin":PROVENANCE,
        "font_source":"https://github.com/google/fonts/tree/main/ofl/geist",
        "mono_source":"https://github.com/google/fonts/tree/main/ofl/geistmono",
        "geography_source":"https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson",
        "geography_license":"https://www.naturalearthdata.com/about/terms-of-use/",
        "duration_ms":sum(DURATION_MS),"frames":FRAMES,"outputs":outputs,
        "font_identification":"Geist family matches the Next.js graphic; original JPEG font metadata is unavailable."
    },indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    build()

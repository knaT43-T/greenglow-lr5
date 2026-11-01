"""Генерация трёх локальных изображений товаров GreenGlow (1200x900)."""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2  # supersampling
W, H = 1200, 900
OUT = "assets/img"
os.makedirs(OUT, exist_ok=True)

FONT_SANS = "C:/Windows/Fonts/segoeui.ttf"
FONT_SANS_LIGHT = "C:/Windows/Fonts/segoeuil.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SERIF_ITALIC = "C:/Windows/Fonts/georgiai.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def vertical_gradient(size, top, bottom):
    w, h = size
    t = np.linspace(0, 1, h)[:, None, None]
    top = np.array(top, dtype=np.float32)
    bottom = np.array(bottom, dtype=np.float32)
    arr = top * (1 - t) + bottom * t
    return Image.fromarray(np.repeat(arr, w, axis=1).astype(np.uint8), "RGB")


def background():
    w, h = W * S, H * S
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # warm cream vertical gradient
    top = np.array(rgb("#FBF7EF"), dtype=np.float32)
    bottom = np.array(rgb("#E6DED0"), dtype=np.float32)
    t = (yy / h)[..., None]
    arr = top * (1 - t) + bottom * t

    # soft radial light from upper left
    cx, cy = w * 0.22, h * 0.10
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    light = np.clip(1 - dist / (w * 0.85), 0, 1) ** 2
    arr += light[..., None] * np.array([18, 16, 12], dtype=np.float32)

    # diagonal window light bands
    for start, width, strength in [(-0.1, 0.08, 10), (0.12, 0.04, 7), (0.55, 0.06, 6)]:
        band = ((xx / w) - start - (yy / h) * 0.25)
        mask = np.exp(-((band - 0.05) ** 2) / (2 * width ** 2))
        arr += mask[..., None] * strength

    # subtle grain
    rng = np.random.default_rng(42)
    arr += rng.normal(0, 2.0, (h, w, 1))
    arr = np.clip(arr, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "RGB")

    # surface: slightly darker table plane
    plane = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plane)
    pd.rectangle([0, int(h * 0.70), w, h], fill=(225, 216, 203, 190))
    plane = plane.filter(ImageFilter.GaussianBlur(1.5 * S))
    img = Image.alpha_composite(img.convert("RGBA"), plane).convert("RGB")

    # horizon soft shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([0, int(h * 0.695), w, int(h * 0.715)], fill=(120, 105, 85, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10 * S))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    return img


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius * S, fill=255)
    return mask


def paste_gradient(base, box, top, bottom, radius):
    x0, y0, x1, y1 = [v * S for v in box]
    w, h = int(x1 - x0), int(y1 - y0)
    grad = vertical_gradient((w, h), rgb(top), rgb(bottom))
    mask = rounded_mask((w, h), radius)
    base.paste(grad, (int(x0), int(y0)), mask)


def soft_shadow(base, box, blur=24, opacity=90, offset=(0, 18)):
    x0, y0, x1, y1 = [v * S for v in box]
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([x0 + offset[0] * S, y0 + offset[1] * S, x1 + offset[0] * S, y1 + offset[1] * S],
              fill=(60, 50, 38, opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
    base.alpha_composite(layer)


def add_highlight(base, box, radius, alpha=100):
    x0, y0, x1, y1 = [v * S for v in box]
    w, h = int(x1 - x0), int(y1 - y0)
    layer = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius * S, fill=(255, 255, 255, alpha))
    # fade highlight towards the right
    fade = Image.new("L", (w, h), 0)
    fd = ImageDraw.Draw(fade)
    for x in range(w):
        fd.line([(x, 0), (x, h)], fill=int(255 * max(0, 1 - x / (w * 0.55))))
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (w, h), 0), fade))
    base.alpha_composite(layer, (int(x0), int(y0)))


def text_center(draw, xy, text, fnt, fill, spacing=0):
    if spacing == 0:
        bbox = draw.textbbox((0, 0), text, font=fnt)
        draw.text((xy[0] - (bbox[2] - bbox[0]) / 2, xy[1]), text, font=fnt, fill=fill)
        return
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * S * (len(text) - 1)
    x = xy[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, xy[1]), ch, font=fnt, fill=fill)
        x += w + spacing * S


def leaf_layer(size, color, vein_color, alpha=255):
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = w / 2
    pts_left, pts_right = [], []
    for i in range(41):
        t = i / 40
        y = h * (0.04 + 0.92 * t)
        half = (w * 0.38) * (math.sin(math.pi * t) ** 0.75)
        pts_left.append((cx - half, y))
        pts_right.append((cx + half, y))
    d.polygon(pts_left + pts_right[::-1], fill=(*color, alpha))
    # vein
    d.line([(cx, h * 0.06), (cx, h * 0.94)], fill=(*vein_color, min(255, alpha)), width=max(1, S))
    for i in range(1, 8):
        t = i / 8
        y = h * (0.12 + 0.76 * t)
        half = (w * 0.30) * (math.sin(math.pi * t) ** 0.75)
        d.line([(cx, y), (cx - half, y - h * 0.05)], fill=(*vein_color, min(180, alpha)), width=max(1, S // 2))
        d.line([(cx, y), (cx + half, y - h * 0.05)], fill=(*vein_color, min(180, alpha)), width=max(1, S // 2))
    return layer


def paste_rotated(base, layer, center, angle, scale=1.0):
    if scale != 1.0:
        layer = layer.resize((int(layer.width * scale), int(layer.height * scale)), Image.LANCZOS)
    rotated = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    x = int(center[0] * S - rotated.width / 2)
    y = int(center[1] * S - rotated.height / 2)
    base.alpha_composite(rotated, (x, y))


def add_leaf(base, center, angle, length, color, vein, alpha=230, blur=1.5):
    w = int(length * 0.42)
    layer = leaf_layer((w, int(length)), color, vein, alpha)
    layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
    paste_rotated(base, layer, center, angle)


def label(base, box, title, subtitle, volume, accent="#8A9A86", title_size=30):
    x0, y0, x1, y1 = box
    # shadow
    soft_shadow(base, (x0, y0, x1, y1), blur=10, opacity=45, offset=(0, 4))
    # paper
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=4 * S, fill=(251, 247, 238, 255))
    base.alpha_composite(layer)
    d = ImageDraw.Draw(base)
    # thin border
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=4 * S,
                        outline=(44, 62, 45, 40), width=max(1, S // 2))
    cx = (x0 + x1) / 2 * S
    top = y0 * S
    text_center(d, (cx, top + 22 * S), "GREENGLOW", font(FONT_SANS_BOLD, 10), (*rgb(accent), 255), spacing=2.4)
    d.line([(x0 + 18) * S, top + 44 * S, (x1 - 18) * S, top + 44 * S], fill=(44, 62, 45, 45), width=max(1, S // 2))
    text_center(d, (cx, top + 56 * S), title, font(FONT_SERIF, title_size), (*rgb("#2C3E2D"), 255))
    text_center(d, (cx, top + 104 * S), subtitle, font(FONT_SANS, 9), (*rgb("#66705F"), 255), spacing=1.6)
    d.line([(x0 + 18) * S, top + 126 * S, (x1 - 18) * S, top + 126 * S], fill=(44, 62, 45, 45), width=max(1, S // 2))
    text_center(d, (cx, top + 136 * S), volume, font(FONT_SANS, 9), (*rgb("#66705F"), 255), spacing=1.2)


def finish(img, name):
    img = img.convert("RGB").resize((W, H), Image.LANCZOS)
    path = os.path.join(OUT, name)
    img.save(path, quality=92, subsampling=1, optimize=True)
    print(path)


def render_photo1():
    img = background().convert("RGBA")

    # botanical background
    add_leaf(img, (330, 420), -22, 430, rgb("#6F846C"), rgb("#A9B9A4"), alpha=235, blur=2.2)
    add_leaf(img, (285, 560), -55, 330, rgb("#7E927A"), rgb("#B7C6B1"), alpha=220, blur=2.4)
    add_leaf(img, (855, 500), 28, 380, rgb("#6F846C"), rgb("#A9B9A4"), alpha=220, blur=2.6)
    add_leaf(img, (905, 610), 58, 300, rgb("#7E927A"), rgb("#B7C6B1"), alpha=200, blur=2.6)

    # shadow
    soft_shadow(img, (390, 650, 810, 735), blur=28, opacity=105, offset=(0, 10))

    # jar body
    paste_gradient(img, (425, 350, 775, 690), "#F7FAF3", "#CFDBCA", 42)
    # glass side shading
    shade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rounded_rectangle([425 * S, 350 * S, 775 * S, 690 * S], radius=42 * S, outline=(120, 140, 115, 80), width=2 * S)
    sd.rounded_rectangle([650 * S, 360 * S, 775 * S, 680 * S], radius=40 * S, fill=(120, 140, 115, 38))
    img.alpha_composite(shade.filter(ImageFilter.GaussianBlur(6 * S)))
    # left highlight
    add_highlight(img, (440, 365, 520, 675), 30, alpha=150)

    # cream inside (subtle)
    cream = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cream)
    cd.rounded_rectangle([447 * S, 470 * S, 753 * S, 672 * S], radius=30 * S, fill=(250, 248, 239, 120))
    img.alpha_composite(cream.filter(ImageFilter.GaussianBlur(2 * S)))

    # lid
    paste_gradient(img, (410, 282, 790, 358), "#A5B39E", "#71826C", 16)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([410 * S, 282 * S, 790 * S, 358 * S], radius=16 * S, outline=(90, 105, 86, 90), width=max(1, S))
    # lid top ellipse
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    td.ellipse([418 * S, 270 * S, 782 * S, 312 * S], fill=(166, 181, 159, 255))
    img.alpha_composite(top)
    # lid ridges
    for x in range(430, 775, 11):
        d.line([(x * S, 292 * S), (x * S, 350 * S)], fill=(70, 84, 67, 40), width=max(1, S // 2))
    # lid highlight
    hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([445 * S, 276 * S, 700 * S, 298 * S], fill=(255, 255, 255, 75))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(4 * S)))

    # label
    label(img, (480, 405, 720, 585), "aloe", "MOISTURE CREAM", "50 ml  ·  natural care")
    # small leaf on label
    add_leaf(img, (600, 388), 0, 30, rgb("#8A9A86"), rgb("#6F846C"), alpha=255, blur=0.3)

    finish(img, "photo1.jpg")


def render_photo2():
    img = background().convert("RGBA")

    # botanicals and orange
    add_leaf(img, (330, 500), -35, 380, rgb("#6F846C"), rgb("#A9B9A4"), alpha=235, blur=2.0)
    add_leaf(img, (860, 520), 32, 360, rgb("#7E927A"), rgb("#B7C6B1"), alpha=220, blur=2.2)

    # orange slice
    cx, cy, r = 320, 650, 92
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=(232, 145, 52, 255))
    d.ellipse([(cx - r + 9) * S, (cy - r + 9) * S, (cx + r - 9) * S, (cy + r - 9) * S], fill=(250, 240, 219, 255))
    d.ellipse([(cx - r + 16) * S, (cy - r + 16) * S, (cx + r - 16) * S, (cy + r - 16) * S], fill=(238, 160, 62, 255))
    for i in range(8):
        a = i * math.pi / 4
        d.line([(cx * S, cy * S), ((cx + math.cos(a) * (r - 22)) * S, (cy + math.sin(a) * (r - 22)) * S)],
               fill=(250, 231, 191, 190), width=max(1, int(2.2 * S)))
    img.alpha_composite(layer)
    # orange highlight
    hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([(cx - r + 14) * S, (cy - r + 12) * S, (cx - 10) * S, (cy - 20) * S], fill=(255, 255, 255, 45))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(6 * S)))

    # shadow
    soft_shadow(img, (480, 650, 740, 735), blur=26, opacity=105, offset=(0, 10))

    # bottle body
    paste_gradient(img, (505, 395, 695, 690), "#C9823F", "#7B421B", 34)
    # glass highlight and shade
    shade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rounded_rectangle([505 * S, 395 * S, 695 * S, 690 * S], radius=34 * S, outline=(70, 36, 14, 100), width=2 * S)
    sd.rounded_rectangle([625 * S, 405 * S, 695 * S, 680 * S], radius=30 * S, fill=(55, 28, 10, 55))
    img.alpha_composite(shade.filter(ImageFilter.GaussianBlur(6 * S)))
    add_highlight(img, (518, 410, 580, 675), 26, alpha=120)

    # shoulder and neck
    shoulder = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shoulder)
    sd.polygon([(520 * S, 410 * S), (680 * S, 410 * S), (645 * S, 360 * S), (555 * S, 360 * S)], fill=(125, 68, 30, 255))
    img.alpha_composite(shoulder)
    paste_gradient(img, (560, 325, 640, 375), "#9A5525", "#6C3815", 10)

    # dropper cap
    paste_gradient(img, (552, 245, 648, 335), "#F5F0E4", "#D7CFBE", 12)
    d = ImageDraw.Draw(img)
    for y in range(258, 326, 9):
        d.line([(558 * S, y * S), (642 * S, y * S)], fill=(160, 150, 132, 70), width=max(1, S // 2))
    d.rounded_rectangle([552 * S, 245 * S, 648 * S, 335 * S], radius=12 * S, outline=(150, 140, 122, 80), width=max(1, S))
    # bulb
    bulb = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(bulb)
    bd.rounded_rectangle([568 * S, 210 * S, 632 * S, 252 * S], radius=18 * S, fill=(226, 218, 203, 255))
    img.alpha_composite(bulb)
    hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([576 * S, 216 * S, 604 * S, 246 * S], radius=10 * S, fill=(255, 255, 255, 80))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(3 * S)))

    # label
    label(img, (530, 445, 670, 615), "vitamin C", "BRIGHTENING SERUM", "30 ml  ·  15% vitamin C", accent="#B57A3C")

    finish(img, "photo2.jpg")


def render_photo3():
    img = background().convert("RGBA")

    # botanicals
    add_leaf(img, (315, 520), -30, 400, rgb("#6F846C"), rgb("#A9B9A4"), alpha=235, blur=2.0)
    add_leaf(img, (875, 500), 35, 380, rgb("#7E927A"), rgb("#B7C6B1"), alpha=220, blur=2.2)
    add_leaf(img, (930, 650), 65, 300, rgb("#6F846C"), rgb("#A9B9A4"), alpha=200, blur=2.4)

    # shadow
    soft_shadow(img, (460, 660, 760, 745), blur=28, opacity=105, offset=(0, 10))

    # bottle glass
    paste_gradient(img, (485, 380, 715, 700), "#F4F7EF", "#DDE5D7", 36)
    # oil fill
    oil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(oil)
    od.rounded_rectangle([497 * S, 500 * S, 703 * S, 688 * S], radius=26 * S, fill=(211, 164, 77, 170))
    od.rounded_rectangle([497 * S, 500 * S, 703 * S, 520 * S], radius=10 * S, fill=(226, 184, 101, 180))
    img.alpha_composite(oil)
    # glass edges/highlights
    shade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rounded_rectangle([485 * S, 380 * S, 715 * S, 700 * S], radius=36 * S, outline=(120, 140, 115, 90), width=2 * S)
    sd.rounded_rectangle([650 * S, 390 * S, 715 * S, 690 * S], radius=32 * S, fill=(110, 130, 105, 40))
    img.alpha_composite(shade.filter(ImageFilter.GaussianBlur(5 * S)))
    add_highlight(img, (500, 395, 565, 685), 28, alpha=150)

    # pump collar
    paste_gradient(img, (555, 335, 645, 390), "#9AA994", "#6F806B", 10)
    # pump head
    paste_gradient(img, (548, 282, 642, 340), "#A5B39E", "#71826C", 14)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([548 * S, 282 * S, 642 * S, 340 * S], radius=14 * S, outline=(80, 95, 77, 90), width=max(1, S))
    # spout
    spout = Image.new("RGBA", img.size, (0, 0, 0, 0))
    spd = ImageDraw.Draw(spout)
    spd.rounded_rectangle([620 * S, 296 * S, 690 * S, 320 * S], radius=10 * S, fill=(113, 130, 108, 255))
    img.alpha_composite(spout)
    # pump highlight
    hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([558 * S, 289 * S, 610 * S, 300 * S], radius=6 * S, fill=(255, 255, 255, 70))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(3 * S)))
    # tube inside
    tube = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(tube)
    td.rounded_rectangle([594 * S, 390 * S, 606 * S, 670 * S], radius=6 * S, fill=(240, 238, 228, 150))
    img.alpha_composite(tube)

    # label
    label(img, (515, 435, 685, 610), "cleansing oil", "HYDROPHILIC OIL", "150 ml  ·  gentle cleanse", accent="#8A9A86", title_size=22)

    # water droplets
    rng = random.Random(7)
    for i in range(9):
        x = rng.randint(380, 830)
        y = rng.randint(690, 780)
        rw = rng.randint(6, 14)
        rh = int(rw * 1.25)
        drop = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(drop)
        dd.ellipse([(x - rw) * S, (y - rh) * S, (x + rw) * S, (y + rh) * S], fill=(205, 222, 210, 130))
        dd.ellipse([(x - rw + 2) * S, (y - rh + 2) * S, (x - rw // 2) * S, (y - rh // 2) * S], fill=(255, 255, 255, 160))
        img.alpha_composite(drop.filter(ImageFilter.GaussianBlur(0.8 * S)))

    finish(img, "photo3.jpg")


if __name__ == "__main__":
    render_photo1()
    render_photo2()
    render_photo3()

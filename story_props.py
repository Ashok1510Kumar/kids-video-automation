#!/usr/bin/env python3
"""
STORY PROPS & NARRATIVE VISUAL EFFECTS
Procedurally creates transparent story props (Golden Egg, Cracking Egg, Baby Dragon,
Magic Cake, Balloons) to visually drive the story progression.
"""

import math
from PIL import Image, ImageDraw

def create_golden_egg(size=320) -> Image.Image:
    """Creates a glowing, shiny golden mystery egg."""
    img = Image.new("RGBA", (size, int(size * 1.25)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = img.size
    cx, cy = w // 2, h // 2

    # Outer egg silhouette
    rx, ry = int(w * 0.42), int(h * 0.46)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 215, 0), outline=(230, 160, 0), width=6)
    # Inner gold gradient shine
    draw.ellipse([cx - int(rx * 0.75), cy - int(ry * 0.80), cx + int(rx * 0.75), cy + int(ry * 0.70)], fill=(255, 238, 88))
    # Curving gloss highlight
    draw.ellipse([cx - int(rx * 0.55), cy - int(ry * 0.65), cx - int(rx * 0.15), cy - int(ry * 0.20)], fill=(255, 255, 255, 220))
    # Little sparkle stars on the shell
    for sx, sy in [(cx + 40, cy - 30), (cx - 30, cy + 50), (cx + 25, cy + 60)]:
        draw.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 255, 255))
    return img

def create_cracking_egg(size=340) -> Image.Image:
    """The golden egg wobbling with a dramatic zigzag crack and glowing light beams."""
    img = create_golden_egg(size)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    cx, cy = w // 2, h // 2

    # Zigzag crack down the middle
    crack_pts = [
        (cx - 10, cy - 80),
        (cx + 25, cy - 40),
        (cx - 30, cy),
        (cx + 35, cy + 40),
        (cx - 15, cy + 90)
    ]
    draw.line(crack_pts, fill=(255, 64, 129), width=8)
    draw.line(crack_pts, fill=(255, 255, 255), width=4)

    # Glowing light rays emerging from the crack
    for ang in [0.2, 0.8, 1.4, 2.0, 2.6, 3.2]:
        lx = cx + int(100 * math.cos(ang))
        ly = cy + int(100 * math.sin(ang))
        draw.line([(cx, cy), (lx, ly)], fill=(255, 255, 255, 180), width=3)
    return img

def create_baby_dragon_reveal(size=380) -> Image.Image:
    """Cute baby glitter dragon with purple wings bursting out with sparkles!"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Purple dragon body
    draw.ellipse([cx - 75, cy - 40, cx + 75, cy + 95], fill=(186, 104, 200), outline=(142, 36, 170), width=5)
    # Creamy tummy
    draw.ellipse([cx - 45, cy - 5, cx + 45, cy + 85], fill=(243, 229, 245))

    # Cute Sparkly Wings
    draw.ellipse([cx - 150, cy - 65, cx - 60, cy + 15], fill=(225, 190, 231), outline=(142, 36, 170), width=4)
    draw.ellipse([cx + 60, cy - 65, cx + 150, cy + 15], fill=(225, 190, 231), outline=(142, 36, 170), width=4)

    # Round Cute Head
    draw.ellipse([cx - 90, cy - 130, cx + 90, cy + 5], fill=(186, 104, 200), outline=(142, 36, 170), width=5)
    # Dragon horns
    draw.polygon([(cx - 60, cy - 110), (cx - 85, cy - 165), (cx - 35, cy - 120)], fill=(255, 238, 88), outline=(245, 124, 0))
    draw.polygon([(cx + 60, cy - 110), (cx + 85, cy - 165), (cx + 35, cy - 120)], fill=(255, 238, 88), outline=(245, 124, 0))

    # Big Anime Eyes
    for ex in [cx - 38, cx + 38]:
        draw.ellipse([ex - 18, cy - 75, ex + 18, cy - 39], fill=(45, 20, 50))
        draw.ellipse([ex - 8, cy - 70, ex + 2, cy - 56], fill=(255, 255, 255))
        draw.ellipse([ex + 2, cy - 50, ex + 8, cy - 44], fill=(255, 255, 255))

    # Happy Open Mouth & Pink Tongue
    draw.chord([cx - 24, cy - 35, cx + 24, cy + 5], start=0, end=180, fill=(194, 24, 91))
    draw.chord([cx - 14, cy - 18, cx + 14, cy + 3], start=0, end=180, fill=(255, 128, 171))

    # Rosy Cheeks
    draw.ellipse([cx - 65, cy - 48, cx - 35, cy - 28], fill=(255, 128, 171, 190))
    draw.ellipse([cx + 35, cy - 48, cx + 65, cy - 28], fill=(255, 128, 171, 190))

    return img

def create_magic_cake(size=360) -> Image.Image:
    """Giant fluffy rainbow birthday cake with pastel layers and strawberry glaze."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Bottom Cake Layer (Vanilla sponge)
    draw.rounded_rectangle([cx - 140, cy + 30, cx + 140, cy + 130], radius=20, fill=(255, 243, 224), outline=(240, 160, 120), width=5)
    # Middle Strawberry Layer
    draw.rounded_rectangle([cx - 110, cy - 35, cx + 110, cy + 40], radius=18, fill=(248, 187, 208), outline=(236, 64, 122), width=5)
    # Top Mint Layer
    draw.rounded_rectangle([cx - 80, cy - 90, cx + 80, cy - 25], radius=15, fill=(178, 235, 242), outline=(0, 188, 212), width=5)

    # Frosting drips
    for dx in range(cx - 120, cx + 130, 30):
        draw.ellipse([dx - 12, cy + 30, dx + 12, cy + 54], fill=(255, 128, 171))

    # Birthday Candle & Glow
    draw.rectangle([cx - 8, cy - 130, cx + 8, cy - 90], fill=(255, 238, 88))
    # Flame
    draw.ellipse([cx - 12, cy - 155, cx + 12, cy - 130], fill=(255, 87, 34))
    draw.ellipse([cx - 6, cy - 150, cx + 6, cy - 135], fill=(255, 235, 59))
    return img

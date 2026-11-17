#!/usr/bin/env python3
"""
RICKS CLIPS ENVIRONMENT & VISUAL PROPS ENGINE (@RicksClips3000 Style)
Builds stylized 3D workshop/studio environments and crisp technical diagrams/props:
- Modern engineering studio / workshop with depth-of-field lighting
- Technical props: expanding rails, stress vectors, bronze dragon urn
- Cinematic camera snap-zooms
"""

import math
from PIL import Image, ImageDraw, ImageFilter

def create_studio_workshop_environment(width=720, height=1280) -> Image.Image:
    """Creates a moody, cinematic engineering studio / workshop interior."""
    bg = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)

    # 1. Moody studio wall gradient (Slate Navy to Deep Charcoal)
    for y in range(860):
        ratio = y / 860.0
        r = int(24 + 18 * ratio)
        g = int(32 + 20 * ratio)
        b = int(44 + 22 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Blueprint grid / architectural lines on the wall
    for gx in range(40, width, 60):
        draw.line([(gx, 60), (gx, 840)], fill=(45, 60, 80, 70), width=1)
    for gy in range(80, 840, 60):
        draw.line([(30, gy), (width - 30, gy)], fill=(45, 60, 80, 70), width=1)

    # Warm overhead studio spotlight beam (soft radial glow)
    draw.ellipse([width // 2 - 280, 80, width // 2 + 280, 680], fill=(255, 235, 180, 28))

    # 2. Polished Studio Floor (Smooth reflective wood/concrete)
    for y in range(860, height):
        ratio = (y - 860.0) / (height - 860.0)
        r = int(50 + 40 * ratio)
        g = int(45 + 35 * ratio)
        b = int(40 + 30 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Floor baseboard / trim line
    draw.rectangle([(0, 854), (width, 862)], fill=(30, 25, 20))

    # Soft ambient depth blur
    bg = bg.filter(ImageFilter.GaussianBlur(radius=1.8))
    return bg

def create_railroad_diagram_prop(size=(380, 280), hot_sun_kink=False) -> Image.Image:
    """Visual diagram showing steel rails with expansion gap or buckled sun kink."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2

    # Container pill card
    draw.rounded_rectangle([10, 10, w - 10, h - 10], radius=20, fill=(33, 37, 43, 230), outline=(97, 175, 239), width=4)

    if not hot_sun_kink:
        # Normal Rails with Gap
        draw.text((cx, 35), "EXPANSION GAP (1.5mm)", fill=(97, 175, 239), anchor="mm")
        # Wooden ties
        for tx in range(40, w - 40, 50):
            draw.rectangle([tx, cy - 35, tx + 25, cy + 35], fill=(139, 115, 85), outline=(90, 70, 50), width=2)
        # Steel Rails
        draw.line([(30, cy - 14), (cx - 15, cy - 14)], fill=(200, 210, 220), width=10)
        draw.line([(cx + 15, cy - 14), (w - 30, cy - 14)], fill=(200, 210, 220), width=10)
        draw.line([(30, cy + 14), (cx - 15, cy + 14)], fill=(200, 210, 220), width=10)
        draw.line([(cx + 15, cy + 14), (w - 30, cy + 14)], fill=(200, 210, 220), width=10)
        # Yellow measurement arrows
        draw.line([(cx - 12, cy - 40), (cx + 12, cy - 40)], fill=(255, 214, 0), width=3)
        draw.text((cx, cy + 65), "Safe in Summer", fill=(152, 195, 121), anchor="mm")
    else:
        # Buckled Sun Kink (Dangerous Jagged S-curve)
        draw.text((cx, 35), "HEAT BUCKLING ('SUN KINK')", fill=(224, 108, 117), anchor="mm")
        # Overheated glowing red/orange twisted rails
        kink_pts_1 = [(30, cy - 14), (cx - 60, cy - 14), (cx - 10, cy - 45), (cx + 40, cy + 30), (cx + 80, cy - 14), (w - 30, cy - 14)]
        kink_pts_2 = [(30, cy + 14), (cx - 60, cy + 14), (cx - 10, cy - 17), (cx + 40, cy + 58), (cx + 80, cy + 14), (w - 30, cy + 14)]
        draw.line(kink_pts_1, fill=(255, 82, 82), width=12)
        draw.line(kink_pts_2, fill=(255, 82, 82), width=12)
        draw.text((cx, cy + 85), "CRITICAL DERAILMENT RISK", fill=(255, 82, 82), anchor="mm")

    return img

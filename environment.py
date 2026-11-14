#!/usr/bin/env python3
"""
ENVIRONMENT & LIGHTING ENGINE (Modular Sets & Depth of Field)
Builds reusable sets (Garden, Nursery Room, Starlight Night) with soft lighting,
atmospheric depth-of-field, and gentle camera framing.
"""

import math
from PIL import Image, ImageDraw, ImageFilter

def create_sunny_garden_environment(width=720, height=1280) -> Image.Image:
    """
    Creates a lush outdoor garden set with soft background bokeh (Depth of Field).
    Far elements are slightly blurred to keep visual focus locked on the hero character.
    """
    # 1. Distant Background Layer (Sky + Far Mountains)
    bg = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)

    # Soft pastel sky gradient
    for y in range(height):
        r = int(129 + 80 * (y / height))
        g = int(212 + 35 * (y / height))
        b = int(250 + 5 * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Far distant hills (Soft lavender-blue)
    far_hill = [(0, height)]
    for x in range(0, width + 20, 20):
        y = 650 + 40 * math.sin(x * 0.005)
        far_hill.append((x, y))
    far_hill.append((width, height))
    draw.polygon(far_hill, fill=(179, 218, 240))

    # Apply soft depth-of-field blur to distant background
    bg = bg.filter(ImageFilter.GaussianBlur(radius=3.5))

    # 2. Midground Layer (Crisp Rolling Hills)
    mid_draw = ImageDraw.Draw(bg)
    mid_hill = [(0, height)]
    for x in range(0, width + 10, 15):
        y = 780 + 35 * math.sin(x * 0.008 + 1.2)
        mid_hill.append((x, y))
    mid_hill.append((width, height))
    mid_draw.polygon(mid_hill, fill=(160, 212, 104))  # Soft meadow lime

    # 3. Foreground Stage Hill (Sharp emerald green)
    fg_hill = [(0, height)]
    for x in range(0, width + 10, 15):
        y = 860 + 25 * math.sin(x * 0.010 + 2.8)
        fg_hill.append((x, y))
    fg_hill.append((width, height))
    mid_draw.polygon(fg_hill, fill=(140, 193, 82))

    return bg

def create_cozy_nursery_environment(width=720, height=1280) -> Image.Image:
    """
    Creates a warm, cozy nursery room with wallpaper patterns and warm lighting.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Warm cream wall (#FFF9E6)
    draw.rectangle([(0, 0), (width, 820)], fill=(255, 249, 230))

    # Soft pastel wallpaper polka-dots
    for wx in range(40, width, 80):
        for wy in range(40, 800, 80):
            draw.ellipse([wx - 6, wy - 6, wx + 6, wy + 6], fill=(255, 224, 178, 120))

    # Wooden Skirting board
    draw.rectangle([(0, 810), (width, 835)], fill=(215, 170, 125))

    # Soft carpet floor (#FFE0B2)
    draw.rectangle([(0, 835), (width, height)], fill=(255, 230, 204))

    # Cozy Window with sunlight beam
    win_x0, win_y0 = 60, 120
    win_x1, win_y1 = 280, 420
    draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y1], radius=20, fill=(225, 245, 254), outline=(255, 255, 255), width=8)
    # Window panes
    mid_x = (win_x0 + win_x1) // 2
    mid_y = (win_y0 + win_y1) // 2
    draw.line([(mid_x, win_y0), (mid_x, win_y1)], fill=(255, 255, 255), width=6)
    draw.line([(win_x0, mid_y), (win_x1, mid_y)], fill=(255, 255, 255), width=6)

    # Soft depth blur
    img = img.filter(ImageFilter.GaussianBlur(radius=2.0))
    return img

#!/usr/bin/env python3
"""
RICKS CLIPS STUDIO ENVIRONMENT & STORY PROPS ENGINE (@RicksClips3000 Style)
Builds clean, high-contrast, fully opaque broadcast studio sets with dedicated
story presentation screens so text and visuals are crisp, grounded, and contained.
"""

import math
from PIL import Image, ImageDraw, ImageFilter

def create_studio_workshop_environment(width=720, height=1280) -> Image.Image:
    """
    Creates an opaque, high-contrast modern documentary studio stage.
    Fully opaque RGBA (alpha=255) to eliminate white blob artifacts.
    """
    bg = Image.new("RGBA", (width, height), (26, 32, 44, 255))
    draw = ImageDraw.Draw(bg)

    # 1. Studio Wall Gradient (Deep Charcoal Slate)
    for y in range(880):
        ratio = y / 880.0
        r = int(22 + 14 * ratio)
        g = int(28 + 16 * ratio)
        b = int(38 + 18 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Subtle tech blueprint grid lines on the back wall
    for gx in range(40, width, 60):
        draw.line([(gx, 60), (gx, 860)], fill=(45, 60, 85, 90), width=1)
    for gy in range(80, 860, 60):
        draw.line([(20, gy), (width - 20, gy)], fill=(45, 60, 85, 90), width=1)

    # Presentation Display Board on the wall (Framed monitor)
    board_x0, board_y0 = 60, 180
    board_x1, board_y1 = width - 60, 520
    draw.rounded_rectangle([board_x0, board_y0, board_x1, board_y1], radius=20, fill=(18, 22, 30, 255), outline=(97, 175, 239, 255), width=4)
    # Subtle inner screen header
    draw.rounded_rectangle([board_x0 + 8, board_y0 + 8, board_x1 - 8, board_y0 + 42], radius=10, fill=(30, 38, 52, 255))
    draw.text(((board_x0 + board_x1) // 2, board_y0 + 25), "TECHNICAL INVESTIGATION ARCHIVE", fill=(120, 150, 190, 255), anchor="mm")

    # 2. Polished Studio Floor
    for y in range(880, height):
        ratio = (y - 880.0) / (height - 880.0)
        r = int(48 + 32 * ratio)
        g = int(42 + 28 * ratio)
        b = int(38 + 24 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Baseboard separator
    draw.rectangle([(0, 874), (width, 882)], fill=(15, 18, 24, 255))
    return bg

# ==========================================
# STORY PROPS & DIAGRAMS (AIRPLANE & RAILROAD)
# ==========================================
def create_airplane_window_prop(size=(520, 260), window_type="SQUARE_STRESS") -> Image.Image:
    """Visual prop showing airplane fuselage with square vs rounded windows."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2

    # Metal aircraft fuselage panel
    draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=16, fill=(235, 240, 245), outline=(150, 160, 175), width=5)
    # Rivet details
    for rx in range(35, w - 30, 45):
        draw.ellipse([rx - 2, 24, rx + 2, 28], fill=(130, 140, 155))
        draw.ellipse([rx - 2, h - 28, rx + 2, h - 24], fill=(130, 140, 155))

    if window_type == "SQUARE_STRESS":
        # Square Window with RED stress concentration arrows
        win_size = 90
        wx0, wy0 = cx - win_size // 2, cy - win_size // 2
        wx1, wy1 = cx + win_size // 2, cy + win_size // 2
        # Deep blue sky inside window
        draw.rectangle([wx0, wy0, wx1, wy1], fill=(41, 128, 185), outline=(30, 30, 30), width=6)

        # RED Stress Concentration Lines bursting from corners
        for px, py, dx, dy in [
            (wx0, wy0, -35, -35),
            (wx1, wy0, 35, -35),
            (wx0, wy1, -35, 35),
            (wx1, wy1, 35, 35)
        ]:
            draw.line([(px, py), (px + dx, py + dy)], fill=(229, 57, 53), width=6)
            draw.text((px + dx - 8, py + dy - 8), "⚠️", fill=(255, 214, 0))

        draw.text((cx, h - 38), "90° CORNERS = 300% STRESS CRACKS", fill=(229, 57, 53), anchor="mm")

    else:
        # Modern Curved Oval Window with Smooth Green Flow
        win_w, win_h = 75, 105
        wx0, wy0 = cx - win_w // 2, cy - win_h // 2
        wx1, wy1 = cx + win_w // 2, cy + win_h // 2
        draw.rounded_rectangle([wx0, wy0, wx1, wy1], radius=32, fill=(41, 128, 185), outline=(30, 30, 30), width=6)

        # Smooth green pressure flow curves
        draw.arc([wx0 - 25, wy0 - 15, wx1 + 25, wy1 + 15], start=45, end=135, fill=(76, 175, 80), width=5)
        draw.arc([wx0 - 25, wy0 - 15, wx1 + 25, wy1 + 15], start=225, end=315, fill=(76, 175, 80), width=5)

        draw.text((cx, h - 38), "CURVED CORNERS = EVEN PRESSURE", fill=(76, 175, 80), anchor="mm")

    return img

def create_airplane_in_flight_prop(size=(520, 260)) -> Image.Image:
    """Retro 1954 De Havilland Comet jetliner in flight."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2

    # Sky card background
    draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=16, fill=(30, 45, 65), outline=(97, 175, 239), width=3)
    # Clouds
    draw.ellipse([40, cy + 20, 180, cy + 70], fill=(255, 255, 255, 60))
    draw.ellipse([320, cy - 40, 480, cy + 10], fill=(255, 255, 255, 60))

    # Sleek retro airliner silhouette (Silver with blue stripe)
    fuse_x0, fuse_y0 = 60, cy - 25
    fuse_x1, fuse_y1 = w - 80, cy + 25
    # Main fuselage
    draw.rounded_rectangle([fuse_x0, fuse_y0, fuse_x1, fuse_y1], radius=22, fill=(240, 244, 248), outline=(40, 45, 55), width=4)
    # Cockpit nose
    draw.chord([fuse_x1 - 25, fuse_y0, fuse_x1 + 35, fuse_y1], start=270, end=90, fill=(240, 244, 248), outline=(40, 45, 55), width=4)
    # Cockpit windshield
    draw.polygon([(fuse_x1, fuse_y0 + 4), (fuse_x1 + 22, fuse_y0 + 12), (fuse_x1 + 10, fuse_y0 + 20), (fuse_x1 - 5, fuse_y0 + 12)], fill=(33, 150, 243))
    # Tail fin
    draw.polygon([(fuse_x0 + 15, fuse_y0), (fuse_x0 - 25, fuse_y0 - 55), (fuse_x0 + 10, fuse_y0 - 55), (fuse_x0 + 45, fuse_y0)], fill=(33, 150, 243), outline=(40, 45, 55), width=3)
    # Blue cheatline
    draw.rectangle([fuse_x0 + 20, cy - 5, fuse_x1 + 15, cy + 5], fill=(33, 150, 243))

    # Row of SQUARE windows (historic design flaw!)
    for wx in range(fuse_x0 + 70, fuse_x1 - 30, 42):
        draw.rectangle([wx, cy - 14, wx + 18, cy + 2], fill=(40, 40, 40), outline=(229, 57, 53), width=2)

    draw.text((cx, h - 35), "1954: DE HAVILLAND COMET JET", fill=(255, 214, 0), anchor="mm")
    return img

def create_railroad_diagram_prop(size=(520, 260), hot_sun_kink=False) -> Image.Image:
    """Visual diagram showing steel rails with expansion gap or buckled sun kink."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2

    draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=16, fill=(22, 28, 38), outline=(97, 175, 239), width=3)

    if not hot_sun_kink:
        draw.text((cx, 38), "EXPANSION GAP (1.5mm)", fill=(97, 175, 239), anchor="mm")
        for tx in range(50, w - 50, 55):
            draw.rectangle([tx, cy - 35, tx + 28, cy + 35], fill=(130, 105, 75), outline=(70, 50, 35), width=2)
        # Steel Rails
        draw.line([(40, cy - 14), (cx - 15, cy - 14)], fill=(200, 210, 220), width=10)
        draw.line([(cx + 15, cy - 14), (w - 40, cy - 14)], fill=(200, 210, 220), width=10)
        draw.line([(40, cy + 14), (cx - 15, cy + 14)], fill=(200, 210, 220), width=10)
        draw.line([(cx + 15, cy + 14), (w - 40, cy + 14)], fill=(200, 210, 220), width=10)
        draw.text((cx, h - 38), "Gap absorbs summer heat expansion", fill=(152, 195, 121), anchor="mm")
    else:
        draw.text((cx, 38), "HEAT BUCKLING ('SUN KINK')", fill=(229, 57, 53), anchor="mm")
        kink1 = [(40, cy - 14), (cx - 60, cy - 14), (cx - 10, cy - 45), (cx + 40, cy + 30), (cx + 80, cy - 14), (w - 40, cy - 14)]
        kink2 = [(40, cy + 14), (cx - 60, cy + 14), (cx - 10, cy - 17), (cx + 40, cy + 58), (cx + 80, cy + 14), (w - 40, cy + 14)]
        draw.line(kink1, fill=(255, 82, 82), width=12)
        draw.line(kink2, fill=(255, 82, 82), width=12)
        draw.text((cx, h - 38), "Tracks twist and cause derailments!", fill=(255, 82, 82), anchor="mm")

    return img

#!/usr/bin/env python3
"""
Cartoon Asset Generator (Lalafun / Cocomelon Style)
Procedurally creates adorable vector-like cartoon characters and environment sprites.
"""

import math
from PIL import Image, ImageDraw

def create_smiling_sun(size=400) -> Image.Image:
    """Generates a warm, smiling cartoon sun with 12 friendly rays."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r_core = int(size * 0.30)
    r_ray_tip = int(size * 0.46)
    r_ray_base = int(size * 0.32)

    # 1. Draw 12 cheerful triangular rays
    num_rays = 12
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        ang_left = angle - 0.12
        ang_right = angle + 0.12

        p_tip = (cx + r_ray_tip * math.cos(angle), cy + r_ray_tip * math.sin(angle))
        p_l = (cx + r_ray_base * math.cos(ang_left), cy + r_ray_base * math.sin(ang_left))
        p_r = (cx + r_ray_base * math.cos(ang_right), cy + r_ray_base * math.sin(ang_right))

        draw.polygon([p_l, p_tip, p_r], fill=(255, 179, 0), outline=(245, 124, 0))

    # 2. Main Sun Body (Golden Yellow)
    draw.ellipse([cx - r_core, cy - r_core, cx + r_core, cy + r_core], fill=(255, 214, 0), outline=(255, 160, 0), width=6)

    # 3. Rosy Blushing Cheeks
    cheek_r = 18
    draw.ellipse([cx - 55 - cheek_r, cy + 12 - cheek_r, cx - 55 + cheek_r, cy + 12 + cheek_r], fill=(255, 112, 112, 190))
    draw.ellipse([cx + 55 - cheek_r, cy + 12 - cheek_r, cx + 55 + cheek_r, cy + 12 + cheek_r], fill=(255, 112, 112, 190))

    # 4. Big Sparkly Eyes
    eye_r = 14
    for ex in [cx - 35, cx + 35]:
        draw.ellipse([ex - eye_r, cy - 10 - eye_r, ex + eye_r, cy - 10 + eye_r], fill=(33, 33, 33))
        # White sparkle glints
        draw.ellipse([ex - 6, cy - 18, ex + 4, cy - 8], fill=(255, 255, 255))
        draw.ellipse([ex + 2, cy - 7, ex + 7, cy - 2], fill=(255, 255, 255))

    # 5. Happy Smiling Mouth
    draw.arc([cx - 28, cy - 2, cx + 28, cy + 38], start=20, end=160, fill=(33, 33, 33), width=6)
    # Tongue
    draw.chord([cx - 16, cy + 16, cx + 16, cy + 34], start=0, end=180, fill=(255, 128, 171))

    return img

def create_fluffy_cloud(width=340, height=180) -> Image.Image:
    """Generates a soft, puffy cartoon cloud."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Multi-circle overlapping cloud puffs
    circles = [
        (80, 110, 55),
        (140, 85, 65),
        (205, 80, 70),
        (265, 110, 50),
        (175, 115, 60),
    ]

    # Cloud shadow layer
    for x, y, r in circles:
        draw.ellipse([x - r, y - r + 8, x + r, y + r + 8], fill=(225, 240, 255, 220))
    # Pure white puff layer
    for x, y, r in circles:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 245))

    return img

def create_cute_bear(size=520) -> Image.Image:
    """
    Generates 'Barnaby Bear', an adorable cartoon character with big sparkly eyes,
    pink rosy cheeks, cute ears, and joyful expression (Lalafun / Cocomelon aesthetic).
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, int(size * 0.52)

    fur_color = (255, 183, 77)       # Warm honey caramel
    fur_dark = (239, 108, 0)         # Caramel outline
    belly_color = (255, 243, 224)    # Creamy tummy
    pink_inner = (248, 187, 208)     # Soft pastel pink

    # 1. Round Ears
    ear_radius = 50
    ear_offsets = [(-110, -115), (110, -115)]
    for ox, oy in ear_offsets:
        ex, ey = cx + ox, cy + oy
        # Outer ear
        draw.ellipse([ex - ear_radius, ey - ear_radius, ex + ear_radius, ey + ear_radius], fill=fur_color, outline=fur_dark, width=6)
        # Inner ear
        draw.ellipse([ex - ear_radius + 15, ey - ear_radius + 15, ex + ear_radius - 15, ey + ear_radius - 15], fill=pink_inner)

    # 2. Chubby Body
    body_w, body_h = 130, 140
    draw.ellipse([cx - body_w, cy - 20, cx + body_w, cy + body_h + 80], fill=fur_color, outline=fur_dark, width=6)
    # Creamy Tummy
    draw.ellipse([cx - 85, cy + 25, cx + 85, cy + body_h + 45], fill=belly_color)

    # Cute Tummy Heart Emblem
    draw.ellipse([cx - 20, cy + 60, cx + 5, cy + 85], fill=(255, 128, 171))
    draw.ellipse([cx - 5, cy + 60, cx + 20, cy + 85], fill=(255, 128, 171))
    draw.polygon([(cx - 20, cy + 74), (cx + 20, cy + 74), (cx, cy + 98)], fill=(255, 128, 171))

    # 3. Chubby Paws
    # Left Paw (waving)
    draw.ellipse([cx - 155, cy + 30, cx - 90, cy + 95], fill=fur_color, outline=fur_dark, width=5)
    # Right Paw
    draw.ellipse([cx + 90, cy + 30, cx + 155, cy + 95], fill=fur_color, outline=fur_dark, width=5)

    # 4. Big Round Cute Head
    head_r = 145
    draw.ellipse([cx - head_r, cy - head_r - 20, cx + head_r, cy + head_r - 20], fill=fur_color, outline=fur_dark, width=7)

    # 5. Muzzle (Snout)
    snout_w, snout_h = 80, 55
    snout_y = cy + 5
    draw.ellipse([cx - snout_w, snout_y - snout_h, cx + snout_w, snout_y + snout_h], fill=belly_color, outline=fur_dark, width=4)

    # Little Heart/Oval Nose
    draw.ellipse([cx - 22, snout_y - 30, cx + 22, snout_y - 6], fill=(55, 40, 30))
    # Nose highlight
    draw.ellipse([cx - 10, snout_y - 27, cx + 2, snout_y - 19], fill=(255, 255, 255, 180))

    # Cute Smile & Tongue
    draw.arc([cx - 26, snout_y - 14, cx + 26, snout_y + 30], start=10, end=170, fill=(55, 40, 30), width=5)
    draw.chord([cx - 15, snout_y + 6, cx + 15, snout_y + 26], start=0, end=180, fill=(255, 128, 171))

    # 6. Big Sparkling Anime/Cartoon Eyes
    eye_r = 26
    for ex in [cx - 65, cx + 65]:
        ey = cy - 40
        # Dark pupil
        draw.ellipse([ex - eye_r, ey - eye_r, ex + eye_r, ey + eye_r], fill=(38, 25, 20))
        # Big white catchlight
        draw.ellipse([ex - 12, ey - 18, ex + 4, ey - 2], fill=(255, 255, 255))
        # Small secondary twinkle
        draw.ellipse([ex + 4, ey + 2, ex + 12, ey + 10], fill=(255, 255, 255))

    # 7. Big Rosy Blush Cheeks (Sweet Kawaii style)
    blush_rx, blush_ry = 32, 20
    draw.ellipse([cx - 105 - blush_rx, cy - 8 - blush_ry, cx - 105 + blush_rx, cy - 8 + blush_ry], fill=(255, 138, 128, 180))
    draw.ellipse([cx + 105 - blush_rx, cy - 8 - blush_ry, cx + 105 + blush_rx, cy - 8 + blush_ry], fill=(255, 138, 128, 180))

    return img

def create_musical_note(size=120, color=(255, 64, 129)) -> Image.Image:
    """Creates a bouncy musical note sprite."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Double eighth note or single eighth note
    # Left note head
    draw.ellipse([20, 75, 55, 105], fill=color)
    # Right note head
    draw.ellipse([70, 60, 105, 90], fill=color)
    # Stems
    draw.rectangle([48, 25, 55, 88], fill=color)
    draw.rectangle([98, 12, 105, 73], fill=color)
    # Top beam
    draw.polygon([(48, 25), (105, 12), (105, 28), (48, 41)], fill=color)
    return img

def create_sparkle_star(size=140, color=(255, 238, 88)) -> Image.Image:
    """Creates a twinkling 5-point star with a happy smile."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r_outer = size * 0.46
    r_inner = size * 0.22

    points = []
    for i in range(10):
        angle = (math.pi / 5) * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

    draw.polygon(points, fill=color, outline=(245, 124, 0), width=4)
    # Little eye dots
    draw.ellipse([cx - 15, cy - 8, cx - 7, cy], fill=(33, 33, 33))
    draw.ellipse([cx + 7, cy - 8, cx + 15, cy], fill=(33, 33, 33))
    # Star smile
    draw.arc([cx - 10, cy - 2, cx + 10, cy + 12], start=20, end=160, fill=(33, 33, 33), width=3)
    return img

def create_rainbow_banner(width=1080, height=200) -> Image.Image:
    """Creates a vibrant curved rainbow arc."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = width // 2, height + 350
    colors = [
        (255, 82, 82),   # Red
        (255, 171, 64),  # Orange
        (255, 238, 88),  # Yellow
        (105, 240, 174), # Green
        (68, 138, 255),  # Blue
        (179, 136, 255)  # Violet
    ]
    r = 480
    for col in colors:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=190, end=350, fill=col, width=16)
        r -= 16
    return img

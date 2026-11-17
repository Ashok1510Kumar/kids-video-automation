#!/usr/bin/env python3
"""
DRAW UTILITIES (CLEAN FLOATING SUBTITLES - NO BOXES)
Renders viral YouTube Shorts subtitles floating directly on screen:
- Thick black stroke outline (stroke_width=4, stroke_fill=(0, 0, 0)) for 100% legibility on any background
- Zero background boxes, zero container rectangles, zero ugly borders
- Dynamic word wrapping into clean, centered 1-2 line subtitle bursts
"""

from PIL import Image, ImageDraw, ImageFont

def get_text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list:
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        if get_text_width(draw, test_line, font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines

def draw_floating_subtitles(
    draw: ImageDraw.ImageDraw,
    text: str,
    center_pos: tuple,     # (cx, cy)
    font: ImageFont.ImageFont,
    max_width=580,
    fill_color=(255, 255, 255),
    stroke_color=(0, 0, 0),
    stroke_width=4,
    line_spacing=10
):
    """
    Renders pure floating subtitles with black outline directly onto the scene.
    No boxes, no rectangles, no dialogue bubbles.
    """
    cx, cy = center_pos
    lines = wrap_text(draw, text, font, max_width)
    if not lines:
        return

    # Sample height
    sample_bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = sample_bbox[3] - sample_bbox[1]
    total_h = len(lines) * line_h + (len(lines) - 1) * line_spacing
    start_y = cy - total_h // 2

    cur_y = start_y
    for line in lines:
        draw.text(
            (cx, cur_y + line_h // 2),
            line,
            font=font,
            fill=fill_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
            anchor="mm"
        )
        cur_y += line_h + line_spacing

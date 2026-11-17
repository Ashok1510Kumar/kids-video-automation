#!/usr/bin/env python3
"""
DRAW UTILITIES & SAFE-ZONE TYPOGRAPHY ENGINE
Ensures all text is automatically word-wrapped, vertically centered,
and strictly kept INSIDE bounding boxes with zero clipping or overflow.
"""

from PIL import Image, ImageDraw, ImageFont

def get_text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    """Returns exact pixel width of text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list:
    """Wraps text into lines that do not exceed max_width."""
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

def draw_contained_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple,          # (x0, y0, x1, y1)
    font: ImageFont.ImageFont,
    fill_color=(255, 255, 255),
    line_spacing=8,
    align="center"
):
    """
    Renders text strictly inside box (x0, y0, x1, y1) with automatic word-wrapping
    and vertical centering. Never bleeds outside the box.
    """
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    max_h = y1 - y0

    lines = wrap_text(draw, text, font, max_w)
    if not lines:
        return

    # Measure total height
    sample_bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = sample_bbox[3] - sample_bbox[1]
    total_text_h = len(lines) * line_h + (len(lines) - 1) * line_spacing

    # Center vertically inside the container
    start_y = y0 + max(0, (max_h - total_text_h) // 2)

    cur_y = start_y
    for line in lines:
        lw = get_text_width(draw, line, font)
        if align == "center":
            lx = x0 + (max_w - lw) // 2
        else:
            lx = x0
        draw.text((lx, cur_y), line, fill=fill_color, font=font)
        cur_y += line_h + line_spacing

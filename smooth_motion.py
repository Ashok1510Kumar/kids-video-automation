#!/usr/bin/env python3
"""
SMOOTH MOTION & EASING ENGINE
Provides cubic/sine easing curves, smooth alpha cross-fading, and camera interpolation
to eliminate stutter and create silky-smooth 30fps animation.
"""

import math
from PIL import Image

def ease_in_out_quad(t: float) -> float:
    """Standard smooth ease-in-out curve (0.0 to 1.0)."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2.0 * t * t
    return 1.0 - math.pow(-2.0 * t + 2.0, 2) / 2.0

def ease_out_back(t: float, overshoot=1.4) -> float:
    """Spring overshoot easing for snappy, organic pop-in animations."""
    t = max(0.0, min(1.0, t))
    c1 = overshoot
    c3 = c1 + 1.0
    return 1.0 + c3 * math.pow(t - 1.0, 3) + c1 * math.pow(t - 1.0, 2)

def smooth_crossfade(img_from: Image.Image, img_to: Image.Image, progress: float) -> Image.Image:
    """
    Smoothly dissolves between two images with alpha blending.
    progress: 0.0 (100% img_from) to 1.0 (100% img_to).
    """
    alpha = ease_in_out_quad(progress)
    return Image.blend(img_from, img_to, alpha)

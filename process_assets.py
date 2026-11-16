#!/usr/bin/env python3
"""
ASSET PROCESSOR
Extracts characters with clean alpha transparency and formats 9:16 background scenes.
"""

import os
from PIL import Image, ImageFilter
import numpy as np

def make_transparent_from_solid(img_path: str, output_path: str, bg_color=(255, 255, 255), tolerance=28):
    """
    Intelligently removes a solid/near-solid background and creates smooth anti-aliased transparency.
    """
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img, dtype=np.float32)

    # Compute Euclidean color distance from target background color
    target = np.array(bg_color, dtype=np.float32)
    dist = np.sqrt(np.sum((arr[:, :, :3] - target) ** 2, axis=2))

    # Soft alpha ramp between tolerance and tolerance * 2.5 for smooth anti-aliased edges
    t_min = float(tolerance)
    t_max = float(tolerance * 2.8)

    alpha = np.clip((dist - t_min) / (t_max - t_min), 0.0, 1.0) * 255.0
    arr[:, :, 3] = alpha.astype(np.uint8)

    result = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.save(output_path, "PNG")
    print(f"Processed transparent character sprite: {output_path} ({result.size})")

def format_background(bg_path: str, output_path: str, target_size=(720, 1280)):
    """
    Crops and scales a background image to exact 9:16 vertical video dimensions.
    """
    img = Image.open(bg_path).convert("RGB")
    tw, th = target_size
    iw, ih = img.size

    # Scale to cover target aspect ratio
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)

    # Center crop
    left = (nw - tw) // 2
    top = (nh - th) // 2
    cropped = resized.crop((left, top, left + tw, top + th))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cropped.save(output_path, "PNG")
    print(f"Formatted 9:16 background: {output_path} ({cropped.size})")

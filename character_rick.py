#!/usr/bin/env python3
"""
RICKS CLIPS CHARACTER ENGINE (@RicksClips3000 Style)
Faithfully renders the signature Rick's Clips character design:
- Smooth white bean-shaped head with uniform 5px black contour
- Distinctive CONJOINED circular white eyes with black pupil dots
- Floating expressive detached eyebrows
- Dynamic mouth shapes (speaking, teeth grimace, smile)
- Sweating panic teardrops
- Capsule torso with costume variants (Narrator, Train Engineer, Arrogant Boss)
- Minimalist black stick limbs with elbow/knee joints and contact shadows
"""

import math
from PIL import Image, ImageDraw

def render_ricks_clips_character(
    costume="NARRATOR",
    eye_expression="NEUTRAL",   # NEUTRAL, WIDE_SHOCK, SKEPTICAL, JOY_ARC, PANIC
    mouth_expression="SPEAKING", # SPEAKING, TEETH_GRIMACE, SMILE, OPEN_O
    sweat_drop=False,
    brow_angle=0.0,             # -15 (angry/stern) to +20 (worried/confused)
    arm_pose="POINT_RIGHT",     # IDLE, POINT_RIGHT, SHOCKED_HANDS, HOLD_PROP
    size=(540, 720)
) -> Image.Image:
    """Renders a complete Rick's Clips 2D character sprite."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, int(h * 0.44)

    # 1. Contact Shadow on ground
    shadow_w, shadow_h = 170, 24
    shadow_y = h - 35
    draw.ellipse([cx - shadow_w // 2, shadow_y - shadow_h // 2, cx + shadow_w // 2, shadow_y + shadow_h // 2], fill=(0, 0, 0, 75))

    # 2. Stick Legs (Minimalist solid black 6px strokes)
    hip_y = cy + 120
    foot_y = shadow_y - 2
    # Left leg
    draw.line([(cx - 30, hip_y), (cx - 35, foot_y - 30), (cx - 40, foot_y)], fill=(20, 20, 20), width=6)
    # Right leg
    draw.line([(cx + 30, hip_y), (cx + 35, foot_y - 30), (cx + 40, foot_y)], fill=(20, 20, 20), width=6)
    # Shoes (small black capsules)
    draw.ellipse([cx - 58, foot_y - 8, cx - 24, foot_y + 4], fill=(20, 20, 20))
    draw.ellipse([cx + 24, foot_y - 8, cx + 58, foot_y + 4], fill=(20, 20, 20))

    # 3. Torso (Capsule shape with Costume Fills)
    torso_w, torso_h = 100, 115
    torso_x0, torso_y0 = cx - torso_w // 2, cy + 10
    torso_x1, torso_y1 = cx + torso_w // 2, cy + 10 + torso_h

    if costume == "ENGINEER":
        # Teal work vest over white collared shirt + red bandana
        draw.rounded_rectangle([torso_x0, torso_y0, torso_x1, torso_y1], radius=24, fill=(250, 250, 250), outline=(20, 20, 20), width=5)
        # Teal vest
        draw.rectangle([torso_x0 + 10, torso_y0 + 15, torso_x0 + 40, torso_y1 - 5], fill=(0, 137, 123), outline=(20, 20, 20), width=4)
        draw.rectangle([torso_x1 - 40, torso_y0 + 15, torso_x1 - 10, torso_y1 - 5], fill=(0, 137, 123), outline=(20, 20, 20), width=4)
        # Red neckerchief
        draw.polygon([(cx - 25, torso_y0), (cx + 25, torso_y0), (cx, torso_y0 + 25)], fill=(229, 57, 53), outline=(20, 20, 20), width=3)
    elif costume == "BOSS":
        # Frock coat with double-breasted yellow waistcoat and bowtie
        draw.rounded_rectangle([torso_x0, torso_y0, torso_x1, torso_y1], radius=24, fill=(255, 214, 0), outline=(20, 20, 20), width=5)
        # Dark coat sides
        draw.rectangle([torso_x0, torso_y0, torso_x0 + 25, torso_y1], fill=(38, 50, 56), outline=(20, 20, 20), width=4)
        draw.rectangle([torso_x1 - 25, torso_y0, torso_x1, torso_y1], fill=(38, 50, 56), outline=(20, 20, 20), width=4)
        # Black bowtie
        draw.polygon([(cx - 15, torso_y0 + 8), (cx + 15, torso_y0 + 8), (cx, torso_y0 + 18)], fill=(20, 20, 20))
        # Gold watch chain arc
        draw.arc([cx - 20, torso_y0 + 55, cx + 20, torso_y0 + 85], start=0, end=180, fill=(245, 127, 23), width=4)
    else:
        # Default Protagonist (Rick's clean light-blue collared shirt)
        draw.rounded_rectangle([torso_x0, torso_y0, torso_x1, torso_y1], radius=24, fill=(129, 212, 250), outline=(20, 20, 20), width=5)
        # Collar V
        draw.line([(cx - 20, torso_y0), (cx, torso_y0 + 22), (cx + 20, torso_y0)], fill=(20, 20, 20), width=4)
        # Buttons
        draw.ellipse([cx - 3, torso_y0 + 40, cx + 3, torso_y0 + 46], fill=(20, 20, 20))
        draw.ellipse([cx - 3, torso_y0 + 65, cx + 3, torso_y0 + 71], fill=(20, 20, 20))
        draw.ellipse([cx - 3, torso_y0 + 90, cx + 3, torso_y0 + 96], fill=(20, 20, 20))

    # 4. Stick Arms & Poses
    shoulder_y = torso_y0 + 15
    if arm_pose == "POINT_RIGHT":
        # Left arm relaxed
        draw.line([(cx - torso_w // 2, shoulder_y), (cx - 75, shoulder_y + 40), (cx - 65, shoulder_y + 90)], fill=(20, 20, 20), width=6)
        # Right arm pointing forward
        draw.line([(cx + torso_w // 2, shoulder_y), (cx + 85, shoulder_y + 10), (cx + 140, shoulder_y + 5)], fill=(20, 20, 20), width=6)
        # Pointing hand
        draw.ellipse([cx + 135, shoulder_y - 2, cx + 150, shoulder_y + 12], fill=(255, 255, 255), outline=(20, 20, 20), width=3)
    elif arm_pose == "SHOCKED_HANDS":
        # Both hands clutching face/temples
        draw.line([(cx - torso_w // 2, shoulder_y), (cx - 95, shoulder_y - 20), (cx - 75, cy - 30)], fill=(20, 20, 20), width=6)
        draw.line([(cx + torso_w // 2, shoulder_y), (cx + 95, shoulder_y - 20), (cx + 75, cy - 30)], fill=(20, 20, 20), width=6)
    else:
        # Neutral conversational gesturing
        draw.line([(cx - torso_w // 2, shoulder_y), (cx - 75, shoulder_y + 45), (cx - 50, shoulder_y + 75)], fill=(20, 20, 20), width=6)
        draw.line([(cx + torso_w // 2, shoulder_y), (cx + 75, shoulder_y + 45), (cx + 85, shoulder_y + 25)], fill=(20, 20, 20), width=6)

    # 5. Oversized White Bean Head (Pure white fill + 5px uniform black contour)
    head_w, head_h = 165, 145
    hx0, hy0 = cx - head_w // 2, cy - head_h // 2 - 25
    hx1, hy1 = cx + head_w // 2, cy + head_h // 2 - 25
    draw.ellipse([hx0, hy0, hx1, hy1], fill=(255, 255, 255), outline=(20, 20, 20), width=5)

    # Hair / Hats by Archetype
    if costume == "ENGINEER":
        # Pinstripe train engineer cap
        cap_y0 = hy0 - 15
        draw.arc([hx0 - 10, cap_y0, hx1 + 10, cap_y0 + 70], start=180, end=360, fill=(70, 90, 120), width=6)
        draw.chord([hx0 - 10, cap_y0, hx1 + 10, cap_y0 + 70], start=180, end=360, fill=(90, 115, 150))
        # Cap visor brim
        draw.arc([hx0 - 25, cap_y0 + 40, hx1 + 25, cap_y0 + 75], start=170, end=370, fill=(20, 20, 20), width=8)
    elif costume == "BOSS":
        # Black Bowler / Derby Hat
        hat_y = hy0 - 20
        # Hat brim
        draw.ellipse([hx0 - 30, hat_y + 35, hx1 + 30, hat_y + 60], fill=(30, 30, 30), outline=(10, 10, 10), width=4)
        # Hat dome
        draw.chord([hx0 + 5, hat_y - 25, hx1 - 5, hat_y + 45], start=180, end=360, fill=(40, 40, 40), outline=(10, 10, 10), width=4)
        # Grey side hair puffs
        draw.ellipse([hx0 - 15, cy - 40, hx0 + 15, cy - 10], fill=(210, 215, 220), outline=(20, 20, 20), width=3)
        draw.ellipse([hx1 - 15, cy - 40, hx1 + 15, cy - 10], fill=(210, 215, 220), outline=(20, 20, 20), width=3)
    else:
        # Rick's classic dark side-parted hair
        hair_pts = [(hx0 + 15, hy0 + 35), (hx0 + 30, hy0 + 10), (cx, hy0 + 5), (hx1 - 25, hy0 + 18), (hx1 - 10, hy0 + 45)]
        draw.polygon(hair_pts, fill=(35, 25, 20))

    # 6. SIGNATURE CONJOINED EYES
    eye_cy = cy - 35
    eye_r = 22
    left_ecx = cx - 18
    right_ecx = cx + 18

    # Outer black contour encompassing both eyes
    draw.ellipse([left_ecx - eye_r - 4, eye_cy - eye_r - 4, left_ecx + eye_r + 4, eye_cy + eye_r + 4], fill=(20, 20, 20))
    draw.ellipse([right_ecx - eye_r - 4, eye_cy - eye_r - 4, right_ecx + eye_r + 4, eye_cy + eye_r + 4], fill=(20, 20, 20))
    # Inner white eye fill (fused in center)
    draw.ellipse([left_ecx - eye_r, eye_cy - eye_r, left_ecx + eye_r, eye_cy + eye_r], fill=(255, 255, 255))
    draw.ellipse([right_ecx - eye_r, eye_cy - eye_r, right_ecx + eye_r, eye_cy + eye_r], fill=(255, 255, 255))
    draw.rectangle([left_ecx, eye_cy - eye_r + 4, right_ecx, eye_cy + eye_r - 4], fill=(255, 255, 255))

    # Pupils / Expression morphing
    if eye_expression == "WIDE_SHOCK":
        # Tiny pinprick shocked pupils
        draw.ellipse([left_ecx - 3, eye_cy - 3, left_ecx + 3, eye_cy + 3], fill=(20, 20, 20))
        draw.ellipse([right_ecx - 3, eye_cy - 3, right_ecx + 3, eye_cy + 3], fill=(20, 20, 20))
    elif eye_expression == "SKEPTICAL":
        # Horizontal half-lidded eyelids
        draw.chord([left_ecx - eye_r, eye_cy - eye_r, left_ecx + eye_r, eye_cy], start=180, end=360, fill=(255, 255, 255), outline=(20, 20, 20), width=4)
        draw.chord([right_ecx - eye_r, eye_cy - eye_r, right_ecx + eye_r, eye_cy], start=180, end=360, fill=(255, 255, 255), outline=(20, 20, 20), width=4)
        draw.ellipse([left_ecx - 4, eye_cy - 1, left_ecx + 4, eye_cy + 7], fill=(20, 20, 20))
        draw.ellipse([right_ecx - 4, eye_cy - 1, right_ecx + 4, eye_cy + 7], fill=(20, 20, 20))
    elif eye_expression == "JOY_ARC":
        # Curved happy eyes (^ ^)
        draw.arc([left_ecx - 14, eye_cy - 10, left_ecx + 14, eye_cy + 12], start=200, end=340, fill=(20, 20, 20), width=5)
        draw.arc([right_ecx - 14, eye_cy - 10, right_ecx + 14, eye_cy + 12], start=200, end=340, fill=(20, 20, 20), width=5)
    else:
        # Standard Rick's Clips pupils looking towards camera
        pupil_r = 7
        draw.ellipse([left_ecx - pupil_r + 2, eye_cy - pupil_r, left_ecx + pupil_r + 2, eye_cy + pupil_r], fill=(20, 20, 20))
        draw.ellipse([right_ecx - pupil_r + 2, eye_cy - pupil_r, right_ecx + pupil_r + 2, eye_cy + pupil_r], fill=(20, 20, 20))

    # 7. Floating Detached Eyebrows
    brow_y = eye_cy - eye_r - 12
    # Left brow
    draw.line([(left_ecx - 18, brow_y + int(brow_angle)), (left_ecx + 12, brow_y - int(brow_angle * 0.4))], fill=(20, 20, 20), width=5)
    # Right brow
    draw.line([(right_ecx - 12, brow_y - int(brow_angle * 0.4)), (right_ecx + 18, brow_y + int(brow_angle))], fill=(20, 20, 20), width=5)

    # 8. Mouth & Expressive Shapes
    mouth_y = cy + 12
    if mouth_expression == "TEETH_GRIMACE":
        # Stressed clenched white teeth grid
        mw, mh = 48, 22
        draw.rounded_rectangle([cx - mw // 2, mouth_y - mh // 2, cx + mw // 2, mouth_y + mh // 2], radius=6, fill=(255, 255, 255), outline=(20, 20, 20), width=4)
        draw.line([(cx - mw // 2, mouth_y), (cx + mw // 2, mouth_y)], fill=(20, 20, 20), width=3)
        for gx in range(cx - 14, cx + 20, 10):
            draw.line([(gx, mouth_y - mh // 2), (gx, mouth_y + mh // 2)], fill=(20, 20, 20), width=2)
    elif mouth_expression == "OPEN_O":
        # Shocked open oval mouth
        draw.ellipse([cx - 16, mouth_y - 12, cx + 16, mouth_y + 18], fill=(30, 20, 25), outline=(20, 20, 20), width=4)
        draw.ellipse([cx - 8, mouth_y + 2, cx + 8, mouth_y + 14], fill=(255, 128, 171))
    elif mouth_expression == "SMILE":
        # Confident curved smile
        draw.arc([cx - 22, mouth_y - 15, cx + 22, mouth_y + 18], start=20, end=160, fill=(20, 20, 20), width=5)
    else:
        # Active talking bean mouth
        draw.chord([cx - 20, mouth_y - 8, cx + 20, mouth_y + 16], start=0, end=180, fill=(35, 20, 25), outline=(20, 20, 20), width=4)
        draw.chord([cx - 12, mouth_y + 2, cx + 12, mouth_y + 14], start=0, end=180, fill=(255, 128, 171))

    # 9. Panic / Stress Sweat Teardrops (Signature anime sweat)
    if sweat_drop:
        sx = cx + head_w // 2 - 12
        sy = cy - 45
        draw.polygon([(sx, sy - 18), (sx - 9, sy + 6), (sx + 9, sy + 6)], fill=(79, 195, 247), outline=(2, 136, 209), width=2)
        draw.ellipse([sx - 9, sy - 2, sx + 9, sy + 14], fill=(79, 195, 247), outline=(2, 136, 209), width=2)

    return img

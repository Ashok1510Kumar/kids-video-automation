#!/usr/bin/env python3
"""
ANIMATION CONTROLLER & RIGGING ENGINE
Implements squash & stretch, periodic eye blinks, secondary head tilts,
rhythmic beat bouncing, and phoneme lip-sync driven by audio timing.
"""

import math
from PIL import Image, ImageDraw
from character_bible import CHARACTERS, EXPRESSIONS

class CharacterRig:
    def __init__(self, character_key="LEO_THE_BEAR", base_size=460):
        self.char_data = CHARACTERS[character_key]
        self.size = base_size
        self.colors = self.char_data["colors"]

    def render_pose(self, expression_key="REST", mouth_phoneme="REST", arm_wave=0.0) -> Image.Image:
        """
        Renders the character with specific facial expression, phoneme mouth shape, and arm pose.
        """
        img = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = self.size // 2, int(self.size * 0.52)
        c = self.colors

        # 1. Round Ears
        ear_r = 46
        for ox in [-100, 100]:
            ex, ey = cx + ox, cy - 105
            draw.ellipse([ex - ear_r, ey - ear_r, ex + ear_r, ey + ear_r], fill=c["fur_base"], outline=c["fur_shadow"], width=5)
            draw.ellipse([ex - ear_r + 14, ey - ear_r + 14, ex + ear_r - 14, ey + ear_r - 14], fill=c["inner_ear"])

        # 2. Chubby Body
        bw, bh = 115, 130
        draw.ellipse([cx - bw, cy - 10, cx + bw, cy + bh + 70], fill=c["fur_base"], outline=c["fur_shadow"], width=5)
        # Dungarees / Outfit
        draw.rounded_rectangle([cx - bw + 8, cy + 25, cx + bw - 8, cy + bh + 65], radius=25, fill=c["outfit_primary"])
        # Outfit Straps & Buttons
        draw.rectangle([cx - 75, cy + 10, cx - 45, cy + 65], fill=c["outfit_primary"])
        draw.rectangle([cx + 45, cy + 10, cx + 75, cy + 65], fill=c["outfit_primary"])
        draw.ellipse([cx - 68, cy + 50, cx - 52, cy + 66], fill=c["outfit_accent"])
        draw.ellipse([cx + 52, cy + 50, cx + 68, cy + 66], fill=c["outfit_accent"])

        # 3. Paws (with dynamic arm waving angle)
        # Left paw waving
        paw_angle = math.sin(arm_wave) * 18.0
        draw.ellipse([cx - 145, cy + 25 - int(paw_angle), cx - 85, cy + 85 - int(paw_angle)], fill=c["fur_base"], outline=c["fur_shadow"], width=5)
        # Right paw
        draw.ellipse([cx + 85, cy + 25 + int(paw_angle), cx + 145, cy + 85 + int(paw_angle)], fill=c["fur_base"], outline=c["fur_shadow"], width=5)

        # 4. Cute Big Head
        hr = 135
        draw.ellipse([cx - hr, cy - hr - 15, cx + hr, cy + hr - 15], fill=c["fur_base"], outline=c["fur_shadow"], width=6)

        # 5. Snout
        sw, sh = 72, 50
        sy = cy + 12
        draw.ellipse([cx - sw, sy - sh, cx + sw, sy + sh], fill=c["snout_belly"], outline=c["fur_shadow"], width=4)
        # Heart/Oval Nose
        draw.ellipse([cx - 18, sy - 26, cx + 18, sy - 6], fill=c["nose"])
        draw.ellipse([cx - 8, sy - 23, cx + 2, sy - 17], fill=(255, 255, 255, 200))

        # 6. Blushing Cheeks
        draw.ellipse([cx - 100 - 24, cy - 8 - 14, cx - 100 + 24, cy - 8 + 14], fill=c["blush"])
        draw.ellipse([cx + 100 - 24, cy - 8 - 14, cx + 100 + 24, cy - 8 + 14], fill=c["blush"])

        # 7. Eyes (Blinking vs Open Sparkly)
        is_blinking = (expression_key == "BLINK")
        eye_y = cy - 35
        eye_r = 24
        for ex in [cx - 58, cx + 58]:
            if is_blinking:
                # Closed happy sleeping/blinking arc
                draw.arc([ex - eye_r, eye_y - 8, ex + eye_r, eye_y + 14], start=10, end=170, fill=c["eyes"], width=5)
            else:
                # Big anime sparkling pupil
                draw.ellipse([ex - eye_r, eye_y - eye_r, ex + eye_r, eye_y + eye_r], fill=c["eyes"])
                # Primary white highlight
                draw.ellipse([ex - 10, eye_y - 16, ex + 4, eye_y - 2], fill=(255, 255, 255))
                # Secondary sparkle
                draw.ellipse([ex + 4, eye_y + 2, ex + 10, eye_y + 8], fill=(255, 255, 255))

        # 8. Dynamic Lip Sync Mouth Shape
        # Phonemes: REST, A_PHONEME, O_PHONEME, E_PHONEME
        if mouth_phoneme == "O_PHONEME":
            # Round O singing mouth
            draw.ellipse([cx - 15, sy - 2, cx + 15, sy + 30], fill=(50, 20, 20), outline=c["nose"], width=3)
            draw.ellipse([cx - 9, sy + 10, cx + 9, sy + 25], fill=(255, 128, 171))
        elif mouth_phoneme == "A_PHONEME":
            # Wide open singing mouth
            draw.chord([cx - 26, sy - 4, cx + 26, sy + 36], start=0, end=180, fill=(50, 20, 20), outline=c["nose"], width=3)
            draw.chord([cx - 18, sy + 12, cx + 18, sy + 34], start=0, end=180, fill=(255, 128, 171))
        elif mouth_phoneme == "E_PHONEME":
            # Wide smile with teeth
            draw.rounded_rectangle([cx - 28, sy - 2, cx + 28, sy + 20], radius=8, fill=(50, 20, 20), outline=c["nose"], width=3)
            draw.rounded_rectangle([cx - 24, sy, cx + 24, sy + 8], radius=4, fill=(255, 255, 255))
        else:
            # REST friendly smile arc
            draw.arc([cx - 24, sy - 10, cx + 24, sy + 22], start=15, end=165, fill=c["eyes"], width=5)

        return img

class StudioAnimator:
    """Calculates frame-by-frame transforms for beat-synced motion, blinks, and lip-sync."""
    def __init__(self, character_key="LEO_THE_BEAR", bpm=112):
        self.rig = CharacterRig(character_key)
        self.bpm = bpm
        self.beat_interval = 60.0 / bpm

        # Pre-cache main expression poses for ultra-fast rendering
        print("Caching character expression rigs...")
        self.cache = {}
        for expr in ["REST", "BLINK"]:
            for phoneme in ["REST", "A_PHONEME", "O_PHONEME", "E_PHONEME"]:
                self.cache[(expr, phoneme)] = self.rig.render_pose(expr, phoneme)

    def get_frame_pose(self, t: float, is_singing: bool) -> tuple:
        """
        Returns (transformed_image, draw_x_offset, draw_y_offset).
        Applies squash & stretch, periodic blinking, and secondary head tilts.
        """
        # 1. Natural Blinking Cycle (Every 3.2 seconds, lasts 0.16 seconds)
        blink_cycle = t % 3.2
        is_blinking = (blink_cycle < 0.16)
        expression = "BLINK" if is_blinking else "REST"

        # 2. Dynamic Lip-Sync driven by speech rhythm
        if is_singing:
            # Phoneme changes rhythmically on eighth-notes (~4 changes per second)
            phoneme_idx = int(t * 4.2) % 3
            phonemes = ["A_PHONEME", "O_PHONEME", "E_PHONEME"]
            active_phoneme = phonemes[phoneme_idx]
        else:
            active_phoneme = "REST"

        # Fetch base sprite
        base_sprite = self.cache.get((expression, active_phoneme), self.cache[("REST", "REST")])

        # 3. Beat-Synced Squash & Stretch Physics
        # Beat phase: 0.0 to 1.0 within current musical beat
        beat_phase = (t / self.beat_interval) % 1.0

        # Vertical hop: parabolic jump during beat
        hop_y = -abs(28.0 * math.sin(beat_phase * math.pi))

        # Elastic squash when landing (beat_phase near 0 or 1)
        if beat_phase < 0.15 or beat_phase > 0.85:
            scale_x = 1.08
            scale_y = 0.92
        else:
            # Stretch during upward motion
            scale_x = 0.95
            scale_y = 1.05

        # 4. Secondary Motion: Head & Body Tilt
        tilt_angle = 5.0 * math.sin(t * (self.bpm / 60.0) * math.pi)

        # Apply scaling & rotation
        w = max(10, int(base_sprite.width * scale_x))
        h = max(10, int(base_sprite.height * scale_y))
        transformed = base_sprite.resize((w, h), Image.BILINEAR)
        transformed = transformed.rotate(tilt_angle, resample=Image.BICUBIC)

        return transformed, hop_y

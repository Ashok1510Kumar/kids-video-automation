#!/usr/bin/env python3
"""
Lalafun / Cocomelon Style Kids Nursery Rhyme Video Generator & YouTube Uploader
Generates vibrant cartoon animations with character bobbing, spinning sun,
drifting clouds, floating musical notes, music box melody, and karaoke lyrics.
"""

import os
import sys
import math
import random
import asyncio
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Audio & Video processing
import edge_tts
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoClip
)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Custom modules
from music_generator import generate_nursery_music
from cartoon_assets import (
    create_smiling_sun,
    create_fluffy_cloud,
    create_cute_bear,
    create_musical_note,
    create_sparkle_star,
    create_rainbow_banner
)

# ==========================================
# 1. NURSERY RHYMES CATALOG (LALAFUN STYLE)
# ==========================================
RHYMES = [
    {
        "id": "twinkle",
        "title": "🌟 Twinkle Twinkle Little Star",
        "melody": "twinkle",
        "stanzas": [
            "Twinkle, twinkle, little star!",
            "How I wonder what you are!",
            "Up above the world so high,",
            "Like a diamond in the sky!",
            "Twinkle, twinkle, little star!",
            "How I wonder what you are! ⭐"
        ],
        "speech_text": (
            "Twinkle, twinkle, little star! "
            "How I wonder what you are! "
            "Up above the world so high, "
            "like a diamond in the sky! "
            "Twinkle, twinkle, little star, "
            "how I wonder what you are!"
        )
    },
    {
        "id": "wheels_on_bus",
        "title": "🚌 The Wheels on the Bus Go Round and Round",
        "melody": "wheels_on_bus",
        "stanzas": [
            "The wheels on the bus go round and round,",
            "Round and round, round and round!",
            "The wheels on the bus go round and round,",
            "All through the town!",
            "The horn on the bus goes beep, beep, beep!",
            "All through the town! 🚌"
        ],
        "speech_text": (
            "The wheels on the bus go round and round, "
            "round and round, round and round! "
            "The wheels on the bus go round and round, "
            "all through the town! "
            "The horn on the bus goes beep, beep, beep, "
            "all through the town!"
        )
    },
    {
        "id": "happy_and_you_know_it",
        "title": "👏 If You're Happy and You Know It!",
        "melody": "happy_and_you_know_it",
        "stanzas": [
            "If you're happy and you know it, clap your hands!",
            "If you're happy and you know it, clap your hands!",
            "If you're happy and you know it,",
            "And you really want to show it,",
            "If you're happy and you know it, clap your hands! 👏"
        ],
        "speech_text": (
            "If you're happy and you know it, clap your hands! "
            "If you're happy and you know it, clap your hands! "
            "If you're happy and you know it, and you really want to show it, "
            "if you're happy and you know it, clap your hands!"
        )
    },
    {
        "id": "old_macdonald",
        "title": "🐮 Old MacDonald Had a Farm",
        "melody": "old_macdonald",
        "stanzas": [
            "Old MacDonald had a farm, E-I-E-I-O!",
            "And on that farm he had a cow, E-I-E-I-O!",
            "With a moo moo here and a moo moo there,",
            "Here a moo, there a moo, everywhere a moo moo!",
            "Old MacDonald had a farm, E-I-E-I-O! 🐮"
        ],
        "speech_text": (
            "Old MacDonald had a farm, E-I-E-I-O! "
            "And on that farm he had a cow, E-I-E-I-O! "
            "With a moo moo here, and a moo moo there! "
            "Here a moo, there a moo, everywhere a moo moo! "
            "Old MacDonald had a farm, E-I-E-I-O!"
        )
    }
]

# High quality child-friendly voice
VOICE_NAME = "en-US-AnaNeural"

# ==========================================
# 2. AUDIO GENERATION (VOICE + MUSIC BOX)
# ==========================================
async def generate_speech(text: str, output_path: str):
    """Generates cheerful singing/spoken child narration."""
    print(f"Generating voiceover with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(text, VOICE_NAME, rate="+6%", pitch="+3Hz")
    await communicate.save(output_path)

def create_full_audio(rhyme: dict, voice_path: str, music_path: str, final_audio_path: str) -> float:
    """Mixes voiceover with pleasant synthesized music box melody."""
    voice_clip = AudioFileClip(voice_path)
    total_duration = voice_clip.duration + 1.2

    # Generate music box background matching duration
    generate_nursery_music(rhyme["melody"], total_duration, music_path, bpm=112)
    music_clip = AudioFileClip(music_path).volumex(0.28)  # Gentle background level

    # Voice is prioritized and loud
    voice_clip = voice_clip.volumex(1.0).set_start(0.4)

    composite_audio = CompositeAudioClip([music_clip, voice_clip]).set_duration(total_duration)
    composite_audio.write_audiofile(final_audio_path, fps=44100, logger=None)
    print(f"Mixed soundtrack ready: {final_audio_path} ({total_duration:.1f}s)")
    return total_duration

# ==========================================
# 3. PROCEDURAL CARTOON VIDEO COMPOSITOR
# ==========================================
class CartoonSceneRenderer:
    def __init__(self, rhyme: dict, width=720, height=1280):
        self.rhyme = rhyme
        self.width = width
        self.height = height

        # Load fonts
        try:
            self.font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            self.font_lyrics = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            self.font_cta = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        except IOError:
            try:
                self.font_header = ImageFont.truetype("arialbd.ttf", 36)
                self.font_lyrics = ImageFont.truetype("arialbd.ttf", 34)
                self.font_cta = ImageFont.truetype("arialbd.ttf", 28)
            except IOError:
                self.font_header = self.font_lyrics = self.font_cta = ImageFont.load_default()

        # Pre-render sprites in memory
        print("Pre-rendering Lalafun-style cartoon sprites...")
        self.sun_sprite = create_smiling_sun(size=260)
        self.cloud_sprite = create_fluffy_cloud(width=280, height=150)
        self.bear_sprite = create_cute_bear(size=440)
        self.note_pink = create_musical_note(size=85, color=(255, 64, 129))
        self.note_blue = create_musical_note(size=80, color=(0, 229, 255))
        self.note_yellow = create_musical_note(size=75, color=(255, 214, 0))
        self.star_sprite = create_sparkle_star(size=90)
        self.rainbow_sprite = create_rainbow_banner(width=720, height=160)

        # Pre-compute sky background gradient
        self.base_sky = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        sky_draw = ImageDraw.Draw(self.base_sky)
        for y in range(height):
            # Gradient: Soft Sunny Sky Blue to Pastel Mint
            ratio = y / height
            r = int(100 * (1 - ratio) + 178 * ratio)
            g = int(210 * (1 - ratio) + 235 * ratio)
            b = int(255 * (1 - ratio) + 242 * ratio)
            sky_draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Floating particle initial seeds
        self.notes_data = [
            {"sprite": self.note_pink, "x": 120, "speed": 65, "phase": 0.0},
            {"sprite": self.note_blue, "x": 230, "speed": 80, "phase": 1.7},
            {"sprite": self.note_yellow, "x": 580, "speed": 70, "phase": 3.4},
            {"sprite": self.star_sprite, "x": 480, "speed": 55, "phase": 5.1},
        ]

    def render_frame(self, t: float) -> np.ndarray:
        """Renders one single frame at time t."""
        # 1. Start with sky gradient
        frame = self.base_sky.copy()
        draw = ImageDraw.Draw(frame)

        # 2. Rainbow Arc in background
        frame.alpha_composite(self.rainbow_sprite, (0, 160))

        # 3. Rotating Smiling Sun in top-right
        sun_angle = (t * 22.0) % 360.0  # gentle continuous rotation
        rotated_sun = self.sun_sprite.rotate(sun_angle, resample=Image.BICUBIC)
        frame.alpha_composite(rotated_sun, (self.width - 240, 40))

        # 4. Parallax Drifting Fluffy Clouds
        cloud1_x = int((t * 28.0) % (self.width + 320)) - 280
        cloud2_x = int((t * 18.0 + 380) % (self.width + 320)) - 280
        frame.alpha_composite(self.cloud_sprite, (cloud1_x, 100))
        frame.alpha_composite(self.cloud_sprite, (cloud2_x, 220))

        # 5. Layered Rolling Green Hills (Cartoon waves)
        # Background Hill (Mint green)
        hill1_pts = [(0, self.height)]
        for x in range(0, self.width + 10, 20):
            y = 790 + 35 * math.sin(x * 0.007 + 0.5)
            hill1_pts.append((x, y))
        hill1_pts.append((self.width, self.height))
        draw.polygon(hill1_pts, fill=(129, 199, 132))

        # Foreground Hill (Vibrant Lime Green)
        hill2_pts = [(0, self.height)]
        for x in range(0, self.width + 10, 20):
            y = 860 + 30 * math.sin(x * 0.009 + 2.2)
            hill2_pts.append((x, y))
        hill2_pts.append((self.width, self.height))
        draw.polygon(hill2_pts, fill=(139, 195, 74))

        # Colorful Daisy Flowers on the grass
        for fx, fy in [(70, 930), (160, 980), (560, 920), (650, 970), (280, 1010)]:
            sway = int(4 * math.sin(t * 3.0 + fx))
            draw.ellipse([fx - 8 + sway, fy - 8, fx + 8 + sway, fy + 8], fill=(255, 235, 59))
            draw.ellipse([fx - 4 + sway, fy - 4, fx + 4 + sway, fy + 4], fill=(255, 112, 67))

        # 6. Floating Musical Notes & Stars (Rising & Swaying)
        for p in self.notes_data:
            py = int(self.height - 350 - ((t * p["speed"] + p["phase"] * 100) % 650))
            px = int(p["x"] + 24 * math.sin(t * 2.5 + p["phase"]))
            frame.alpha_composite(p["sprite"], (px, py))

        # 7. Animated Barnaby Bear (Squash, Stretch, Hop & Tilt)
        beat_freq = 2.0  # 2 hops per second
        bounce_phase = (t * beat_freq * math.pi) % math.pi
        hop_y = -abs(32.0 * math.sin(bounce_phase))

        # Squash and stretch scaling
        scale_x = 1.0 + 0.05 * math.cos(bounce_phase * 2)
        scale_y = 1.0 - 0.05 * math.cos(bounce_phase * 2)
        tilt_angle = 5.0 * math.sin(t * beat_freq * math.pi)

        # Apply transform
        scaled_w = max(10, int(self.bear_sprite.width * scale_x))
        scaled_h = max(10, int(self.bear_sprite.height * scale_y))
        resized_bear = self.bear_sprite.resize((scaled_w, scaled_h), Image.BILINEAR)
        animated_bear = resized_bear.rotate(tilt_angle, resample=Image.BICUBIC)

        bear_draw_x = (self.width - animated_bear.width) // 2
        bear_draw_y = int(580 + hop_y)
        frame.alpha_composite(animated_bear, (bear_draw_x, bear_draw_y))

        # 8. Top Banner Badge ("⭐ LALAFUN NURSERY RHYMES ⭐")
        badge_w, badge_h = 620, 75
        bx0 = (self.width - badge_w) // 2
        by0 = 35
        # Soft shadow
        draw.rounded_rectangle([bx0 + 4, by0 + 6, bx0 + badge_w + 4, by0 + badge_h + 6], radius=25, fill=(0, 0, 0, 45))
        # Candy Yellow Badge
        draw.rounded_rectangle([bx0, by0, bx0 + badge_w, by0 + badge_h], radius=25, fill=(255, 238, 88), outline=(255, 160, 0), width=5)
        draw.text((self.width // 2, by0 + badge_h // 2), "⭐ LALAFUN NURSERY RHYMES ⭐", fill=(40, 40, 40), font=self.font_header, anchor="mm")

        # 9. Karaoke Animated Lyrics Card (Bottom)
        # Determine active stanza
        stanzas = self.rhyme["stanzas"]
        idx = min(len(stanzas) - 1, int(t / 4.8))
        current_line = stanzas[idx]

        card_w, card_h = 660, 180
        cx0 = (self.width - card_w) // 2
        cy0 = self.height - 230

        # Card shadow & white candy container
        draw.rounded_rectangle([cx0 + 4, cy0 + 6, cx0 + card_w + 4, cy0 + card_h + 6], radius=30, fill=(0, 0, 0, 50))
        draw.rounded_rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], radius=30, fill=(255, 255, 255), outline=(255, 64, 129), width=6)

        # Pulse effect on lyrics text
        pulse_scale = 1.0 + 0.03 * math.sin(t * 8.0)
        draw.text((self.width // 2, cy0 + 65), current_line, fill=(216, 27, 96), font=self.font_lyrics, anchor="mm")

        # Little subscribe prompt pill
        draw.rounded_rectangle([cx0 + 80, cy0 + 120, cx0 + card_w - 80, cy0 + 160], radius=15, fill=(255, 240, 245))
        draw.text((self.width // 2, cy0 + 140), "🔔 Sing along & Subscribe! 🔔", fill=(100, 100, 100), font=self.font_cta, anchor="mm")

        # Convert RGBA to RGB for video output
        rgb_frame = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_frame.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_frame)

def render_cartoon_video(rhyme: dict, audio_path: str, output_video_path: str, duration: float):
    """Composites the animated video clip with audio."""
    print("Beginning Lalafun cartoon video rendering...")
    renderer = CartoonSceneRenderer(rhyme, width=720, height=1280)

    # Frame generator function for MoviePy
    def make_frame(t):
        return renderer.render_frame(t)

    audio_clip = AudioFileClip(audio_path)
    video = VideoClip(make_frame, duration=duration).set_audio(audio_clip)

    video.write_videofile(
        output_video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",  # Super fast encoding on GitHub Actions runner
        logger=None
    )
    print(f"Lalafun cartoon video rendered successfully: {output_video_path}")

# ==========================================
# 4. YOUTUBE UPLOADER (COPPA COMPLIANT)
# ==========================================
def upload_to_youtube(video_path: str, rhyme: dict) -> str:
    """Uploads nursery rhyme video to YouTube marked as Made for Kids."""
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    privacy = os.environ.get("YT_PRIVACY", "public")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials in environment!")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    youtube = build("youtube", "v3", credentials=creds)

    title = f"{rhyme['title']} | Nursery Rhymes for Kids #Shorts"
    description = (
        f"Sing along to {rhyme['title']} with Lalafun Nursery Rhymes! 🎶✨\n\n"
        "Lyrics:\n"
        + "\n".join(rhyme["stanzas"])
        + "\n\n🔔 Subscribe to our channel for new daily fun nursery rhymes and kids songs!\n\n"
        "#Shorts #NurseryRhymes #KidsSongs #Lalafun #Cocomelon #ToddlerSongs #Children #KidsAnimation"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": [
                "nursery rhymes", "kids songs", "lalafun", "cocomelon",
                "toddler learning", "rhymes for children", "baby songs", "shorts"
            ],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True,  # COPPA Compliance
        }
    }

    print(f"Uploading '{title}' to YouTube...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"SUCCESS! Video live at: {video_url}")
    return video_id

# ==========================================
# 5. MAIN PIPELINE
# ==========================================
def main():
    print(f"=== Starting Lalafun Nursery Rhymes Automation ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")

    rhyme = random.choice(RHYMES)
    print(f"Selected Nursery Rhyme: {rhyme['title']}")

    raw_voice = "voice_temp.mp3"
    raw_music = "music_temp.wav"
    mixed_audio = "soundtrack.wav"
    output_video = "lalafun_kids_video.mp4"

    # 1. Voiceover
    asyncio.run(generate_speech(rhyme["speech_text"], raw_voice))

    # 2. Music Box + Mix
    duration = create_full_audio(rhyme, raw_voice, raw_music, mixed_audio)

    # 3. Video Composition
    render_cartoon_video(rhyme, mixed_audio, output_video, duration)

    # 4. Upload
    upload_to_youtube(output_video, rhyme)

    print("=== Automation Finished Successfully ===")

if __name__ == "__main__":
    main()

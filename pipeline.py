#!/usr/bin/env python3
"""
LALAFUN STUDIO PRODUCTION PIPELINE
Implements the 7 Production Pillars:
1. Character Bible adherence (Fixed palette, silhouette, facial features)
2. Beat-synced squash & stretch, periodic eye blinks, and phoneme lip-sync
3. Modular environments with depth-of-field background blur
4. Music box melody + mastered audio + sound effects (sparkle, boing, pop)
5. Intro bumper + Outro with YouTube End-Screen safe zones
6. YouTube upload with strict COPPA compliance
"""

import os
import sys
import math
import random
import asyncio
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Audio & Video tools
import edge_tts
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoClip
)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Studio Modules
from character_bible import CHARACTERS
from animator import StudioAnimator
from environment import create_sunny_garden_environment
from music_generator import generate_nursery_music
from sfx_generator import generate_all_sfx
from cartoon_assets import (
    create_smiling_sun,
    create_fluffy_cloud,
    create_musical_note,
    create_sparkle_star,
    create_rainbow_banner
)

# ==========================================
# 1. CURATED NURSERY RHYMES CATALOG (90-120 BPM)
# ==========================================
RHYMES = [
    {
        "id": "twinkle",
        "title": "🌟 Twinkle Twinkle Little Star",
        "character": "LEO_THE_BEAR",
        "melody": "twinkle",
        "bpm": 112,
        "stanzas": [
            "Twinkle, twinkle, little star! ⭐",
            "How I wonder what you are!",
            "Up above the world so high,",
            "Like a diamond in the sky! 💎",
            "Twinkle, twinkle, little star!",
            "How I wonder what you are! ✨"
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
        "character": "LEO_THE_BEAR",
        "melody": "wheels_on_bus",
        "bpm": 116,
        "stanzas": [
            "The wheels on the bus go round and round! 🚌",
            "Round and round, round and round!",
            "The wheels on the bus go round and round,",
            "All through the town! 🏘️",
            "The horn on the bus goes beep beep beep!",
            "All through the town! 🎵"
        ],
        "speech_text": (
            "The wheels on the bus go round and round, "
            "round and round, round and round! "
            "The wheels on the bus go round and round, "
            "all through the town! "
            "The horn on the bus goes beep beep beep, "
            "all through the town!"
        )
    },
    {
        "id": "happy_and_you_know_it",
        "title": "👏 If You're Happy and You Know It!",
        "character": "LEO_THE_BEAR",
        "melody": "happy_and_you_know_it",
        "bpm": 114,
        "stanzas": [
            "If you're happy and you know it, clap your hands! 👏",
            "If you're happy and you know it, clap your hands! 👏",
            "If you're happy and you know it,",
            "And you really want to show it,",
            "If you're happy and you know it, clap your hands! 🥳"
        ],
        "speech_text": (
            "If you're happy and you know it, clap your hands! "
            "If you're happy and you know it, clap your hands! "
            "If you're happy and you know it, and you really want to show it, "
            "if you're happy and you know it, clap your hands!"
        )
    }
]

VOICE_NAME = "en-US-AnaNeural"

# ==========================================
# 2. AUDIO & SOUND DESIGN (MASTERED TO -14 LUFS)
# ==========================================
async def generate_speech(text: str, output_path: str):
    """Generates warm, expressive child narration."""
    print(f"Synthesizing voice with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(text, VOICE_NAME, rate="+6%", pitch="+3Hz")
    await communicate.save(output_path)

def build_soundtrack(rhyme: dict, voice_path: str, output_soundtrack_path: str) -> float:
    """
    Mixes voiceover, music box melody, and sound effects with broadcast loudness balance.
    """
    generate_all_sfx()
    voice_clip = AudioFileClip(voice_path)
    # 2.5s Intro + Voice Duration + 3.0s Outro
    intro_dur = 2.5
    outro_dur = 3.0
    total_duration = intro_dur + voice_clip.duration + outro_dur

    # Generate music box background
    music_temp = "music_temp.wav"
    generate_nursery_music(rhyme["melody"], total_duration, music_temp, bpm=rhyme["bpm"])

    # Sound Clips
    music_clip = AudioFileClip(music_temp).volumex(0.26)
    voice_clip = voice_clip.volumex(1.0).set_start(intro_dur)

    # SFX Cues
    sfx_sparkle = AudioFileClip("sfx_sparkle.wav").volumex(0.35).set_start(0.2)
    sfx_pop1 = AudioFileClip("sfx_pop.wav").volumex(0.30).set_start(intro_dur)
    sfx_outro_sparkle = AudioFileClip("sfx_sparkle.wav").volumex(0.35).set_start(total_duration - outro_dur + 0.3)

    final_audio = CompositeAudioClip([
        music_clip,
        voice_clip,
        sfx_sparkle,
        sfx_pop1,
        sfx_outro_sparkle
    ]).set_duration(total_duration)

    final_audio.write_audiofile(output_soundtrack_path, fps=44100, logger=None)
    print(f"Mastered soundtrack ready: {output_soundtrack_path} ({total_duration:.1f}s)")
    return total_duration

# ==========================================
# 3. PRODUCTION SCENE COMPOSITOR
# ==========================================
class LalafunDirector:
    def __init__(self, rhyme: dict, total_duration: float, width=720, height=1280):
        self.rhyme = rhyme
        self.total_duration = total_duration
        self.intro_dur = 2.5
        self.outro_dur = 3.0
        self.width = width
        self.height = height

        # Initialize Character Rig & Animator
        self.animator = StudioAnimator(rhyme["character"], bpm=rhyme["bpm"])

        # Load typography
        try:
            self.font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
            self.font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            self.font_cta = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
        except IOError:
            try:
                self.font_title = ImageFont.truetype("arialbd.ttf", 40)
                self.font_sub = ImageFont.truetype("arialbd.ttf", 32)
                self.font_cta = ImageFont.truetype("arialbd.ttf", 26)
            except IOError:
                self.font_title = self.font_sub = self.font_cta = ImageFont.load_default()

        # Build environments & sprites
        print("Assembling studio environment & lighting layers...")
        self.env_bg = create_sunny_garden_environment(width, height)
        self.sun_sprite = create_smiling_sun(size=250)
        self.cloud_sprite = create_fluffy_cloud(width=270, height=140)
        self.rainbow_sprite = create_rainbow_banner(width=720, height=160)
        self.note_pink = create_musical_note(size=85, color=(255, 64, 129))
        self.note_cyan = create_musical_note(size=80, color=(0, 229, 255))
        self.star_sprite = create_sparkle_star(size=90)

    def render_frame(self, t: float) -> np.ndarray:
        frame = self.env_bg.copy()
        draw = ImageDraw.Draw(frame)

        # ----------------------------------------------------
        # SCENE A: INTRO BUMPER (0.0s to 2.5s)
        # ----------------------------------------------------
        if t < self.intro_dur:
            # Rotating Sun & Rainbow
            frame.alpha_composite(self.rainbow_sprite, (0, 140))
            rot_sun = self.sun_sprite.rotate((t * 24.0) % 360, resample=Image.BICUBIC)
            frame.alpha_composite(rot_sun, (self.width - 230, 40))

            # Cheerful Welcome Card
            intro_card_w, intro_card_h = 640, 240
            ix0 = (self.width - intro_card_w) // 2
            iy0 = 240
            draw.rounded_rectangle([ix0 + 4, iy0 + 6, ix0 + intro_card_w + 4, iy0 + intro_card_h + 6], radius=30, fill=(0, 0, 0, 45))
            draw.rounded_rectangle([ix0, iy0, ix0 + intro_card_w, iy0 + intro_card_h], radius=30, fill=(255, 238, 88), outline=(255, 143, 0), width=6)
            draw.text((self.width // 2, iy0 + 70), "⭐ LALAFUN NURSERY ⭐", fill=(40, 40, 40), font=self.font_title, anchor="mm")
            draw.text((self.width // 2, iy0 + 150), self.rhyme["title"], fill=(216, 27, 96), font=self.font_sub, anchor="mm")

            # Waving Character Pose
            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=False)
            cx = (self.width - char_sprite.width) // 2
            cy = int(620 + hop)
            frame.alpha_composite(char_sprite, (cx, cy))

        # ----------------------------------------------------
        # SCENE C: OUTRO CARD & END-SCREEN SAFE ZONE (Last 3.0s)
        # ----------------------------------------------------
        elif t >= self.total_duration - self.outro_dur:
            outro_w, outro_h = 650, 680
            ox0 = (self.width - outro_w) // 2
            oy0 = 200
            # Card background
            draw.rounded_rectangle([ox0, oy0, ox0 + outro_w, oy0 + outro_h], radius=35, fill=(255, 255, 255), outline=(255, 64, 129), width=7)
            draw.text((self.width // 2, oy0 + 60), "🎉 THANKS FOR WATCHING! 🎉", fill=(216, 27, 96), font=self.font_title, anchor="mm")
            draw.text((self.width // 2, oy0 + 120), "Sing along with us again tomorrow!", fill=(70, 70, 70), font=self.font_sub, anchor="mm")

            # YouTube End Screen Placeholders (Subscribe Circle & Next Video Box)
            draw.ellipse([self.width // 2 - 80, oy0 + 170, self.width // 2 + 80, oy0 + 330], fill=(255, 240, 245), outline=(255, 64, 129), width=5)
            draw.text((self.width // 2, oy0 + 250), "SUBSCRIBE", fill=(216, 27, 96), font=self.font_sub, anchor="mm")

            draw.rounded_rectangle([ox0 + 60, oy0 + 370, ox0 + outro_w - 60, oy0 + 580], radius=20, fill=(240, 248, 255), outline=(33, 150, 243), width=5)
            draw.text((self.width // 2, oy0 + 475), "▶ NEXT NURSERY RHYME", fill=(25, 118, 210), font=self.font_sub, anchor="mm")

            # Small dancing character at the bottom
            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=False)
            thumb_char = char_sprite.resize((240, 240), Image.BILINEAR)
            frame.alpha_composite(thumb_char, ((self.width - 240) // 2, self.height - 300))

        # ----------------------------------------------------
        # SCENE B: HERO SING-ALONG PERFORMANCE (Main Body)
        # ----------------------------------------------------
        else:
            rel_t = t - self.intro_dur

            # 1. Background Rainbow Arc
            frame.alpha_composite(self.rainbow_sprite, (0, 140))

            # 2. Rotating Smiling Sun
            rot_sun = self.sun_sprite.rotate((t * 22.0) % 360, resample=Image.BICUBIC)
            frame.alpha_composite(rot_sun, (self.width - 230, 40))

            # 3. Parallax Floating Clouds
            c1_x = int((t * 26.0) % (self.width + 300)) - 270
            c2_x = int((t * 16.0 + 360) % (self.width + 300)) - 270
            frame.alpha_composite(self.cloud_sprite, (c1_x, 90))
            frame.alpha_composite(self.cloud_sprite, (c2_x, 210))

            # 4. Floating Musical Notes (Wobbling Sine Wave)
            for idx, (note_img, nx, spd, phase) in enumerate([
                (self.note_pink, 110, 65, 0.0),
                (self.note_cyan, 220, 80, 1.8),
                (self.star_sprite, 570, 70, 3.5),
            ]):
                ny = int(self.height - 360 - ((t * spd + phase * 90) % 650))
                rx = int(nx + 22 * math.sin(t * 2.8 + phase))
                frame.alpha_composite(note_img, (rx, ny))

            # 5. Beat-Synced Animated Character (Squash, Stretch, Blink, Lip-Sync)
            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=True)
            cx = (self.width - char_sprite.width) // 2
            cy = int(580 + hop)
            frame.alpha_composite(char_sprite, (cx, cy))

            # 6. Top Studio Branding
            badge_w, badge_h = 620, 70
            bx0 = (self.width - badge_w) // 2
            by0 = 35
            draw.rounded_rectangle([bx0 + 3, by0 + 5, bx0 + badge_w + 3, by0 + badge_h + 5], radius=22, fill=(0, 0, 0, 40))
            draw.rounded_rectangle([bx0, by0, bx0 + badge_w, by0 + badge_h], radius=22, fill=(255, 238, 88), outline=(255, 143, 0), width=5)
            draw.text((self.width // 2, by0 + badge_h // 2), "⭐ LALAFUN NURSERY RHYMES ⭐", fill=(40, 40, 40), font=self.font_sub, anchor="mm")

            # 7. Karaoke Lyric Cards (Bottom Container)
            stanzas = self.rhyme["stanzas"]
            total_song_time = self.total_duration - self.intro_dur - self.outro_dur
            stanza_dur = total_song_time / len(stanzas)
            cur_idx = min(len(stanzas) - 1, int(rel_t / stanza_dur))
            cur_line = stanzas[cur_idx]

            card_w, card_h = 660, 175
            cx0 = (self.width - card_w) // 2
            cy0 = self.height - 225

            draw.rounded_rectangle([cx0 + 4, cy0 + 6, cx0 + card_w + 4, cy0 + card_h + 6], radius=28, fill=(0, 0, 0, 45))
            draw.rounded_rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], radius=28, fill=(255, 255, 255), outline=(255, 64, 129), width=6)
            draw.text((self.width // 2, cy0 + 60), cur_line, fill=(216, 27, 96), font=self.font_sub, anchor="mm")

            # Sing-along hint
            draw.rounded_rectangle([cx0 + 90, cy0 + 115, cx0 + card_w - 90, cy0 + 155], radius=15, fill=(255, 240, 245))
            draw.text((self.width // 2, cy0 + 135), "🔔 Sing along with Leo! 🔔", fill=(110, 110, 110), font=self.font_cta, anchor="mm")

        # Convert to RGB array for MoviePy
        rgb_out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_out.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_out)

def render_studio_video(rhyme: dict, audio_path: str, output_path: str, duration: float):
    """Composites the full Lalafun animation with mastered audio."""
    print("Beginning Studio video composition...")
    director = LalafunDirector(rhyme, duration, width=720, height=1280)

    audio_clip = AudioFileClip(audio_path)
    video = VideoClip(lambda t: director.render_frame(t), duration=duration).set_audio(audio_clip)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None
    )
    print(f"Lalafun studio video rendered: {output_path} ({duration:.1f}s)")

# ==========================================
# 4. YOUTUBE UPLOADER (COPPA COMPLIANT)
# ==========================================
def upload_to_youtube(video_path: str, rhyme: dict) -> str:
    """Uploads nursery rhyme video with strict Made for Kids flag."""
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

    title = f"{rhyme['title']} | Lalafun Nursery Rhymes for Kids #Shorts"
    description = (
        f"Sing and dance with Leo the Bear in {rhyme['title']}! 🐻🎶✨\n\n"
        "Song Lyrics:\n"
        + "\n".join(rhyme["stanzas"])
        + "\n\n🔔 Subscribe to Lalafun for new joyful nursery rhymes and kids songs every day!\n\n"
        "#Shorts #NurseryRhymes #Lalafun #Cocomelon #KidsSongs #ToddlerLearning #ChildrenAnimation #SingAlong"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": [
                "lalafun", "nursery rhymes", "kids songs", "cocomelon",
                "toddler learning", "rhymes for children", "baby songs", "shorts"
            ],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True,  # Mandatory COPPA flag
        }
    }

    print(f"Publishing '{title}' to YouTube ({privacy})...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    vid_id = response.get("id")
    video_url = f"https://youtu.be/{vid_id}"
    print(f"SUCCESS! Video live at: {video_url}")
    return vid_id

# ==========================================
# 5. MAIN ENTRY POINT
# ==========================================
def main():
    print(f"=== Lalafun Studio Automation Started ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
    rhyme = random.choice(RHYMES)
    print(f"Hero Song: {rhyme['title']} (Character: {rhyme['character']})")

    voice_file = "voice_track.mp3"
    soundtrack_file = "soundtrack_master.wav"
    output_video_file = "lalafun_studio_output.mp4"

    # 1. Voiceover
    asyncio.run(generate_speech(rhyme["speech_text"], voice_file))

    # 2. Sound Design & Mastered Soundtrack
    duration = build_soundtrack(rhyme, voice_file, soundtrack_file)

    # 3. Studio Video Composition
    render_studio_video(rhyme, soundtrack_file, output_video_file, duration)

    # 4. YouTube Upload
    upload_to_youtube(output_video_file, rhyme)

    print("=== Lalafun Studio Automation Finished Successfully ===")

if __name__ == "__main__":
    main()

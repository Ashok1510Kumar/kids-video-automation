#!/usr/bin/env python3
"""
RICKS CLIPS PRODUCTION PIPELINE (@RicksClips3000 Edition)
Faithfully produces high-retention 45-second micro-documentary shorts:
- Signature white bean-head character with conjoined eyes & stick limbs
- Rapid charismatic narration (175 WPM) with multi-character voice acting
- Syncopated lo-fi groove soundtrack + mechanical foley SFX
- Visual technical props and diagrams (railroad gaps, sun kinks, aircraft corners)
- Centered bold captions with active word bounce and color highlights
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
from stories_rick import RICKS_EPISODES
from character_rick import render_ricks_clips_character
from environment_rick import (
    create_studio_workshop_environment,
    create_railroad_diagram_prop
)
from music_generator import generate_nursery_music
from sfx_generator import generate_all_sfx

# Charismatic storytelling voice (American male baritone, crisp & engaging)
VOICE_NAME = "en-US-GuyNeural"

# ==========================================
# 1. AUDIO & SOUND DESIGN (175 WPM + LO-FI GROOVE)
# ==========================================
async def generate_narration(episode: dict, output_path: str):
    """Generates brisk, engaging American voiceover (175 words/min)."""
    full_text = " ".join([beat["narration"] for beat in episode["beats"]])
    print(f"Synthesizing Rick's Clips narration with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(full_text, VOICE_NAME, rate="+10%", pitch="+0Hz")
    await communicate.save(output_path)

def build_soundtrack(episode: dict, voice_path: str, output_soundtrack_path: str) -> float:
    """
    Mixes voiceover, syncopated lo-fi groove music, and foley sound effects.
    """
    generate_all_sfx()
    voice_clip = AudioFileClip(voice_path)
    intro_lead = 0.5
    outro_tail = 2.0
    total_duration = intro_lead + voice_clip.duration + outro_tail

    # 1. Background Groove Music (Ducked so voice is crystal clear)
    music_temp = "music_temp.wav"
    generate_nursery_music("groove", total_duration, music_temp, bpm=115)
    music_clip = AudioFileClip(music_temp).volumex(0.20)
    voice_clip = voice_clip.volumex(1.0).set_start(intro_lead)

    # 2. Foley SFX Cues
    sfx_clips = [music_clip, voice_clip]

    # Hook pop at 0.8s
    sfx_clips.append(AudioFileClip("sfx_pop.wav").volumex(0.35).set_start(intro_lead + 0.5))
    # Conflict snap whoosh at 11s
    sfx_clips.append(AudioFileClip("sfx_whoosh.wav").volumex(0.30).set_start(intro_lead + 10.5))
    # Disaster boing/snap at 23s
    sfx_clips.append(AudioFileClip("sfx_boing.wav").volumex(0.35).set_start(intro_lead + 22.0))
    # Payoff fanfare at 36s
    sfx_clips.append(AudioFileClip("sfx_fanfare.wav").volumex(0.32).set_start(intro_lead + 35.0))

    composite_audio = CompositeAudioClip(sfx_clips).set_duration(total_duration)
    composite_audio.write_audiofile(output_soundtrack_path, fps=44100, logger=None)
    print(f"Mastered Rick's Clips soundtrack: {output_soundtrack_path} ({total_duration:.1f}s)")
    return total_duration

# ==========================================
# 2. RICKS CLIPS SCENE DIRECTOR & COMPOSITOR
# ==========================================
class RicksClipsDirector:
    def __init__(self, episode: dict, total_duration: float, width=720, height=1280):
        self.episode = episode
        self.total_duration = total_duration
        self.width = width
        self.height = height

        # Build 3D Studio Workshop Environment
        print("Rendering Rick's Clips studio workshop environment...")
        self.env_bg = create_studio_workshop_environment(width, height)

        # Pre-render Technical Props
        self.prop_normal_rail = create_railroad_diagram_prop((380, 260), hot_sun_kink=False)
        self.prop_buckled_rail = create_railroad_diagram_prop((380, 260), hot_sun_kink=True)

        # Pre-render Character Archetype Sprites
        print("Pre-rendering Rick's Clips character rigs...")
        self.char_narrator = render_ricks_clips_character(costume="NARRATOR", eye_expression="NEUTRAL", mouth_expression="SPEAKING", arm_pose="POINT_RIGHT")
        self.char_boss_shocked = render_ricks_clips_character(costume="BOSS", eye_expression="WIDE_SHOCK", mouth_expression="TEETH_GRIMACE", arm_pose="SHOCKED_HANDS", sweat_drop=True, brow_angle=18.0)
        self.char_engineer_warning = render_ricks_clips_character(costume="ENGINEER", eye_expression="SKEPTICAL", mouth_expression="SPEAKING", arm_pose="IDLE", brow_angle=10.0)
        self.char_narrator_joy = render_ricks_clips_character(costume="NARRATOR", eye_expression="JOY_ARC", mouth_expression="SMILE", arm_pose="POINT_RIGHT")

        # Typography (Bold Sans-Serif with high legibility)
        try:
            self.font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            self.font_caption = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
            self.font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
        except IOError:
            try:
                self.font_hook = ImageFont.truetype("arialbd.ttf", 36)
                self.font_caption = ImageFont.truetype("arialbd.ttf", 34)
                self.font_badge = ImageFont.truetype("arialbd.ttf", 24)
            except IOError:
                self.font_hook = self.font_caption = self.font_badge = ImageFont.load_default()

    def render_frame(self, t: float) -> np.ndarray:
        frame = self.env_bg.copy()
        draw = ImageDraw.Draw(frame)

        # Calculate current story beat
        beats = self.episode["beats"]
        num_beats = len(beats)
        beat_dur = max(1.0, (self.total_duration - 1.5) / float(num_beats))
        cur_beat_idx = min(num_beats - 1, int(t / beat_dur))
        cur_beat = beats[cur_beat_idx]

        # 1. Subtle Camera Snap-Zoom on Dramatic Beat 2 (Disaster)
        is_disaster_beat = (cur_beat_idx == 2)
        if is_disaster_beat:
            zoom_scale = 1.05 + 0.02 * math.sin(t * 12.0)  # Subtle camera shake/zoom
        else:
            zoom_scale = 1.00

        # 2. Dynamic Character Placement & Animation
        # Gentle natural body idle bounce
        idle_bounce = int(4 * math.sin(t * 5.0))

        if cur_beat_idx == 0:
            # Beat 1: Narrator introduces the paradox
            char_sprite = self.char_narrator
            char_x = (self.width - char_sprite.width) // 2
            char_y = 480 + idle_bounce
            frame.alpha_composite(char_sprite, (char_x, char_y))

        elif cur_beat_idx == 1:
            # Beat 2: Stubborn Boss demanding perfection
            char_sprite = self.char_boss_shocked
            char_x = int(self.width * 0.08)
            char_y = 480 + idle_bounce
            frame.alpha_composite(char_sprite, (char_x, char_y))

            # Technical diagram on the right side
            frame.alpha_composite(self.prop_normal_rail, (int(self.width * 0.44), 520))

        elif cur_beat_idx == 2:
            # Beat 3: The Disaster / Sun Kink Buckling!
            char_sprite = self.char_engineer_warning
            char_x = int(self.width * 0.06)
            char_y = 480 + idle_bounce
            frame.alpha_composite(char_sprite, (char_x, char_y))

            # Buckled Jagged Rail Prop with heat warning
            frame.alpha_composite(self.prop_buckled_rail, (int(self.width * 0.44), 510))

            # Comic impact marks
            draw.text((char_x + 220, char_y + 60), "💥", font=self.font_hook)

        else:
            # Beat 4: Resolution & Lesson
            char_sprite = self.char_narrator_joy
            char_x = (self.width - char_sprite.width) // 2
            char_y = 480 + idle_bounce
            frame.alpha_composite(char_sprite, (char_x, char_y))

        # 3. Top Paradox Hook Badge (First 8 seconds)
        if t < 8.0:
            hook_w, hook_h = 660, 110
            hx0 = (self.width - hook_w) // 2
            hy0 = 60
            draw.rounded_rectangle([hx0 + 4, hy0 + 6, hx0 + hook_w + 4, hy0 + hook_h + 6], radius=24, fill=(0, 0, 0, 90))
            draw.rounded_rectangle([hx0, hy0, hx0 + hook_w, hy0 + hook_h], radius=24, fill=(255, 214, 0), outline=(20, 20, 20), width=5)
            draw.text((self.width // 2, hy0 + 35), "⚡ WHY DO ENGINEERS DO THIS? ⚡", fill=(20, 20, 20), font=self.font_badge, anchor="mm")
            draw.text((self.width // 2, hy0 + 75), self.episode["hook_line"][:40] + "...", fill=(216, 27, 96), font=self.font_caption, anchor="mm")

        # 4. Centered Kinetic Subtitles (Word-by-word active bounce)
        sentences = [s.strip() for s in cur_beat["narration"].split(".") if len(s.strip()) > 3]
        s_idx = min(len(sentences) - 1, int((t % beat_dur) / (beat_dur / max(1, len(sentences)))))
        current_caption = sentences[s_idx]

        # Subtitle Container Pill
        card_w, card_h = 670, 175
        cx0 = (self.width - card_w) // 2
        cy0 = self.height - 240

        draw.rounded_rectangle([cx0 + 4, cy0 + 6, cx0 + card_w + 4, cy0 + card_h + 6], radius=26, fill=(0, 0, 0, 95))
        draw.rounded_rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], radius=26, fill=(20, 24, 33), outline=(97, 175, 239), width=5)

        # Speaker Tag
        role_label = f"🎙️ {cur_beat['character_role']}"
        draw.rounded_rectangle([cx0 + 25, cy0 + 15, cx0 + 200, cy0 + 50], radius=10, fill=(97, 175, 239))
        draw.text((cx0 + 112, cy0 + 32), role_label, fill=(20, 20, 20), font=self.font_badge, anchor="mm")

        # Text with vibrant active bounce
        bounce_scale = 1.0 + 0.02 * math.sin(t * 10.0)
        draw.text((self.width // 2, cy0 + 110), current_caption, fill=(255, 255, 255), font=self.font_caption, anchor="mm")

        # Outro Safe Zone prompt (Last 2.5s)
        if t >= self.total_duration - 2.5:
            draw.rounded_rectangle([cx0 + 80, cy0 - 55, cx0 + card_w - 80, cy0 - 15], radius=15, fill=(255, 214, 0))
            draw.text((self.width // 2, cy0 - 35), "🔔 Subscribe for Daily Mysteries! 🔔", fill=(20, 20, 20), font=self.font_badge, anchor="mm")

        # Convert to RGB array for MoviePy
        rgb_out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_out.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_out)

def render_ricks_video(episode: dict, audio_path: str, output_path: str, duration: float):
    """Composites the complete Rick's Clips style animated short."""
    print("Beginning Rick's Clips video composition...")
    director = RicksClipsDirector(episode, duration, width=720, height=1280)

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
    print(f"Rick's Clips video rendered successfully: {output_path} ({duration:.1f}s)")

# ==========================================
# 3. YOUTUBE UPLOADER
# ==========================================
def upload_to_youtube(video_path: str, episode: dict) -> str:
    """Uploads Rick's Clips micro-documentary short to YouTube."""
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

    title = episode["youtube_title"]
    description = (
        f"{episode['title']}! 🤯🔍\n\n"
        f"The Story Behind It:\n"
        + "\n\n".join([f"⚡ {beat['beat_name']}:\n{beat['narration']}" for beat in episode["beats"]])
        + "\n\n🔔 Subscribe to Rick's Clips for daily engineering paradoxes, history mysteries, and science facts!\n\n"
        "#Shorts #Engineering #Science #History #Curiosity #RicksClips #FunFacts #Education"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": episode["tags"],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,  # General audience edutainment
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
# 4. MAIN ENTRY POINT
# ==========================================
def main():
    print(f"=== Rick's Clips Automation Engine Started ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
    episode = random.choice(RICKS_EPISODES)
    print(f"Selected Episode: {episode['title']}")

    voice_file = "ricks_narration.mp3"
    soundtrack_file = "ricks_soundtrack.wav"
    output_video_file = "ricks_clips_output.mp4"

    # 1. Voiceover
    asyncio.run(generate_narration(episode, voice_file))

    # 2. Sound Design & Lo-Fi Groove Soundtrack
    duration = build_soundtrack(episode, voice_file, soundtrack_file)

    # 3. Video Composition
    render_ricks_video(episode, soundtrack_file, output_video_file, duration)

    # 4. YouTube Upload
    upload_to_youtube(output_video_file, episode)

    print("=== Rick's Clips Episode Completed Successfully ===")

if __name__ == "__main__":
    main()

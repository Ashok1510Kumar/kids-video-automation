#!/usr/bin/env python3
"""
RICKS CLIPS PRODUCTION PIPELINE (@RicksClips3000 Edition)
Features:
- Guaranteed text boundary enforcement (zero overflow/clipping via draw_utils)
- Conversational documentary presentation (Rick narrating beside a dynamic visual display)
- Illustrated story props (Comet airliner, square stress corners, curved oval windows, railroad sun kinks)
- Multi-character voice acting & syncopated lo-fi groove audio
- YouTube Shorts safe zone adherence (all critical visuals kept inside safe margins)
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
    create_airplane_window_prop,
    create_airplane_in_flight_prop,
    create_railroad_diagram_prop
)
from draw_utils import draw_contained_text
from music_generator import generate_nursery_music
from sfx_generator import generate_all_sfx

# Charismatic American male narrator (crisp, warm, rapid 175 WPM)
VOICE_NAME = "en-US-GuyNeural"

# ==========================================
# 1. AUDIO & SOUND DESIGN (175 WPM + LO-FI GROOVE)
# ==========================================
async def generate_narration(episode: dict, output_path: str):
    """Generates conversational, rapid American voiceover."""
    full_text = " ".join([beat["narration"] for beat in episode["beats"]])
    print(f"Synthesizing narration with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(full_text, VOICE_NAME, rate="+9%", pitch="+0Hz")
    await communicate.save(output_path)

def build_soundtrack(episode: dict, voice_path: str, output_soundtrack_path: str) -> float:
    """Mixes voiceover, syncopated lo-fi groove music, and foley sound effects."""
    generate_all_sfx()
    voice_clip = AudioFileClip(voice_path)
    intro_lead = 0.5
    outro_tail = 2.0
    total_duration = intro_lead + voice_clip.duration + outro_tail

    # 1. Background Groove Music (Ducked at -18dB so speech is crystal clear)
    music_temp = "music_temp.wav"
    generate_nursery_music("groove", total_duration, music_temp, bpm=114)
    music_clip = AudioFileClip(music_temp).volumex(0.18)
    voice_clip = voice_clip.volumex(1.0).set_start(intro_lead)

    # 2. Narrative Foley Cues
    sfx_clips = [music_clip, voice_clip]
    sfx_clips.append(AudioFileClip("sfx_pop.wav").volumex(0.32).set_start(intro_lead + 0.5))
    sfx_clips.append(AudioFileClip("sfx_whoosh.wav").volumex(0.30).set_start(intro_lead + 10.0))
    sfx_clips.append(AudioFileClip("sfx_boing.wav").volumex(0.35).set_start(intro_lead + 21.5))
    sfx_clips.append(AudioFileClip("sfx_fanfare.wav").volumex(0.30).set_start(intro_lead + 34.0))

    composite_audio = CompositeAudioClip(sfx_clips).set_duration(total_duration)
    composite_audio.write_audiofile(output_soundtrack_path, fps=44100, logger=None)
    print(f"Soundtrack ready: {output_soundtrack_path} ({total_duration:.1f}s)")
    return total_duration

# ==========================================
# 2. CONVERSATIONAL SCENE DIRECTOR
# ==========================================
class RicksClipsDirector:
    def __init__(self, episode: dict, total_duration: float, width=720, height=1280):
        self.episode = episode
        self.total_duration = total_duration
        self.width = width
        self.height = height

        # Base Studio Stage (Opaque, clean dark theme)
        self.env_bg = create_studio_workshop_environment(width, height)

        # Pre-render Story Props for Dynamic Presentation Screen
        print("Pre-rendering story visual props...")
        self.prop_plane_flight = create_airplane_in_flight_prop((540, 280))
        self.prop_square_stress = create_airplane_window_prop((540, 280), window_type="SQUARE_STRESS")
        self.prop_oval_safe = create_airplane_window_prop((540, 280), window_type="OVAL_SAFE")
        self.prop_rail_gap = create_railroad_diagram_prop((540, 280), hot_sun_kink=False)
        self.prop_sun_kink = create_railroad_diagram_prop((540, 280), hot_sun_kink=True)

        # Pre-render Character Poses
        print("Pre-rendering Rick's Clips character rigs...")
        self.char_narrator_talk = render_ricks_clips_character(costume="NARRATOR", eye_expression="NEUTRAL", mouth_expression="SPEAKING", arm_pose="POINT_RIGHT")
        self.char_narrator_shock = render_ricks_clips_character(costume="NARRATOR", eye_expression="WIDE_SHOCK", mouth_expression="OPEN_O", arm_pose="SHOCKED_HANDS", sweat_drop=True, brow_angle=18.0)
        self.char_narrator_smile = render_ricks_clips_character(costume="NARRATOR", eye_expression="JOY_ARC", mouth_expression="SMILE", arm_pose="POINT_RIGHT")
        self.char_boss_angry = render_ricks_clips_character(costume="BOSS", eye_expression="WIDE_SHOCK", mouth_expression="TEETH_GRIMACE", arm_pose="SHOCKED_HANDS", sweat_drop=True, brow_angle=20.0)
        self.char_engineer_skeptical = render_ricks_clips_character(costume="ENGINEER", eye_expression="SKEPTICAL", mouth_expression="SPEAKING", arm_pose="IDLE", brow_angle=12.0)

        # Typography (Auto-scaling & clean fallback)
        try:
            self.font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
            self.font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
            self.font_caption = ImageFont.truetype("DejaVuSans-Bold.ttf", 27)
            self.font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
        except IOError:
            try:
                self.font_header = ImageFont.truetype("arialbd.ttf", 26)
                self.font_hook = ImageFont.truetype("arialbd.ttf", 28)
                self.font_caption = ImageFont.truetype("arialbd.ttf", 27)
                self.font_badge = ImageFont.truetype("arialbd.ttf", 20)
            except IOError:
                self.font_header = self.font_hook = self.font_caption = self.font_badge = ImageFont.load_default()

    def render_frame(self, t: float) -> np.ndarray:
        frame = self.env_bg.copy()
        draw = ImageDraw.Draw(frame)

        # Determine active beat
        beats = self.episode["beats"]
        num_beats = len(beats)
        beat_dur = max(1.0, (self.total_duration - 1.0) / float(num_beats))
        cur_beat_idx = min(num_beats - 1, int(t / beat_dur))
        cur_beat = beats[cur_beat_idx]

        # ----------------------------------------------------
        # 1. TOP PARADOX HOOK CARD (Strictly Contained, 0s to 7s)
        # ----------------------------------------------------
        if t < 7.0:
            card_x0, card_y0 = 50, 60
            card_x1, card_y1 = self.width - 50, 165
            # Card background
            draw.rounded_rectangle([card_x0 + 4, card_y0 + 5, card_x1 + 4, card_y1 + 5], radius=18, fill=(0, 0, 0, 140))
            draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=18, fill=(255, 214, 0), outline=(20, 20, 20), width=4)

            # Badge pill
            badge_w, badge_h = 320, 30
            bx0 = (self.width - badge_w) // 2
            draw.rounded_rectangle([bx0, card_y0 + 8, bx0 + badge_w, card_y0 + 8 + badge_h], radius=10, fill=(20, 20, 20))
            draw.text(((bx0 + bx0 + badge_w) // 2, card_y0 + 23), "ENGINEERING PARADOX", fill=(255, 214, 0), font=self.font_badge, anchor="mm")

            # Word-wrapped Hook Text strictly inside bounding box
            draw_contained_text(
                draw=draw,
                text=self.episode["hook_line"],
                box=(card_x0 + 15, card_y0 + 42, card_x1 - 15, card_y1 - 8),
                font=self.font_hook,
                fill_color=(194, 24, 91),
                align="center"
            )

        # ----------------------------------------------------
        # 2. DYNAMIC PRESENTATION SCREEN VISUALS (Upper Center)
        # ----------------------------------------------------
        screen_x = 90
        screen_y = 230
        ep_id = self.episode["id"]

        if ep_id == "airplane_windows":
            if cur_beat_idx == 0:
                frame.alpha_composite(self.prop_plane_flight, (screen_x, screen_y))
            elif cur_beat_idx in [1, 2]:
                frame.alpha_composite(self.prop_square_stress, (screen_x, screen_y))
            else:
                frame.alpha_composite(self.prop_oval_safe, (screen_x, screen_y))
        else:
            # Railroads or general engineering
            if cur_beat_idx in [0, 1]:
                frame.alpha_composite(self.prop_rail_gap, (screen_x, screen_y))
            elif cur_beat_idx == 2:
                frame.alpha_composite(self.prop_sun_kink, (screen_x, screen_y))
            else:
                frame.alpha_composite(self.prop_rail_gap, (screen_x, screen_y))

        # ----------------------------------------------------
        # 3. CONVERSATIONAL CHARACTER (Standing & Narrating)
        # ----------------------------------------------------
        idle_bounce = int(3 * math.sin(t * 6.0))
        role = cur_beat["character_role"]

        if role == "BOSS":
            char_sprite = self.char_boss_angry
        elif role == "ENGINEER":
            char_sprite = self.char_engineer_skeptical
        elif cur_beat_idx == 2:
            char_sprite = self.char_narrator_shock
        elif cur_beat_idx == 3:
            char_sprite = self.char_narrator_smile
        else:
            char_sprite = self.char_narrator_talk

        # Host Rick stands on the left/center foreground, gesturing towards the presentation screen
        char_x = int(self.width * 0.22)
        char_y = 520 + idle_bounce
        frame.alpha_composite(char_sprite, (char_x, char_y))

        # ----------------------------------------------------
        # 4. CAPTION CARD (Strictly Contained, Multi-Line Wrapped)
        # ----------------------------------------------------
        sentences = [s.strip() for s in cur_beat["narration"].split(".") if len(s.strip()) > 3]
        s_idx = min(len(sentences) - 1, int((t % beat_dur) / (beat_dur / max(1, len(sentences)))))
        current_sentence = sentences[s_idx]

        # YouTube Shorts Safe Zone for Subtitles (Kept away from right-side buttons and bottom title)
        card_x0 = 45
        card_y0 = self.height - 290
        card_x1 = self.width - 45
        card_y1 = self.height - 120

        # High-contrast dark container pill with cyan border
        draw.rounded_rectangle([card_x0 + 4, card_y0 + 5, card_x1 + 4, card_y1 + 5], radius=22, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=22, fill=(18, 24, 38), outline=(97, 175, 239), width=4)

        # Clean Speaker Badge (No missing emoji boxes!)
        badge_text = f"SPEAKER: {role}"
        draw.rounded_rectangle([card_x0 + 20, card_y0 + 12, card_x0 + 240, card_y0 + 42], radius=10, fill=(97, 175, 239))
        draw.text((card_x0 + 130, card_y0 + 27), badge_text, fill=(15, 20, 25), font=self.font_badge, anchor="mm")

        # RENDER WORD-WRAPPED CAPTION (Never bleeds outside the container)
        draw_contained_text(
            draw=draw,
            text=current_sentence,
            box=(card_x0 + 25, card_y0 + 50, card_x1 - 25, card_y1 - 10),
            font=self.font_caption,
            fill_color=(255, 255, 255),
            line_spacing=6,
            align="center"
        )

        # ----------------------------------------------------
        # 5. OUTRO SUBSCRIBER BANNER (Last 2.5 seconds)
        # ----------------------------------------------------
        if t >= self.total_duration - 2.5:
            banner_x0, banner_y0 = 60, card_y0 - 55
            banner_x1, banner_y1 = self.width - 60, card_y0 - 15
            draw.rounded_rectangle([banner_x0, banner_y0, banner_x1, banner_y1], radius=14, fill=(255, 214, 0), outline=(20, 20, 20), width=3)
            draw.text(((banner_x0 + banner_x1) // 2, (banner_y0 + banner_y1) // 2), "SUBSCRIBE FOR DAILY MYSTERIES!", fill=(20, 20, 20), font=self.font_badge, anchor="mm")

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
            "selfDeclaredMadeForKids": False,
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

    # 2. Sound Design & Mastered Soundtrack
    duration = build_soundtrack(episode, voice_file, soundtrack_file)

    # 3. Video Composition
    render_ricks_video(episode, soundtrack_file, output_video_file, duration)

    # 4. YouTube Upload
    upload_to_youtube(output_video_file, episode)

    print("=== Rick's Clips Episode Completed Successfully ===")

if __name__ == "__main__":
    main()

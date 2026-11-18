#!/usr/bin/env python3
"""
RICKS CLIPS PRODUCTION PIPELINE (GOOGLE FLOW + 30FPS SMOOTH MOTION)
Features:
- Google Gemini Flow: Dynamically researches & generates high-retention paradox scripts
- Silky-Smooth 30 FPS Render with cubic easing and alpha cross-dissolves
- Pure floating viral captions with bold black stroke (NO BOXES)
- Conversational documentary presentation with dynamic visual display
- YouTube Shorts safe zone adherence
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
from script_generator import get_daily_episode
from character_rick import render_ricks_clips_character
from environment_rick import (
    create_studio_workshop_environment,
    create_airplane_window_prop,
    create_airplane_in_flight_prop,
    create_railroad_diagram_prop
)
from draw_utils import draw_floating_subtitles
from smooth_motion import ease_in_out_quad, smooth_crossfade
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
# 2. CONVERSATIONAL SCENE DIRECTOR (30 FPS)
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

        # Typography
        try:
            self.font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            self.font_caption = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            self.font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        except IOError:
            try:
                self.font_hook = ImageFont.truetype("arialbd.ttf", 32)
                self.font_caption = ImageFont.truetype("arialbd.ttf", 32)
                self.font_badge = ImageFont.truetype("arialbd.ttf", 22)
            except IOError:
                self.font_hook = self.font_caption = self.font_badge = ImageFont.load_default()

    def get_current_props(self, cur_beat_idx: int, t_in_beat: float, beat_dur: float) -> Image.Image:
        """Returns the active prop image with smooth alpha cross-dissolves."""
        ep_id = self.episode.get("id", "")
        # Select prop based on episode theme
        if "plane" in ep_id or "window" in ep_id or "air" in ep_id:
            props = [self.prop_plane_flight, self.prop_square_stress, self.prop_square_stress, self.prop_oval_safe]
        else:
            props = [self.prop_rail_gap, self.prop_rail_gap, self.prop_sun_kink, self.prop_rail_gap]

        cur_prop = props[min(len(props) - 1, cur_beat_idx)]

        # Smooth cross-fade transition in first 0.5s of new beat
        transition_duration = 0.5
        if cur_beat_idx > 0 and t_in_beat < transition_duration:
            prev_prop = props[cur_beat_idx - 1]
            progress = t_in_beat / transition_duration
            return smooth_crossfade(prev_prop, cur_prop, progress)

        return cur_prop

    def render_frame(self, t: float) -> np.ndarray:
        frame = self.env_bg.copy()
        draw = ImageDraw.Draw(frame)

        # Determine active beat
        beats = self.episode["beats"]
        num_beats = len(beats)
        beat_dur = max(1.0, (self.total_duration - 1.0) / float(num_beats))
        cur_beat_idx = min(num_beats - 1, int(t / beat_dur))
        t_in_beat = t % beat_dur
        cur_beat = beats[cur_beat_idx]

        # ----------------------------------------------------
        # 1. FLOATING TOP HOOK HEADLINE (NO BOXES, NO BORDERS)
        # ----------------------------------------------------
        if t < 7.0:
            draw_floating_subtitles(
                draw=draw,
                text=self.episode["hook_line"],
                center_pos=(self.width // 2, 110),
                font=self.font_hook,
                max_width=600,
                fill_color=(255, 225, 0),      # Bright Viral Yellow
                stroke_color=(0, 0, 0),         # Bold 4px Black Stroke
                stroke_width=4,
                line_spacing=8
            )

        # ----------------------------------------------------
        # 2. DYNAMIC PRESENTATION SCREEN (SMOOTH CROSS-DISSOLVES)
        # ----------------------------------------------------
        screen_x = 90
        screen_y = 230
        active_prop = self.get_current_props(cur_beat_idx, t_in_beat, beat_dur)
        frame.alpha_composite(active_prop, (screen_x, screen_y))

        # ----------------------------------------------------
        # 3. CONVERSATIONAL CHARACTER (SMOOTH EASING & SWAY)
        # ----------------------------------------------------
        # Smooth harmonic breathing & idle motion
        idle_bounce = int(3.5 * math.sin(t * 5.0))
        role = cur_beat.get("character_role", "NARRATOR")

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

        char_x = int(self.width * 0.22)
        char_y = 520 + idle_bounce
        frame.alpha_composite(char_sprite, (char_x, char_y))

        # ----------------------------------------------------
        # 4. PURE FLOATING VIRAL SUBTITLES (NO BOXES, NO BORDERS)
        # ----------------------------------------------------
        sentences = [s.strip() for s in cur_beat["narration"].split(".") if len(s.strip()) > 3]
        if not sentences:
            sentences = [cur_beat["narration"]]
        s_idx = min(len(sentences) - 1, int(t_in_beat / (beat_dur / max(1, len(sentences)))))
        current_sentence = sentences[s_idx]

        # Draw clean, floating, outlined subtitles directly on screen
        draw_floating_subtitles(
            draw=draw,
            text=current_sentence,
            center_pos=(self.width // 2, self.height - 180),
            font=self.font_caption,
            max_width=580,
            fill_color=(255, 255, 255),      # Pure Crisp White
            stroke_color=(0, 0, 0),          # Bold 4px Black Outline
            stroke_width=4,
            line_spacing=8
        )

        # ----------------------------------------------------
        # 5. FLOATING OUTRO PROMPT (Last 2.5 seconds, NO BOX)
        # ----------------------------------------------------
        if t >= self.total_duration - 2.5:
            draw.text(
                (self.width // 2, self.height - 270),
                "SUBSCRIBE FOR DAILY MYSTERIES!",
                font=self.font_badge,
                fill=(255, 225, 0),
                stroke_width=3,
                stroke_fill=(0, 0, 0),
                anchor="mm"
            )

        # Convert to RGB array for MoviePy
        rgb_out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_out.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_out)

def render_ricks_video(episode: dict, audio_path: str, output_path: str, duration: float):
    """Composites the complete Rick's Clips style animated short at 30 FPS."""
    print("Beginning Rick's Clips video composition (30 FPS Smooth Motion)...")
    director = RicksClipsDirector(episode, duration, width=720, height=1280)

    audio_clip = AudioFileClip(audio_path)
    # Upgraded from 24 FPS to 30 FPS for silky-smooth fluid motion!
    video = VideoClip(lambda t: director.render_frame(t), duration=duration).set_audio(audio_clip)

    video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None
    )
    print(f"Rick's Clips video rendered successfully: {output_path} (30 FPS, {duration:.1f}s)")

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
            "tags": episode.get("tags", ["engineering", "science", "curiosity", "shorts"]),
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
# 4. MAIN ENTRY POINT (GOOGLE FLOW)
# ==========================================
def main():
    print(f"=== Rick's Clips Automation Engine Started ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
    
    # 1. Google Gemini Script Flow (generates dynamic fresh script daily or uses curated fallback)
    episode = get_daily_episode()
    print(f"Selected Story: {episode['title']}")

    voice_file = "ricks_narration.mp3"
    soundtrack_file = "ricks_soundtrack.wav"
    output_video_file = "ricks_clips_output.mp4"

    # 2. Voiceover
    asyncio.run(generate_narration(episode, voice_file))

    # 3. Sound Design & Mastered Soundtrack
    duration = build_soundtrack(episode, voice_file, soundtrack_file)

    # 4. Video Composition (30 FPS Smooth Motion)
    render_ricks_video(episode, soundtrack_file, output_video_file, duration)

    # 5. YouTube Upload
    upload_to_youtube(output_video_file, episode)

    print("=== Rick's Clips Episode Completed Successfully ===")

if __name__ == "__main__":
    main()

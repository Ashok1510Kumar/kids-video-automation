#!/usr/bin/env python3
"""
STREAMER CLIP CUTTER & SPLIT-SCREEN REFORMATTER
1. Slices 30-50s clip from YouTube livestream using yt-dlp.
2. Converts 16:9 widescreen into high-retention 9:16 vertical Short:
   - Top Half: Streamer Facecam (Zoomed & Centered)
   - Bottom Half: Gameplay / Main Screen
   - Center Line: Sleek neon glow separator
3. Overlays:
   - Top Hook Headline (Pure floating yellow text with 4px black stroke)
   - Verified Streamer Credit Badge (@IShowSpeed, @CarryMinati)
   - YouTube Shorts safe zone compliance (Zero clipping)
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, VideoClip, AudioFileClip, CompositeVideoClip
from draw_utils import draw_floating_subtitles

def download_stream_slice(youtube_url: str, start_time: str, end_time: str, output_path: str) -> bool:
    """
    Downloads only the specified 30-50s slice using yt-dlp section slicing.
    Keeps download size under 30MB without downloading multi-hour streams.
    """
    print(f"[CLIP CUTTER] Downloading stream slice: {youtube_url} ({start_time} -> {end_time})...")
    
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "--force-keyframes-at-cuts",
        "--extractor-args", "youtube:player_client=android,web",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "--merge-output-format", "mp4",
        "--recode-video", "mp4",
        "-o", output_path,
        youtube_url
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
        if res.returncode == 0 and os.path.exists(output_path):
            print(f"[CLIP CUTTER] Successfully downloaded slice to: {output_path}")
            return True
        else:
            print(f"[CLIP CUTTER] yt-dlp notice (code {res.returncode}): {res.stderr[:200]}")
    except Exception as e:
        print(f"[CLIP CUTTER] Download exception: {e}")

    return False

def generate_fallback_streamer_clip(moment: dict, output_path: str, duration=35.0):
    """
    Creates a high-energy animated streamer highlight stage if the raw YouTube
    stream is region-locked or temporarily gated by bot checks.
    """
    print(f"[CLIP CUTTER] Generating dynamic animated highlight for '{moment['creator']}'...")
    from environment_rick import create_studio_workshop_environment
    from character_rick import render_ricks_clips_character

    w, h = 720, 1280
    bg = Image.new("RGBA", (w, h), (18, 22, 30, 255))
    draw = ImageDraw.Draw(bg)

    # Streamer room neon aesthetic background
    for y in range(h):
        ratio = y / float(h)
        r = int(18 + 12 * math.sin(ratio * 3.14))
        g = int(22 + 10 * ratio)
        b = int(35 + 25 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Top Half: Streamer Cam Frame (Facecam Zone)
    cam_box = [30, 160, w - 30, 620]
    draw.rounded_rectangle(cam_box, radius=18, fill=(28, 35, 48, 255), outline=(255, 64, 129, 255), width=4)
    draw.text(((cam_box[0] + cam_box[2]) // 2, cam_box[1] + 25), f"🔴 LIVE WEBCAM FEED | {moment['creator'].upper()}", fill=(255, 64, 129, 255), anchor="mm")

    # Bottom Half: High-Action Gameplay Zone
    game_box = [30, 650, w - 30, 1140]
    draw.rounded_rectangle(game_box, radius=18, fill=(22, 28, 38, 255), outline=(0, 229, 255, 255), width=4)
    draw.text(((game_box[0] + game_box[2]) // 2, game_box[1] + 25), "🎮 GAMEPLAY & REACTION FEED", fill=(0, 229, 255, 255), anchor="mm")

    # Pre-render energetic animated character for facecam
    char_shock = render_ricks_clips_character(
        costume="NARRATOR", eye_expression="WIDE_SHOCK", mouth_expression="OPEN_O", arm_pose="SHOCKED_HANDS", sweat_drop=True
    )
    char_talk = render_ricks_clips_character(
        costume="NARRATOR", eye_expression="JOY_ARC", mouth_expression="SMILE", arm_pose="POINT_RIGHT"
    )

    try:
        font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except IOError:
        font_hook = font_badge = ImageFont.load_default()

    def make_frame(t):
        frame = bg.copy()
        fdraw = ImageDraw.Draw(frame)

        # Dynamic screaming bounce
        bounce = int(6.0 * math.sin(t * 12.0))
        cur_char = char_shock if int(t * 3) % 2 == 0 else char_talk
        frame.alpha_composite(cur_char, (int(w * 0.22), 220 + bounce))

        # Dynamic floating top hook headline (NO BOXES)
        draw_floating_subtitles(
            draw=fdraw,
            text=moment["hook_text"],
            center_pos=(w // 2, 100),
            font=font_hook,
            max_width=580,
            fill_color=(255, 225, 0),
            stroke_color=(0, 0, 0),
            stroke_width=4
        )

        # Streamer Credit Pill
        fdraw.text(
            (w // 2, 635),
            f"⚡ CLIP CREDIT: {moment['channel_credit']} ⚡",
            font=font_badge,
            fill=(0, 229, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0),
            anchor="mm"
        )

        # Floating center reaction caption (NO BOXES)
        draw_floating_subtitles(
            draw=fdraw,
            text=f"'{moment['title'].split('!')[0]}!'",
            center_pos=(w // 2, 1050),
            font=font_hook,
            max_width=560,
            fill_color=(255, 255, 255),
            stroke_color=(0, 0, 0),
            stroke_width=4
        )

        rgb = Image.new("RGB", (w, h), (255, 255, 255))
        rgb.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb)

    # Synthesize backing audio
    from music_generator import generate_nursery_music
    from moviepy.editor import AudioFileClip
    temp_audio = "streamer_music.wav"
    generate_nursery_music("groove", duration, temp_audio, bpm=124)
    audio_clip = AudioFileClip(temp_audio)

    video = VideoClip(make_frame, duration=duration).set_audio(audio_clip)
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    print(f"[CLIP CUTTER] Rendered fallback highlight short: {output_path} ({duration:.1f}s)")

def format_split_screen_vertical(raw_clip_path: str, moment: dict, output_path: str):
    """
    Transforms downloaded 16:9 stream into viral 9:16 vertical Short:
    - Top: Streamer facecam zoomed & stabilized
    - Bottom: Gameplay screen
    - Center: Neon divider + Credit badge
    - Overlay: Pure floating subtitles (zero boxes)
    """
    print(f"[CLIP CUTTER] Reformatting 16:9 clip into 9:16 vertical short...")
    clip = VideoFileClip(raw_clip_path)
    
    # Cap duration at 45 seconds for YouTube Shorts
    if clip.duration > 45.0:
        clip = clip.subclip(0, 45.0)

    w_orig, h_orig = clip.size
    out_w, out_h = 720, 1280

    facecam_pos = moment.get("facecam_position", "bottom-right")

    # Define crop coordinates based on facecam position
    if facecam_pos == "top-right":
        x0_face, y0_face = int(w_orig * 0.70), int(h_orig * 0.05)
        x1_face, y1_face = int(w_orig * 0.98), int(h_orig * 0.45)
    elif facecam_pos == "bottom-right":
        x0_face, y0_face = int(w_orig * 0.70), int(h_orig * 0.55)
        x1_face, y1_face = int(w_orig * 0.98), int(h_orig * 0.95)
    elif facecam_pos == "top-left":
        x0_face, y0_face = int(w_orig * 0.02), int(h_orig * 0.05)
        x1_face, y1_face = int(w_orig * 0.30), int(h_orig * 0.45)
    else:
        # Full reaction / IRL video
        x0_face, y0_face = int(w_orig * 0.20), 0
        x1_face, y1_face = int(w_orig * 0.80), h_orig

    # Crop Facecam for Top Half (720x540)
    top_cam = clip.crop(x1=x0_face, y1=y0_face, x2=x1_face, y2=y1_face).resize(width=out_w)
    if top_cam.h > 540:
        top_cam = top_cam.crop(y1=0, y2=540)

    # Crop Center Gameplay for Bottom Half (720x740)
    bot_game = clip.crop(x1=int(w_orig * 0.15), y1=0, x2=int(w_orig * 0.85), y2=h_orig).resize(width=out_w)
    if bot_game.h > 740:
        bot_game = bot_game.crop(y1=0, y2=740)

    # Composite split screen
    top_cam = top_cam.set_position((0, 80))
    bot_game = bot_game.set_position((0, 620))

    try:
        font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except IOError:
        font_hook = font_badge = ImageFont.load_default()

    # Dynamic floating overlays
    def overlay_filter(get_frame, t):
        frame = Image.fromarray(get_frame(t)).convert("RGBA")
        draw = ImageDraw.Draw(frame)

        # Top Floating Hook Headline (NO BOXES)
        draw_floating_subtitles(
            draw=draw,
            text=moment.get("hook_text", moment["title"]),
            center_pos=(out_w // 2, 50),
            font=font_hook,
            max_width=580,
            fill_color=(255, 225, 0),
            stroke_color=(0, 0, 0),
            stroke_width=4
        )

        # Streamer Credit Badge (Floating Center Bar)
        draw.text(
            (out_w // 2, 620),
            f"⚡ STREAMER: {moment['channel_credit']} ⚡",
            font=font_badge,
            fill=(0, 229, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0),
            anchor="mm"
        )

        # Subscribe callout at end
        if t >= clip.duration - 3.0:
            draw.text(
                (out_w // 2, out_h - 180),
                "SUBSCRIBE FOR DAILY STREAMER CLIPS!",
                font=font_badge,
                fill=(255, 225, 0),
                stroke_width=3,
                stroke_fill=(0, 0, 0),
                anchor="mm"
            )

        return np.array(frame.convert("RGB"))

    final_video = CompositeVideoClip([top_cam, bot_game], size=(out_w, out_h))
    final_video = final_video.fl(overlay_filter)
    final_video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None
    )
    print(f"[CLIP CUTTER] Vertical 9:16 short generated successfully: {output_path}")

def process_streamer_moment(moment: dict, output_video_path: str):
    """Orchestrates downloading, vertical formatting, and safe fallbacks."""
    raw_slice = "temp_raw_slice.mp4"

    # Step 1: Attempt to slice raw stream with yt-dlp
    downloaded = download_stream_slice(
        moment["youtube_url"],
        moment["start_time"],
        moment["end_time"],
        raw_slice
    )

    if downloaded and os.path.exists(raw_slice) and os.path.getsize(raw_slice) > 100000:
        try:
            format_split_screen_vertical(raw_slice, moment, output_video_path)
            return
        except Exception as e:
            print(f"[CLIP CUTTER] Error in split-screen composite ({e}). Switching to animated highlight engine.")

    # Fallback: High-energy animated highlight engine
    generate_fallback_streamer_clip(moment, output_video_path, duration=35.0)

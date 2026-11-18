#!/usr/bin/env python3
"""
STREAMER CLIP CUTTER & SPLIT-SCREEN REFORMATTER
1. Slices 30-50s clip from YouTube livestream using yt-dlp.
2. Converts 16:9 widescreen into high-retention 9:16 vertical Short:
   - Full IRL Mode: High-impact 9:16 vertical crop centered on creator.
   - Gaming Mode: Top facecam zoomed, bottom gameplay action.
3. Overlays:
   - Top Hook Headline (Pure floating yellow text with 4px black stroke, NO BOXES)
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

    # Uses iOS player client which does not trigger datacenter IP bot detection
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "--force-keyframes-at-cuts",
        "--extractor-args", "youtube:player_client=ios,android,web",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", output_path,
        youtube_url
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            print(f"[CLIP CUTTER] Successfully downloaded slice to: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[CLIP CUTTER] yt-dlp notice (code {res.returncode}): {res.stderr[:300]}")
    except Exception as e:
        print(f"[CLIP CUTTER] Download exception: {e}")

    return False

def format_split_screen_vertical(raw_clip_path: str, moment: dict, output_path: str):
    """
    Transforms downloaded 16:9 stream into viral 9:16 vertical Short:
    - Real video of the creator filling the screen!
    - Full IRL mode or Split-Screen Facecam + Gameplay
    - Pure floating subtitles (no boxes)
    """
    print(f"[CLIP CUTTER] Reformatting real video clip into 9:16 vertical short...")
    clip = VideoFileClip(raw_clip_path)

    # Cap duration at 45 seconds for YouTube Shorts
    if clip.duration > 45.0:
        clip = clip.subclip(0, 45.0)

    w_orig, h_orig = clip.size
    out_w, out_h = 720, 1280

    facecam_pos = moment.get("facecam_position", "full")

    if facecam_pos == "full":
        # Full IRL / Reaction Clip: Center crop 9:16 vertical so Speed fills the vertical frame!
        target_aspect = 9.0 / 16.0
        current_aspect = w_orig / float(h_orig)
        if current_aspect > target_aspect:
            new_w = int(h_orig * target_aspect)
            x_center = w_orig // 2
            x1 = x_center - new_w // 2
            x2 = x_center + new_w // 2
            main_video = clip.crop(x1=x1, y1=0, x2=x2, y2=h_orig).resize((out_w, out_h))
        else:
            main_video = clip.resize((out_w, out_h))
        composite_layers = [main_video]
    else:
        # Gaming Split-Screen: Zoom Facecam on Top, Gameplay on Bottom
        if facecam_pos == "top-right":
            x0_f, y0_f = int(w_orig * 0.70), int(h_orig * 0.05)
            x1_f, y1_f = int(w_orig * 0.98), int(h_orig * 0.45)
        elif facecam_pos == "bottom-right":
            x0_f, y0_f = int(w_orig * 0.70), int(h_orig * 0.55)
            x1_f, y1_f = int(w_orig * 0.98), int(h_orig * 0.98)
        elif facecam_pos == "top-left":
            x0_f, y0_f = int(w_orig * 0.02), int(h_orig * 0.05)
            x1_f, y1_f = int(w_orig * 0.32), int(h_orig * 0.45)
        else:
            x0_f, y0_f = int(w_orig * 0.02), int(h_orig * 0.55)
            x1_f, y1_f = int(w_orig * 0.32), int(h_orig * 0.98)

        top_cam = clip.crop(x1=x0_f, y1=y0_f, x2=x1_f, y2=y1_f).resize(width=out_w)
        if top_cam.h > 540:
            top_cam = top_cam.crop(y1=0, y2=540)

        bot_game = clip.crop(x1=int(w_orig * 0.15), y1=0, x2=int(w_orig * 0.85), y2=h_orig).resize(width=out_w)
        if bot_game.h > 740:
            bot_game = bot_game.crop(y1=0, y2=740)

        top_cam = top_cam.set_position((0, 80))
        bot_game = bot_game.set_position((0, 620))
        composite_layers = [top_cam, bot_game]

    try:
        font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except IOError:
        font_hook = font_badge = ImageFont.load_default()

    # Dynamic floating overlays (Zero boxes)
    def overlay_filter(get_frame, t):
        frame = Image.fromarray(get_frame(t)).convert("RGBA")
        draw = ImageDraw.Draw(frame)

        # Top Floating Hook Headline (NO BOXES)
        draw_floating_subtitles(
            draw=draw,
            text=moment.get("hook_text", moment["title"]),
            center_pos=(out_w // 2, 70),
            font=font_hook,
            max_width=580,
            fill_color=(255, 225, 0),      # Bright Viral Yellow
            stroke_color=(0, 0, 0),         # Bold 4px Black Outline
            stroke_width=4
        )

        # Streamer Credit Watermark (Bottom / Center)
        draw.text(
            (out_w // 2, out_h - 120),
            f"⚡ STREAMER: {moment['channel_credit']} ⚡",
            font=font_badge,
            fill=(0, 229, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0),
            anchor="mm"
        )

        # Floating Subtitle / Reaction text at bottom
        if t < clip.duration - 3.0:
            draw_floating_subtitles(
                draw=draw,
                text=moment["title"].split("!")[0] + "!",
                center_pos=(out_w // 2, out_h - 220),
                font=font_hook,
                max_width=560,
                fill_color=(255, 255, 255),
                stroke_color=(0, 0, 0),
                stroke_width=4
            )
        else:
            # Subscribe callout at end
            draw.text(
                (out_w // 2, out_h - 220),
                "SUBSCRIBE FOR DAILY VIRAL CLIPS!",
                font=font_badge,
                fill=(255, 225, 0),
                stroke_width=3,
                stroke_fill=(0, 0, 0),
                anchor="mm"
            )

        return np.array(frame.convert("RGB"))

    final_video = CompositeVideoClip(composite_layers, size=(out_w, out_h))
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

def generate_fallback_streamer_clip(moment: dict, output_path: str, duration=35.0):
    """Fallback only if network entirely fails."""
    print(f"[CLIP CUTTER] Fallback animated engine called for '{moment['creator']}'...")
    from character_rick import render_ricks_clips_character
    w, h = 720, 1280
    bg = Image.new("RGBA", (w, h), (18, 22, 30, 255))
    draw = ImageDraw.Draw(bg)

    try:
        font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except IOError:
        font_hook = font_badge = ImageFont.load_default()

    char_shock = render_ricks_clips_character(costume="NARRATOR", eye_expression="WIDE_SHOCK", mouth_expression="OPEN_O", arm_pose="SHOCKED_HANDS", sweat_drop=True)

    def make_frame(t):
        frame = bg.copy()
        fdraw = ImageDraw.Draw(frame)
        bounce = int(5.0 * math.sin(t * 10.0))
        frame.alpha_composite(char_shock, (int(w * 0.22), 350 + bounce))

        draw_floating_subtitles(fdraw, moment["hook_text"], (w // 2, 100), font_hook, max_width=580, fill_color=(255, 225, 0), stroke_color=(0, 0, 0), stroke_width=4)
        fdraw.text((w // 2, 700), f"⚡ CLIP CREDIT: {moment['channel_credit']} ⚡", font=font_badge, fill=(0, 229, 255), stroke_width=3, stroke_fill=(0, 0, 0), anchor="mm")
        draw_floating_subtitles(fdraw, moment["title"].split("!")[0] + "!", (w // 2, 1050), font_hook, max_width=560, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=4)

        rgb = Image.new("RGB", (w, h), (255, 255, 255))
        rgb.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb)

    from music_generator import generate_nursery_music
    temp_audio = "streamer_music.wav"
    generate_nursery_music("groove", duration, temp_audio, bpm=124)
    audio_clip = AudioFileClip(temp_audio)
    video = VideoClip(make_frame, duration=duration).set_audio(audio_clip)
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)

def process_streamer_moment(moment: dict, output_video_path: str):
    """Orchestrates downloading real footage, vertical formatting, and safe fallbacks."""
    raw_slice = "temp_raw_slice.mp4"

    # Step 1: Download real video slice from YouTube
    downloaded = download_stream_slice(
        moment["youtube_url"],
        moment["start_time"],
        moment["end_time"],
        raw_slice
    )

    if downloaded and os.path.exists(raw_slice) and os.path.getsize(raw_slice) > 10000:
        try:
            format_split_screen_vertical(raw_slice, moment, output_video_path)
            return
        except Exception as e:
            print(f"[CLIP CUTTER] Error in formatting real video ({e}). Switching to fallback.")

    # Fallback only if download completely blocked
    generate_fallback_streamer_clip(moment, output_video_path, duration=35.0)

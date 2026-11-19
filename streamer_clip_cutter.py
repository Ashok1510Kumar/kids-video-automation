#!/usr/bin/env python3
"""
STREAMER CLIP CUTTER & SPLIT-SCREEN REFORMATTER
1. Slices 30-45s clip from official livestreams using yt-dlp + FFmpeg.
2. Converts 16:9 widescreen into high-retention 9:16 vertical Short:
   - Full IRL / Reaction Mode: Vertical center crop on streamer.
   - Gaming Mode: Top facecam zoomed, bottom gameplay action.
3. Pure floating text overlays (NO BOXES, NO CONTAINERS, NO CARTOONS):
   - Top Hook Headline (Pure floating yellow text with 4px black stroke)
   - Verified Streamer Credit Badge (@IShowSpeed)
   - Bottom Reaction Subtitle (Pure floating white text with 4px black stroke)
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, CompositeVideoClip
from draw_utils import draw_floating_subtitles

def download_stream_slice(youtube_url: str, start_time: str, end_time: str, output_path: str) -> bool:
    """
    Downloads only the specified 30-45s slice using yt-dlp and ffmpeg.
    Tries multiple client profiles (android, web, ios) to avoid bot detection.
    """
    print(f"[CLIP CUTTER] Downloading stream slice: {youtube_url} ({start_time} -> {end_time})...")

    # Clean up any leftover file
    if os.path.exists(output_path):
        os.remove(output_path)

    # Strategy 1: Direct stream extraction via yt-dlp -g + FFmpeg fast slice
    print("[CLIP CUTTER] Strategy 1: Extracting direct stream URL via yt-dlp...")
    try:
        g_cmd = [
            sys.executable, "-m", "yt_dlp",
            "-g",
            "-f", "best[height<=720]/best",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=android,web",
            youtube_url
        ]
        g_res = subprocess.run(g_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45)
        if g_res.returncode == 0 and g_res.stdout.strip():
            stream_urls = g_res.stdout.strip().split("\n")
            direct_url = stream_urls[0]
            print(f"[CLIP CUTTER] Stream URL resolved successfully. Slicing with FFmpeg ({start_time} -> {end_time})...")

            # Calculate duration in seconds
            def parse_time(t_str):
                parts = [float(x) for x in t_str.split(":")]
                if len(parts) == 3:
                    return parts[0] * 3600 + parts[1] * 60 + parts[2]
                elif len(parts) == 2:
                    return parts[0] * 60 + parts[1]
                return parts[0]

            duration = max(15.0, parse_time(end_time) - parse_time(start_time))

            ff_cmd = [
                "ffmpeg", "-y",
                "-ss", start_time,
                "-i", direct_url,
                "-t", str(int(duration)),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                output_path
            ]
            ff_res = subprocess.run(ff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
            if ff_res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                print(f"[CLIP CUTTER] Strategy 1 SUCCESS! Raw slice: {output_path} ({os.path.getsize(output_path)} bytes)")
                return True
            else:
                print(f"[CLIP CUTTER] FFmpeg direct slice note: {ff_res.stderr[:200]}")
    except Exception as e:
        print(f"[CLIP CUTTER] Strategy 1 exception: {e}")

    # Strategy 2: Standard yt-dlp section slicing with remote EJS solver
    print("[CLIP CUTTER] Strategy 2: Section slicing via yt-dlp...")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "--force-keyframes-at-cuts",
        "--remote-components", "ejs:github",
        "--extractor-args", "youtube:player_client=android,web",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "--merge-output-format", "mp4",
        "-o", output_path,
        youtube_url
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            print(f"[CLIP CUTTER] Strategy 2 SUCCESS! Raw slice: {output_path} ({os.path.getsize(output_path)} bytes)")
            return True
        else:
            print(f"[CLIP CUTTER] Strategy 2 notice (code {res.returncode}): {res.stderr[:300]}")
    except Exception as e:
        print(f"[CLIP CUTTER] Strategy 2 exception: {e}")

    # Strategy 3: Try with cookies if provided
    cookie_file = "youtube_cookies.txt"
    cookies_content = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if cookies_content:
        print("[CLIP CUTTER] Strategy 3: Attempting with cookies...")
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(cookies_content)
        cmd_cookies = cmd + ["--cookies", cookie_file]
        try:
            res_c = subprocess.run(cmd_cookies, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
            if res_c.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                print(f"[CLIP CUTTER] Strategy 3 SUCCESS! Raw slice: {output_path} ({os.path.getsize(output_path)} bytes)")
                return True
        except Exception as e:
            print(f"[CLIP CUTTER] Strategy 3 exception: {e}")

    return False

def format_split_screen_vertical(raw_clip_path: str, moment: dict, output_path: str):
    """
    Transforms downloaded 16:9 stream into viral 9:16 vertical Short:
    - Real video of the creator filling the screen (NO CARTOONS).
    - Pure floating subtitles (NO BOXES, NO BACKGROUND CONTAINERS).
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
        font_hook = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
        font_badge = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except IOError:
        font_hook = font_badge = ImageFont.load_default()

    # Dynamic floating overlays (Zero boxes, floating text with black stroke)
    def overlay_filter(get_frame, t):
        frame = Image.fromarray(get_frame(t)).convert("RGBA")
        draw = ImageDraw.Draw(frame)

        # Top Floating Hook Headline (NO BOXES, bold 4px black stroke)
        draw_floating_subtitles(
            draw=draw,
            text=moment.get("hook_text", moment["title"]),
            center_pos=(out_w // 2, 75),
            font=font_hook,
            max_width=580,
            fill_color=(255, 225, 0),      # Bright Viral Yellow
            stroke_color=(0, 0, 0),         # Bold 4px Black Outline
            stroke_width=4
        )

        # Streamer Credit Badge (Bottom / Center)
        draw.text(
            (out_w // 2, out_h - 120),
            f"⚡ STREAMER: {moment['channel_credit']} ⚡",
            font=font_badge,
            fill=(0, 229, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0),
            anchor="mm"
        )

        # Floating Subtitle / Reaction text at bottom (NO BOXES)
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

def process_streamer_moment(moment: dict, output_video_path: str) -> bool:
    """Orchestrates downloading real footage and vertical formatting. NO CARTOON FALLBACKS."""
    raw_slice = "temp_raw_slice.mp4"

    # Step 1: Download real video slice from YouTube
    downloaded = download_stream_slice(
        moment["youtube_url"],
        moment["start_time"],
        moment["end_time"],
        raw_slice
    )

    if downloaded and os.path.exists(raw_slice) and os.path.getsize(raw_slice) > 10000:
        format_split_screen_vertical(raw_slice, moment, output_video_path)
        return True

    print(f"[CLIP CUTTER] ⚠️ Failed to download stream moment '{moment['title']}' from YouTube.")
    return False

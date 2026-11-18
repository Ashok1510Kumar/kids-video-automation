#!/usr/bin/env python3
"""
GTA 6 AI AUTO-CLIPPER RUNNER
Powered by NaufalRizqullah/opensource-clipping:
- AI Transcriber: Faster-Whisper
- AI Content Curator: Google Gemini
- Smart Face-Tracking: MediaPipe BlazeFace (9:16 Vertical Re-framing)
- Viral Subtitles: Alex Hormozi style kinetic karaoke
- Automated YouTube Shorts Publishing with daily quota protection
"""

import os
import sys
import glob
import shutil
import subprocess
from datetime import datetime

from agents import PublishingAgent

CLIPPING_REPO_URL = "https://github.com/NaufalRizqullah/opensource-clipping.git"
CLIPPING_DIR = "opensource-clipping"

GTA6_SOURCES = [
    # iSHOWSPEED x GTA 6 | OFFICIAL TRAILER
    "https://www.youtube.com/watch?v=2BRL4ALMCyA",
    # Rockstar Games GTA 6 Official Trailer 1
    "https://www.youtube.com/watch?v=QdBZY2fkU-0"
]

def setup_clipper():
    """Clones and prepares opensource-clipping repository."""
    if not os.path.exists(CLIPPING_DIR):
        print(f"[GTA 6 CLIPPER] Cloning {CLIPPING_REPO_URL}...")
        subprocess.run(["git", "clone", "--depth", "1", CLIPPING_REPO_URL, CLIPPING_DIR], check=True)

    # Set up .env with Google Gemini API Key
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_FLOW_ID") or ""
    env_path = os.path.join(CLIPPING_DIR, ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"GOOGLE_API_KEY={gemini_key}\n")
    print(f"[GTA 6 CLIPPER] Configured .env with Gemini API key in {CLIPPING_DIR}")

    # Set up cookies.txt for yt-dlp authentication
    cookies_content = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if cookies_content:
        cookie_path = os.path.join(CLIPPING_DIR, "cookies.txt")
        with open(cookie_path, "w", encoding="utf-8") as f:
            f.write(cookies_content)
        # Also write to root directory
        with open("cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookies_content)
        print(f"[GTA 6 CLIPPER] Loaded authenticated YouTube cookies ({len(cookies_content)} bytes)")

def run_clipping(target_url: str, num_clips: int = 10) -> list:
    """Executes opensource-clipping main.py to generate vertical 9:16 viral shorts."""
    print(f"[GTA 6 CLIPPER] Running AI Auto-Clipper on: {target_url} (Generating {num_clips} clips)...")

    cmd = [
        sys.executable, "main.py",
        "--url", target_url,
        "--clips", str(num_clips),
        "--ratio", "9:16",
        "--whisper-model", "base",
        "--whisper-device", "cpu",
        "--cleanup-source"
    ]

    try:
        subprocess.run(cmd, cwd=CLIPPING_DIR, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[GTA 6 CLIPPER] Notice during main.py execution: {e}")

    # Gather generated clips from output directory
    output_dir = os.path.join(CLIPPING_DIR, "output")
    clips = []
    if os.path.exists(output_dir):
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".mp4"):
                    clips.append(os.path.join(root, file))

    print(f"[GTA 6 CLIPPER] Generated {len(clips)} AI-clipped video(s).")
    return clips

def main():
    print("=" * 70)
    print("🎬 GTA 6 OPEN-SOURCE AI CLIPPING & PUBLISHING ENGINE")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 70)

    # 1. Setup open-source clipping engine
    setup_clipper()

    # 2. Run clipping on Speed's famous GTA 6 stream
    target_url = GTA6_SOURCES[0]
    generated_clips = run_clipping(target_url, num_clips=10)

    # If no clips generated (e.g. cloud runner IP restriction), run our local clip cutter
    if not generated_clips:
        print("[GTA 6 CLIPPER] Utilizing local streamer clip cutter engine for 10 clips...")
        from streamer_manifest import STREAMER_MOMENTS
        from streamer_clip_cutter import process_streamer_moment

        for i, moment in enumerate(STREAMER_MOMENTS[:10], 1):
            out_clip = f"gta6_clip_{i:02d}.mp4"
            print(f"[GTA 6 CLIPPER] Producing Clip {i}/10: '{moment['title']}'...")
            process_streamer_moment(moment, out_clip)
            if os.path.exists(out_clip):
                generated_clips.append(out_clip)

    print(f"\n[GTA 6 CLIPPER] Ready to publish {len(generated_clips)} GTA 6 clips!")

    # 3. Publish to YouTube (handles upload limit cooldown gracefully)
    publisher = PublishingAgent()
    published_count = 0

    for i, clip_path in enumerate(generated_clips, 1):
        filename = os.path.basename(clip_path)
        print(f"\n[GTA 6 CLIPPER] Uploading Clip {i}/{len(generated_clips)}: {filename}...")
        meta = {
            "title": f"iSHOWSPEED x GTA 6 CRAZIEST MOMENTS #{i}! 🎮🔥 #Shorts",
            "youtube_title": f"iSHOWSPEED x GTA 6 CRAZIEST MOMENTS #{i}! 🎮🔥 #Shorts #Speed #GTA6",
            "beats": [
                {
                    "beat_name": "GTA 6 HIGHLIGHT",
                    "narration": f"IShowSpeed reacting to GTA 6! Best gaming clips and viral reactions. Credit: @IShowSpeed #{i}"
                }
            ],
            "tags": ["gta6", "ishowspeed", "speed", "gaming", "shorts", "viral", "rockstar"]
        }

        result = publisher.publish(clip_path, meta)
        if result.get("status") == "success":
            published_count += 1
            print(f"✅ Published Live: {result.get('video_url')}")
        elif result.get("status") == "limit_reached":
            print("⚠️ YouTube daily upload limit reached for today. Remaining clips are saved as artifacts!")
            break

    print("\n" + "=" * 70)
    print(f"🎉 Completed! Published: {published_count}/{len(generated_clips)} clips.")
    print("=" * 70)

if __name__ == "__main__":
    main()

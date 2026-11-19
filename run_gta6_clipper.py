#!/usr/bin/env python3
"""
GTA 6 & STREAMER AI AUTO-CLIPPER
Processes and uploads viral clips directly from IShowSpeed's official GTA 6 and world tour streams:
- Uses verified streams from @IShowSpeed
- High-impact 9:16 vertical reformatting (Facecam zoomed, gameplay action)
- Pure floating hook headlines and captions (zero boxes, zero cartoons)
- Automated YouTube Shorts Publishing with daily quota protection
"""

import os
import sys
import glob
from datetime import datetime

from streamer_manifest import STREAMER_MOMENTS, mark_moment_as_published
from streamer_clip_cutter import process_streamer_moment
from agents import PublishingAgent

def main():
    print("=" * 70)
    print("🎬 IShowSpeed GTA 6 & WORLD STREAMS AUTO-CLIPPER")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 70)

    generated_clips = []

    for i, moment in enumerate(STREAMER_MOMENTS, 1):
        out_clip = f"speed_clip_{i:02d}.mp4"
        print(f"\n[SPEED CLIPPER] Processing Moment {i}/{len(STREAMER_MOMENTS)}: '{moment['title']}'...")
        print(f"[SPEED CLIPPER] Stream URL: {moment['youtube_url']}")

        success = process_streamer_moment(moment, out_clip)
        if success and os.path.exists(out_clip) and os.path.getsize(out_clip) > 50000:
            print(f"✅ Generated real clip: {out_clip} ({os.path.getsize(out_clip)} bytes)")
            generated_clips.append((out_clip, moment))
        else:
            print(f"⚠️ Skipped moment {i} due to stream unavailability.")

    print(f"\n[SPEED CLIPPER] Successfully produced {len(generated_clips)} real video clip(s)!")

    if not generated_clips:
        print("❌ CRITICAL: No real clips could be cut from the streams.")
        sys.exit(1)

    # Publish clips
    publisher = PublishingAgent()
    published_count = 0

    for i, (clip_path, moment) in enumerate(generated_clips, 1):
        filename = os.path.basename(clip_path)
        print(f"\n[SPEED CLIPPER] Publishing Clip {i}/{len(generated_clips)}: {filename}...")
        meta = {
            "title": moment["title"][:100],
            "youtube_title": moment["title"][:100],
            "beats": [
                {
                    "beat_name": "STREAMER CLIP",
                    "narration": moment["description"]
                }
            ],
            "tags": moment.get("tags", ["ishowspeed", "gta6", "speed", "gaming", "shorts"])
        }

        result = publisher.publish(clip_path, meta)
        if result.get("status") == "success":
            published_count += 1
            mark_moment_as_published(moment["id"])
            print(f"✅ Published Live: {result.get('video_url')}")
        elif result.get("status") == "limit_reached":
            print("⚠️ YouTube daily upload limit reached for today. Remaining clips are preserved as GitHub Artifacts!")
            break

    print("\n" + "=" * 70)
    print(f"🎉 Complete! Published {published_count}/{len(generated_clips)} clips. All clips saved as artifacts.")
    print("=" * 70)

if __name__ == "__main__":
    main()

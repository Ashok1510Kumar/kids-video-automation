#!/usr/bin/env python3
"""
STREAMER CLIPS AUTOMATION PIPELINE
Processes and uploads daily viral clips from IShowSpeed:
1. Selects next viral streamer moment from manifest.
2. Slices stream segment and formats into 9:16 vertical Short (Real video of Speed).
3. Adds pure floating subtitles & hook captions (zero boxes, zero cartoons).
4. Publishes directly to YouTube Shorts with creator attribution credit.
"""

import os
import sys
from datetime import datetime

from streamer_manifest import STREAMER_MOMENTS, mark_moment_as_published, get_next_streamer_moment
from streamer_clip_cutter import process_streamer_moment
from agents import PublishingAgent

def main():
    print("=" * 65)
    print("🎬 STREAMER VIRAL CLIPS PIPELINE INITIATED")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)

    output_clip = "streamer_clip_output.mp4"
    success = False
    chosen_moment = None

    # Try un-published moments first, then try all moments until real video is rendered
    start_moment = get_next_streamer_moment()
    all_to_try = [start_moment] + [m for m in STREAMER_MOMENTS if m["id"] != start_moment["id"]]

    for moment in all_to_try:
        print(f"\n🎯 Attempting Creator: {moment['creator']}")
        print(f"📺 Moment Title: '{moment['title']}'")
        print(f"🔗 URL: {moment['youtube_url']}")
        print(f"⏱️ Stream Section: {moment['start_time']} -> {moment['end_time']}\n")

        if process_streamer_moment(moment, output_clip):
            success = True
            chosen_moment = moment
            break
        else:
            print(f"⚠️ Could not cut moment '{moment['id']}', attempting next moment in manifest...")

    if not success or not os.path.exists(output_clip):
        print("❌ CRITICAL: Failed to download real stream footage for any streamer moment.")
        sys.exit(1)

    print(f"\n✅ Successfully generated real streamer clip: {output_clip} ({os.path.getsize(output_clip)} bytes)")

    # 3. Publish to YouTube Shorts
    publisher = PublishingAgent()
    episode_meta = {
        "title": chosen_moment["title"],
        "youtube_title": chosen_moment["title"][:100],
        "beats": [
            {"beat_name": "STREAMER CLIP", "narration": chosen_moment["description"]}
        ],
        "tags": chosen_moment.get("tags", ["shorts", "streamer", "ishowspeed", "gaming"])
    }

    pub_result = publisher.publish(output_clip, episode_meta)
    print(f"🚀 Publishing Status: {pub_result.get('status')}")
    if pub_result.get("video_url"):
        print(f"🔗 YouTube Live URL: {pub_result.get('video_url')}")
        mark_moment_as_published(chosen_moment["id"])

    print("=" * 65)
    print("✅ STREAMER CLIP EPISODE COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
STREAMER CLIPS AUTOMATION PIPELINE
Processes and uploads daily viral clips from IShowSpeed and Indian creators:
1. Selects next viral streamer moment from manifest.
2. Slices stream segment and formats into 9:16 vertical Short (Facecam on top, gameplay on bottom).
3. Adds pure floating subtitles & hook captions (zero boxes).
4. Publishes directly to YouTube Shorts with creator attribution credit.
"""

import os
import sys
from datetime import datetime

from streamer_manifest import get_next_streamer_moment, mark_moment_as_published
from streamer_clip_cutter import process_streamer_moment
from agents import PublishingAgent

def main():
    print("=" * 65)
    print("🎬 STREAMER VIRAL CLIPS PIPELINE INITIATED")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)

    # 1. Select Next Moment
    moment = get_next_streamer_moment()
    print(f"🎯 Selected Creator: {moment['creator']}")
    print(f"📺 Moment Title: '{moment['title']}'")
    print(f"⏱️ Stream Section: {moment['start_time']} -> {moment['end_time']}\n")

    output_clip = "streamer_clip_output.mp4"

    # 2. Slice, Split-Screen Format, and Caption
    process_streamer_moment(moment, output_clip)

    # 3. Publish to YouTube Shorts
    publisher = PublishingAgent()
    episode_meta = {
        "title": moment["title"],
        "youtube_title": moment["title"][:100],
        "beats": [
            {"beat_name": "STREAMER CLIP", "narration": moment["description"]}
        ],
        "tags": moment.get("tags", ["shorts", "streamer", "gaming"])
    }

    pub_result = publisher.publish(output_clip, episode_meta)
    print(f"🚀 Publishing Status: {pub_result.get('status')}")
    if pub_result.get("video_url"):
        print(f"🔗 YouTube Live URL: {pub_result.get('video_url')}")
        mark_moment_as_published(moment["id"])

    print("=" * 65)
    print("✅ STREAMER CLIP EPISODE COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()

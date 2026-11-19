#!/usr/bin/env python3
"""
Direct Publisher for Speed GTA 6 Short
"""
import os
import sys
from agents import PublishingAgent

def main():
    video_path = "speed_gta6_live_short.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        sys.exit(1)

    print(f"🚀 Publishing {video_path} to YouTube Shorts...")
    publisher = PublishingAgent()
    meta = {
        "title": "iSHOWSPEED PLAYS GTA 6 EARLY ACCESS! 🎮🔥 #Shorts #IShowSpeed",
        "youtube_title": "iSHOWSPEED PLAYS GTA 6 EARLY ACCESS! 🎮🔥 #Shorts #IShowSpeed #GTA6",
        "beats": [
            {
                "beat_name": "IShowSpeed GTA 6 Stream",
                "narration": "IShowSpeed playing GTA 6 Early Access gameplay livestream! Pure viral energy. Original streamer: @IShowSpeed."
            }
        ],
        "tags": ["ishowspeed", "gta6", "speed", "gaming", "shorts", "viral", "rockstar"]
    }

    result = publisher.publish(video_path, meta)
    print(f"Status: {result.get('status')}")
    if result.get("video_url"):
        print(f"🎉 LIVE ON YOUTUBE: {result.get('video_url')}")
    elif result.get("status") == "limit_reached":
        print("⚠️ YouTube daily upload limit (24-hour channel security limit) is still cooling down.")
        print("The video file is safely saved in the repository and artifact for automatic release.")

if __name__ == "__main__":
    main()

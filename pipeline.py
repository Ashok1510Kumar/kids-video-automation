#!/usr/bin/env python3
"""
RICKS CLIPS MULTI-AGENT STUDIO PIPELINE
Orchestrates four specialized autonomous agents to write, produce, film, and publish
viral 45-second micro-documentary shorts modeled after @RicksClips3000:

1. AGENT 1: Screenwriter Agent (Google Flow / Gemini 2.0 Flash)
2. AGENT 2: Audio Engineer Agent (175 WPM Voiceover + Lo-Fi Groove + Foley SFX)
3. AGENT 3: Cinematographer Agent (30 FPS Character Staging + Zero-Box Floating Subtitles)
4. AGENT 4: Publishing Agent (YouTube Shorts Automated Upload)
"""

import sys
from datetime import datetime
from agents import (
    ScreenwriterAgent,
    AudioEngineerAgent,
    CinematographerAgent,
    PublishingAgent
)

def run_multi_agent_pipeline():
    print("=" * 65)
    print("🎬 RICK'S CLIPS MULTI-AGENT STUDIO INITIATED")
    print(f"⏰ Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. SCREENWRITER AGENT (Google Flow / Gemini 2.0 Flash)
    # -------------------------------------------------------------
    screenwriter = ScreenwriterAgent()
    episode = screenwriter.write_script()
    print(f"📄 Story Selected: '{episode.get('title')}'")
    print(f"🎯 Opening Hook: '{episode.get('hook_line')}'\n")

    voice_path = "ricks_narration.mp3"
    soundtrack_path = "ricks_soundtrack.wav"
    video_output_path = "ricks_clips_output.mp4"

    # -------------------------------------------------------------
    # 2. AUDIO ENGINEER AGENT (175 WPM Narration + Lo-Fi Groove + SFX)
    # -------------------------------------------------------------
    audio_engineer = AudioEngineerAgent()
    duration = audio_engineer.produce_soundtrack(episode, voice_path, soundtrack_path)
    print(f"🎵 Audio Mastered: {duration:.1f} seconds total runtime\n")

    # -------------------------------------------------------------
    # 3. CINEMATOGRAPHER AGENT (30 FPS, Pure Floating Subtitles - No Boxes)
    # -------------------------------------------------------------
    cinematographer = CinematographerAgent(fps=30)
    cinematographer.film_and_render(episode, soundtrack_path, video_output_path, duration)
    print(f"🎥 Video Filmed & Encoded: {video_output_path}\n")

    # -------------------------------------------------------------
    # 4. PUBLISHING AGENT (YouTube Data API v3 Automation)
    # -------------------------------------------------------------
    publisher = PublishingAgent()
    pub_result = publisher.publish(video_output_path, episode)
    print(f"🚀 Publishing Status: {pub_result.get('status')}")
    if pub_result.get("video_url"):
        print(f"🔗 YouTube Live URL: {pub_result.get('video_url')}")

    print("=" * 65)
    print("✅ RICK'S CLIPS MULTI-AGENT EPISODE COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    run_multi_agent_pipeline()

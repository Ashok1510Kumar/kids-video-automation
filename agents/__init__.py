#!/usr/bin/env python3
"""
MULTI-AGENT STUDIO ARCHITECTURE (@RicksClips3000 Style)
Four specialized autonomous agents collaborating to write, produce, film, and publish
daily high-retention micro-documentaries:
1. ScreenwriterAgent: Story creation via Google Flow (Gemini 2.0 Flash) & paradox structuring
2. AudioEngineerAgent: 175 WPM voiceover, lo-fi groove music, and beat-synced foley SFX
3. CinematographerAgent: 30 FPS character rigging, dynamic diagrams, and pure floating subtitles (no boxes)
4. PublishingAgent: Metadata optimization and automated YouTube Shorts publishing
"""

from agents.screenwriter_agent import ScreenwriterAgent
from agents.audio_engineer_agent import AudioEngineerAgent
from agents.cinematographer_agent import CinematographerAgent
from agents.publishing_agent import PublishingAgent

__all__ = [
    "ScreenwriterAgent",
    "AudioEngineerAgent",
    "CinematographerAgent",
    "PublishingAgent"
]

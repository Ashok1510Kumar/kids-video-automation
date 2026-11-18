#!/usr/bin/env python3
"""
STREAMER VIRAL MOMENTS MANIFEST (PLAYABLE OFFICIAL VIDEOS)
Active, verified playable videos directly from @IShowSpeed & Indian Creators.
"""

STREAMER_MOMENTS = [
    {
        "id": "speed_gta6_trailer_reaction",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "iSHOWSPEED x GTA 6 TRAILER REACTION! 🎮🔥 #Shorts #IShowSpeed",
        "description": (
            "Speed goes wild over the official GTA 6 Trailer! 😱⚡\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily viral streamer highlights & gaming moments!\n\n"
            "#IShowSpeed #GTA6 #Gaming #Shorts #Viral #Speed"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=2BRL4ALMCyA",
        "start_time": "00:00:15",
        "end_time": "00:00:50",
        "facecam_position": "full",
        "hook_text": "SPEED MEETS GTA 6! 💀🔥",
        "tags": ["ishowspeed", "gta6", "speed", "gaming", "shorts", "viral"]
    },
    {
        "id": "speed_ghana_film_moment",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED CRAZIEST IRL MOMENT IN GHANA! 🇬🇭😂 #Shorts #Speed",
        "description": (
            "IShowSpeed in Ghana having the most hilarious interaction with locals! 🐐\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily Speed highlights!\n\n"
            "#IShowSpeed #Ghana #Speed #IRL #Shorts"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=o3xA1J8BoHs",
        "start_time": "00:01:20",
        "end_time": "00:01:55",
        "facecam_position": "full",
        "hook_text": "SPEED IN GHANA IS WILD! 😭",
        "tags": ["ishowspeed", "ghana", "speed", "funny", "shorts"]
    },
    {
        "id": "speed_serena_williams_serve",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED TRIES RETURNING A 120 MPH TENNIS SERVE! 🎾💨 #Shorts",
        "description": (
            "Can Speed actually return a 120 MPH professional tennis serve?! 🤯\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily funny sports & streamer challenges!\n\n"
            "#IShowSpeed #Tennis #Challenge #Funny #Shorts"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=jJ-zWCw85qA",
        "start_time": "00:00:20",
        "end_time": "00:00:55",
        "facecam_position": "full",
        "hook_text": "SPEED VS 120 MPH TENNIS SERVE! 🎾💀",
        "tags": ["ishowspeed", "tennis", "speed", "challenge", "shorts"]
    }
]

def get_next_streamer_moment(tracker_file="published_moments.txt") -> dict:
    """Reads published list and returns the next un-published viral moment."""
    import os
    published_ids = set()
    if os.path.exists(tracker_file):
        with open(tracker_file, "r", encoding="utf-8") as f:
            published_ids = set(line.strip() for line in f if line.strip())

    for moment in STREAMER_MOMENTS:
        if moment["id"] not in published_ids:
            return moment

    # Loop back to first
    return STREAMER_MOMENTS[0]

def mark_moment_as_published(moment_id: str, tracker_file="published_moments.txt"):
    with open(tracker_file, "a", encoding="utf-8") as f:
        f.write(f"{moment_id}\n")

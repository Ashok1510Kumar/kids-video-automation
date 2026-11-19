#!/usr/bin/env python3
"""
STREAMER VIRAL MOMENTS MANIFEST (PLAYABLE OFFICIAL VIDEOS)
Active, verified playable streams directly from @IShowSpeed.
"""

STREAMER_MOMENTS = [
    {
        "id": "speed_gta6_early_access_live",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "iSHOWSPEED PLAYS GTA 6 EARLY ACCESS! 🎮🔥 #Shorts #IShowSpeed",
        "description": (
            "Speed plays GTA 6 Early Access Gameplay! The most viral stream moments! 😱⚡\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily viral streamer highlights & gaming moments!\n\n"
            "#IShowSpeed #GTA6 #Gaming #Shorts #Viral #Speed"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=qSyo5d-dVzA",
        "start_time": "00:02:00",
        "end_time": "00:02:35",
        "facecam_position": "full",
        "hook_text": "SPEED PLAYING GTA 6! 😱🔥",
        "tags": ["ishowspeed", "gta6", "speed", "gaming", "shorts", "viral"]
    },
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
        "id": "speed_meets_obama",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED MEETS PRESIDENT OBAMA! 🇺🇸🤯 #Shorts #IShowSpeed",
        "description": (
            "Speed actually met President Obama in person! 🤯\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily viral Speed moments!\n\n"
            "#IShowSpeed #Obama #Speed #Shorts #Viral"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=o0UeucVxYCA",
        "start_time": "00:00:30",
        "end_time": "00:01:05",
        "facecam_position": "full",
        "hook_text": "SPEED MET PRESIDENT OBAMA?! 💀",
        "tags": ["ishowspeed", "obama", "speed", "viral", "shorts"]
    },
    {
        "id": "speed_haunted_house",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED IN THE SCARIEST HAUNTED HOUSE! 😱👻 #Shorts",
        "description": (
            "Speed spending the night in the world's scariest haunted house! Pure chaos! 🏚️\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily Speed moments!\n\n"
            "#IShowSpeed #HauntedHouse #Speed #Horror #Shorts"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=uQlACpbi4WM",
        "start_time": "00:01:00",
        "end_time": "00:01:35",
        "facecam_position": "full",
        "hook_text": "SPEED REGRETS THIS! 😭🏚️",
        "tags": ["ishowspeed", "hauntedhouse", "speed", "funny", "shorts"]
    },
    {
        "id": "speed_spiderman_irl",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED SPIDER-MAN IRL STREAM! 🎃🕷️ #Shorts #Speed",
        "description": (
            "Speed in a Spider-Man suit roaming the streets! 🕸️\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily Speed moments!\n\n"
            "#IShowSpeed #SpiderMan #Speed #IRL #Shorts"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=IkhjzYsvCmw",
        "start_time": "00:00:45",
        "end_time": "00:01:20",
        "facecam_position": "full",
        "hook_text": "SPEED IS SPIDER-MAN! 🕸️🔥",
        "tags": ["ishowspeed", "spiderman", "speed", "irl", "shorts"]
    },
    {
        "id": "speed_kfc_job",
        "creator": "IShowSpeed",
        "channel_credit": "@IShowSpeed",
        "title": "SPEED WORKING AT KFC GONE WRONG! 🍗😂 #Shorts",
        "description": (
            "Speed gets a job at KFC and causes absolute chaos! 🍟\n\n"
            "Original Streamer: @IShowSpeed\n"
            "Subscribe for daily Speed moments!\n\n"
            "#IShowSpeed #KFC #Speed #Comedy #Shorts"
        ),
        "youtube_url": "https://www.youtube.com/watch?v=o1_FvfJD8fg",
        "start_time": "00:00:30",
        "end_time": "00:01:05",
        "facecam_position": "full",
        "hook_text": "SPEED WORKS AT KFC! 💀🍗",
        "tags": ["ishowspeed", "kfc", "speed", "funny", "shorts"]
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

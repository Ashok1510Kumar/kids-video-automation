#!/usr/bin/env python3
"""
CINEMATIC 3D ANIMATION RELEASES PUBLISHER
Uploads the high-retention 3D Pixar/Blender animated micro-documentaries
and widescreen long-form documentary directly to YouTube.
"""

import os
import sys
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

RELEASES = [
    {
        "id": "short1",
        "file": "japan_gambling_cinematic_short.mp4",
        "title": "The Secret Window That Breaks Japan's Law! 🇯🇵🤫 #Shorts #Curiosity #Mystery",
        "description": (
            "Gambling is 100% illegal in Japan... so how does a $200 BILLION gambling empire operate on every street corner? 🎰✨\n\n"
            "Discover the genius 'San-ten Hōshiki' legal loophole that allows Tokyo Pachinko parlors to operate in broad daylight.\n\n"
            "Would you have figured out the 3-shop trick or taken the cookies? Comment below! 👇\n\n"
            "🔔 Subscribe for mind-bending real-world paradoxes every single week!\n\n"
            "#Shorts #RicksClips #Japan #Mystery #LifeHacks #Law #Education #Curiosity"
        ),
        "category": "27", # Education
        "tags": ["japan gambling law", "pachinko loophole", "san ten hoshiki", "how pachinko works", "japan mystery", "ricks clips", "legal loopholes", "engineering paradox", "shorts", "curiosity"]
    },
    {
        "id": "short2",
        "file": "airplane_windows_cinematic_short.mp4",
        "title": "Why Airplane Windows Are NEVER Square! ✈️📐 #Shorts #Engineering #Science",
        "description": (
            "If you ever board a passenger jet with square windows... RUN! 😱✈️\n\n"
            "In 1954, the world's most advanced jetliner mysteriously broke apart in mid-air. The culprit? A simple 90-degree corner.\n\n"
            "Here is the physics of how curved windows save millions of lives every single day.\n\n"
            "🔔 Hit subscribe to unlock the hidden engineering behind everyday objects!\n\n"
            "#Shorts #Aviation #Engineering #AirplaneFacts #Physics #ScienceFacts #Mystery #RicksClips"
        ),
        "category": "28", # Science & Technology
        "tags": ["airplane square windows", "de havilland comet", "aviation mystery", "why airplane windows are round", "engineering disasters", "physics facts", "science shorts", "ricks clips"]
    },
    {
        "id": "longform",
        "file": "engineering_loopholes_cinematic_longform.mp4",
        "title": "3 Genius Engineering & Legal Loopholes That Broke The World! (Full Documentary)",
        "description": (
            "From a secret back-alley window in Tokyo that bypasses strict gambling bans, to the fatal 90-degree corners that tore apart the world's fastest passenger jet, discover 3 unbelievable engineering and legal loopholes that completely changed modern history! 🤯🛠️\n\n"
            "⏱️ Chapters:\n"
            "00:00 - The Paradoxes That Fooled the World\n"
            "00:18 - Chapter 1: The Tokyo Gambling Secret Window (Japan)\n"
            "00:46 - Chapter 2: The Deadly Train Sun Kink (Railroad Physics)\n"
            "01:15 - Chapter 3: The Fatal Square Airplane Window (Aviation)\n"
            "01:36 - Conclusion: Why Perfection Requires Flaws\n\n"
            "🔔 Subscribe for deep-dive animated engineering mysteries every week!\n\n"
            "#Engineering #Documentary #Science #Physics #History #Animation #Curiosity"
        ),
        "category": "28", # Science & Technology
        "tags": ["engineering loopholes", "san ten hoshiki", "sun kink", "railroad physics", "square airplane windows", "de havilland comet", "engineering documentary", "animation"]
    }
]

def get_youtube_service():
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing YouTube credentials in environment.")
        sys.exit(1)

    print("Authenticating with YouTube API via OAuth2...")
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, item: dict, privacy: str):
    file_path = item["file"]
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return None

    title = item["title"]
    description = item["description"]
    tags = item["tags"]
    category_id = item.get("category", "28")

    print(f"\n" + "=" * 60)
    print(f"UPLOADING: '{title}'")
    print(f"File: {file_path} ({os.path.getsize(file_path):,} bytes)")
    print(f"Category: {category_id} | Privacy: {privacy}")
    print("=" * 60)

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        response = request.execute()
        vid_id = response.get("id")
        video_url = f"https://youtu.be/{vid_id}"
        print(f"\n🎉 SUCCESS! VIDEO IS LIVE ON YOUTUBE:")
        print(f"🔗 {video_url}\n")
        return {"status": "success", "id": vid_id, "url": video_url}
    except Exception as e:
        err_str = str(e)
        if "uploadLimitExceeded" in err_str:
            print(f"⚠️ YouTube 24-hour daily upload limit reached for this channel.")
            return {"status": "limit_reached", "error": err_str}
        else:
            print(f"Upload error: {e}")
            raise e

def main():
    parser = argparse.ArgumentParser(description="YouTube Publisher for Cinematic Trio")
    parser.add_argument("--target", default="all", choices=["short1", "short2", "longform", "all"], help="Which video to upload")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"], help="Privacy status")
    args = parser.parse_args()

    privacy = os.environ.get("YT_PRIVACY", args.privacy)
    youtube = get_youtube_service()

    targets = RELEASES if args.target == "all" else [r for r in RELEASES if r["id"] == args.target]
    results = []

    for item in targets:
        res = upload_video(youtube, item, privacy)
        if res:
            results.append(res)
            if res.get("status") == "limit_reached":
                print("Stopping upload queue due to daily quota limit.")
                break

    print("\n" + "=" * 60)
    print("PUBLISHING RUN COMPLETE")
    for r in results:
        if r.get("url"):
            print(f"✓ LIVE: {r['url']}")
        else:
            print(f"✗ Status: {r.get('status')}")
    print("=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Multi-Creator YouTube Shorts Publisher (Kai Cenat, Techno Gamerz, CarryMinati)
"""
import os
import sys
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SHORTS_QUEUE = [
    {
        "creator": "Kai Cenat",
        "file": "kaicenat_gta6_short.mp4",
        "title": "KAI CENAT PLAYS GTA 6 FOR THE FIRST TIME! 🎮🔥 #Shorts #KaiCenat",
        "description": (
            "Kai Cenat plays GTA 6 for the first time! Pure comedy and hype stream reaction. 😱🎮\n\n"
            "Original Streamer: @KaiCenat (https://www.youtube.com/@KaiCenat)\n"
            "Subscribe for daily viral streamer highlights & GTA 6 clips!\n\n"
            "#KaiCenat #GTA6 #Shorts #Gaming #Viral #Rockstar"
        ),
        "tags": ["kaicenat", "gta6", "kai", "gaming", "shorts", "viral", "rockstar"]
    },
    {
        "creator": "Techno Gamerz",
        "file": "technogamerz_gta6_short.mp4",
        "title": "TECHNO GAMERZ FIRST DAY IN GTA 6 VICE CITY! 🎮🔥 #Shorts #TechnoGamerz",
        "description": (
            "Techno Gamerz (Ujjwal) exploring Vice City in GTA 6! India's #1 GTA streamer. 🚗💨\n\n"
            "Original Streamer: @TechnoGamerz (https://www.youtube.com/@TechnoGamerzOfficial)\n"
            "Subscribe for daily viral moments & GTA 6 gameplay!\n\n"
            "#TechnoGamerz #GTA6 #ViceCity #Shorts #Gaming #Viral #Ujjwal"
        ),
        "tags": ["technogamerz", "gta6", "vicecity", "gaming", "shorts", "viral", "ujjwal"]
    },
    {
        "creator": "CarryMinati",
        "file": "carryminati_gta6_short.mp4",
        "title": "CARRYMINATI CRAZIEST MOMENT ON STREAM! 😱🔥 #Shorts #CarryisLive",
        "description": (
            "CarryMinati (CarryisLive) hilarious gaming stream moment! 🎮🔥\n\n"
            "Original Streamer: @CarryisLive (https://www.youtube.com/@CarryisLive)\n"
            "Subscribe for daily viral moments & streamer highlights!\n\n"
            "#CarryMinati #CarryisLive #Shorts #Gaming #Viral #Carry"
        ),
        "tags": ["carryminati", "carryislive", "gaming", "shorts", "viral", "carry"]
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

def upload_short(youtube, item: dict, privacy: str):
    file_path = item["file"]
    title = item["title"]
    description = item["description"]
    tags = item["tags"]
    creator = item["creator"]

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist, skipping.")
        return None

    print(f"\n==========================================")
    print(f"Uploading {creator} Short: '{title}' ({privacy})...")
    print(f"==========================================")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags,
            "categoryId": "20",  # Gaming
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
        print(f"\n🎉 SUCCESS! {creator.upper()} SHORT IS LIVE ON YOUTUBE:")
        print(f"🔗 {video_url}\n")
        return {"creator": creator, "status": "success", "url": video_url}
    except Exception as e:
        err_str = str(e)
        if "uploadLimitExceeded" in err_str:
            print(f"⚠️ YouTube 24-hour daily upload limit reached for this channel (rolling security limit).")
            return {"creator": creator, "status": "limit_reached", "error": err_str}
        else:
            print(f"❌ Upload error for {creator}: {e}")
            return {"creator": creator, "status": "error", "error": err_str}

def main():
    privacy = os.environ.get("YT_PRIVACY", "public")
    youtube = get_youtube_service()

    results = []
    for item in SHORTS_QUEUE:
        res = upload_short(youtube, item, privacy)
        if res:
            results.append(res)
            if res.get("status") == "limit_reached":
                print("Stopping queue due to daily quota limit.")
                break
        time.sleep(5)

    print("\n==========================================")
    print("FINAL UPLOAD SUMMARY:")
    print("==========================================")
    for r in results:
        print(f"{r['creator']}: {r['status']} -> {r.get('url', r.get('error', ''))}")

if __name__ == "__main__":
    main()

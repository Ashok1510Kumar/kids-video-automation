#!/usr/bin/env python3
"""
Direct Publisher for Synced Hyped Speed Short
"""
import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_short(video_path: str, title: str, description: str, tags: list):
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    privacy = os.environ.get("YT_PRIVACY", "public")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing YouTube credentials in environment.")
        sys.exit(1)

    print("Connecting to YouTube API with OAuth2...")
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    youtube = build("youtube", "v3", credentials=creds)

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

    print(f"Uploading '{title}' ({privacy})...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        response = request.execute()
        vid_id = response.get("id")
        video_url = f"https://youtu.be/{vid_id}"
        print(f"\n🎉 SUCCESS! SYNCED HYPED SPEED SHORT IS LIVE ON YOUTUBE:")
        print(f"🔗 {video_url}\n")
        return {"status": "success", "video_url": video_url}
    except Exception as e:
        err_str = str(e)
        if "uploadLimitExceeded" in err_str:
            print(f"⚠️ YouTube 24-hour daily upload limit reached for this channel (rolling security limit).")
            return {"status": "limit_reached"}
        else:
            print(f"Upload error: {e}")
            raise e

def main():
    video_path = "speed_hyped_split_short_synced.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        sys.exit(1)

    title = "SPEED SURVIVES 52 HOURS IN GTA 6! 🎮🔥 #Shorts #IShowSpeed #GTA6"
    description = (
        "IShowSpeed finishes 52 hours of non-stop GTA 6 gameplay! Pure chaos and hype. 😱⚡\n\n"
        "Original Streamer: @IShowSpeed\n"
        "Subscribe for daily viral moments & GTA 6 clips!\n\n"
        "#IShowSpeed #GTA6 #Speed #Gaming #Shorts #Viral #Lucia"
    )
    tags = ["ishowspeed", "gta6", "speed", "gaming", "shorts", "viral", "rockstar", "lucia"]

    upload_short(video_path, title, description, tags)

if __name__ == "__main__":
    main()

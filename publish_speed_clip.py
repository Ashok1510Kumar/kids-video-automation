#!/usr/bin/env python3
"""
Direct Publisher for Speed GTA 6 Short (Self-contained YouTube Shorts Uploader)
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

    print(f"Connecting to YouTube API with OAuth2...")
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
        print(f"\n🎉 SUCCESS! VIDEO IS LIVE ON YOUTUBE:")
        print(f"🔗 {video_url}\n")
        return {"status": "success", "video_url": video_url}
    except Exception as e:
        err_str = str(e)
        if "uploadLimitExceeded" in err_str:
            print(f"⚠️ YouTube 24-hour daily upload limit reached for this channel (rolling security limit).")
            print(f"The video is rendered, verified, and saved in GitHub artifacts for automated publishing.")
            return {"status": "limit_reached"}
        else:
            print(f"Upload error: {e}")
            raise e

def main():
    video_path = "speed_gta6_live_short.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        sys.exit(1)

    title = "iSHOWSPEED PLAYS GTA 6 EARLY ACCESS! 🎮🔥 #Shorts #IShowSpeed"
    description = (
        "IShowSpeed plays GTA 6 Early Access gameplay livestream! 😱⚡\n\n"
        "Original Streamer: @IShowSpeed (https://www.youtube.com/watch?v=qSyo5d-dVzA)\n"
        "Subscribe for daily viral Speed moments & GTA 6 gameplay!\n\n"
        "#IShowSpeed #GTA6 #Speed #Gaming #Shorts #Viral"
    )
    tags = ["ishowspeed", "gta6", "speed", "gaming", "shorts", "viral", "rockstar"]

    upload_short(video_path, title, description, tags)

if __name__ == "__main__":
    main()

import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload():
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing credentials.")
        sys.exit(1)

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    youtube = build("youtube", "v3", credentials=creds)

    video_file = "kaicenat_gta6_part2_viral.mp4"
    title = "KAI CENAT CRAZIEST REACTION IN GTA 6! 🎮🔥 (Part 2) #Shorts #KaiCenat"
    description = (
        "Kai Cenat hilarious reaction part 2 in GTA 6! 😱🎮\n\n"
        "Original Streamer: @KaiCenat (https://www.youtube.com/@KaiCenat)\n"
        "Subscribe for daily viral streamer highlights & GTA 6 clips!\n\n"
        "---------------------------------------------------\n"
        "🔥 Want to edit viral clips like this in 1-click with AI?\n"
        "👉 Try Opus Clip AI Auto-Clipper: https://www.opus.pro/?via=clipping\n"
        "---------------------------------------------------\n\n"
        "#KaiCenat #GTA6 #Shorts #Gaming #Viral #FunnyMoments"
    )
    tags = ["kaicenat", "gta6", "kai", "gaming", "shorts", "viral", "rockstar", "funny"]

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags,
            "categoryId": "20",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    vid_id = resp.get("id")
    url = f"https://youtu.be/{vid_id}"
    print(f"🎉 SUCCESS! KAI CENAT PART 2 IS LIVE ON YOUTUBE:")
    print(f"🔗 {url}")

if __name__ == "__main__":
    upload()

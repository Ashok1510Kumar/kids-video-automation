#!/usr/bin/env python3
"""
AGENT 4: PUBLISHING AGENT (@RicksClips3000 Style)
Packages viral YouTube Shorts metadata and handles YouTube Data API v3 upload:
- High-CTR Title with emojis and #Shorts tags
- Search-optimized description containing story breakdown and channel tags
- COPPA compliance (selfDeclaredMadeForKids=False) and Education category (27)
- Automated resumable upload via OAuth2 refresh token
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class PublishingAgent:
    def __init__(self):
        self.client_id = os.environ.get("YT_CLIENT_ID")
        self.client_secret = os.environ.get("YT_CLIENT_SECRET")
        self.refresh_token = os.environ.get("YT_REFRESH_TOKEN")
        self.privacy = os.environ.get("YT_PRIVACY", "public")

    def publish(self, video_path: str, episode: dict) -> dict:
        """
        Publishes the rendered short to YouTube using OAuth 2.0.
        Returns dictionary with status and video link.
        """
        print("[AGENT 4: PUBLISHING AGENT] Preparing YouTube Shorts package...")

        if not all([self.client_id, self.client_secret, self.refresh_token]):
            print("[AGENT 4: PUBLISHING AGENT] Missing YouTube credentials. Running in DRY-RUN mode.")
            return {
                "status": "dry_run",
                "message": "Missing credentials. Video rendered locally but not uploaded to YouTube.",
                "title": episode.get("youtube_title"),
                "video_path": video_path
            }

        creds = Credentials(
            None,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        youtube = build("youtube", "v3", credentials=creds)

        title = episode.get("youtube_title", f"{episode.get('title')} #Shorts")
        description = (
            f"{episode.get('title')}! 🤯🔍\n\n"
            f"The Story Behind It:\n"
            + "\n\n".join([f"⚡ {beat['beat_name']}:\n{beat['narration']}" for beat in episode.get("beats", [])])
            + "\n\n🔔 Subscribe to Rick's Clips for daily engineering paradoxes, history mysteries, and science facts!\n\n"
            "#Shorts #Engineering #Science #History #Curiosity #RicksClips #FunFacts #Education"
        )

        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": episode.get("tags", ["engineering", "science", "curiosity", "shorts", "ricksclips"]),
                "categoryId": "27",  # Education
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            },
            "status": {
                "privacyStatus": self.privacy,
                "selfDeclaredMadeForKids": False,
            }
        }

        print(f"[AGENT 4: PUBLISHING AGENT] Uploading '{title[:60]}...' to YouTube ({self.privacy})...")
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()

        vid_id = response.get("id")
        video_url = f"https://youtu.be/{vid_id}"

        print(f"[AGENT 4: PUBLISHING AGENT] SUCCESS! Video is live at: {video_url}")
        return {
            "status": "success",
            "video_id": vid_id,
            "video_url": video_url,
            "title": title
        }

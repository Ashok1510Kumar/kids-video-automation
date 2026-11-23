import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_analytics():
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing YouTube credentials in environment.")
        sys.exit(1)

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    youtube = build("youtube", "v3", credentials=creds)

    # 1. Channel Statistics
    ch_resp = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    channel = ch_resp.get("items", [])[0] if ch_resp.get("items") else {}
    ch_title = channel.get("snippet", {}).get("title", "Unknown")
    stats = channel.get("statistics", {})
    print(f"=== CHANNEL: {ch_title} ===")
    print(f"Total Views: {stats.get('viewCount', '0')}")
    print(f"Subscribers: {stats.get('subscriberCount', '0')}")
    print(f"Total Videos: {stats.get('videoCount', '0')}")
    print(f"Hidden Subscriber Count: {stats.get('hiddenSubscriberCount', False)}")

    # 2. Uploads Playlist Videos & Individual Stats
    uploads_id = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if uploads_id:
        playlist_items = []
        next_page = None
        while True:
            pl_resp = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_id,
                maxResults=50,
                pageToken=next_page
            ).execute()
            playlist_items.extend(pl_resp.get("items", []))
            next_page = pl_resp.get("nextPageToken")
            if not next_page:
                break

        video_ids = [item["contentDetails"]["videoId"] for item in playlist_items]
        if video_ids:
            # Batch query video details & statistics
            v_resp = youtube.videos().list(
                part="snippet,statistics,status",
                id=",".join(video_ids)
            ).execute()

            print("\n=== LIVE VIDEO PERFORMANCE ===")
            print(f"{'ID':12} | {'Views':>7} | {'Likes':>5} | {'Privacy':8} | {'UploadStatus':12} | {'Reject/Failure'} | {'Title'}")
            print("-" * 110)
            total_fetched_views = 0
            for v in v_resp.get("items", []):
                v_id = v["id"]
                s = v.get("statistics", {})
                sn = v.get("snippet", {})
                st = v.get("status", {})
                views = int(s.get("viewCount", 0))
                likes = int(s.get("likeCount", 0))
                privacy = st.get("privacyStatus", "unknown")
                upload_status = st.get("uploadStatus", "unknown")
                reject = st.get("rejectionReason", "") or st.get("failureReason", "") or "None"
                title = sn.get("title", "")[:35]
                total_fetched_views += views
                print(f"{v_id:12} | {views:7d} | {likes:5d} | {privacy:8} | {upload_status:12} | {reject:14} | {title}")

            print("-" * 110)
            print(f"Aggregated Views across all {len(video_ids)} videos: {total_fetched_views:,}")

if __name__ == "__main__":
    get_analytics()

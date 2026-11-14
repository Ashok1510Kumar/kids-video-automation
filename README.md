# 🎬 Daily Kids Video Generator & YouTube Uploader (GitHub Actions)

An automated end-to-end Python pipeline running completely free on **GitHub Actions** that generates and uploads daily educational YouTube Shorts for kids.

---

## 🌟 Features
- **Zero Cost Execution**: Runs via GitHub Actions cron schedule.
- **Child-Friendly Narration**: Generates warm, engaging voiceovers using `edge-tts` (`en-US-AnaNeural`).
- **Dynamic 9:16 Visuals**: Creates high-contrast, colorful vertical video frames sized for YouTube Shorts (`1080x1920`).
- **COPPA Compliant**: Automatically flags uploads with `"selfDeclaredMadeForKids": True`.
- **Headless OAuth**: Uploads automatically using Google OAuth refresh tokens.

---

## 📂 Project Structure

```text
├── .github/
│   └── workflows/
│       └── daily_kids_video.yml   # Scheduled GitHub Actions cron job
├── pipeline.py                    # Main pipeline (TTS, rendering, upload)
├── get_token_from_code.py         # One-time helper to obtain refresh token
├── requirements.txt               # Dependencies
└── .gitignore
```

---

## 🚀 Setup Instructions

### 1. Configure GitHub Secrets
Navigate to **Settings** > **Secrets and variables** > **Actions** in your GitHub repository, and add the following 3 secrets:

| Secret Name | Description |
|-------------|-------------|
| `YT_CLIENT_ID` | Your Google OAuth Client ID |
| `YT_CLIENT_SECRET` | Your Google OAuth Client Secret |
| `YT_REFRESH_TOKEN` | Your Google OAuth Refresh Token |

### 2. Run or Schedule
The workflow will automatically run every day at **10:00 AM UTC**.  
You can also run it manually at any time by going to the **Actions** tab in GitHub and clicking **Run workflow**.

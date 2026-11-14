#!/usr/bin/env python3
"""
Automated Kids Video Generator & YouTube Uploader
Generates daily fun, educational short-form videos for kids and uploads them to YouTube.
"""

import os
import sys
import random
import asyncio
from datetime import datetime
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    ColorClip
)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# 1. TOPIC BANK (FUN EDUCATIONAL FACTS FOR KIDS)
# ==========================================
KIDS_TOPICS = [
    {
        "title": "🐬 Why Are Dolphins So Smart?",
        "topic": "Dolphins",
        "fact": (
            "Did you know dolphins are some of the smartest animals on Earth? "
            "They actually talk to each other using whistles and clicks! "
            "Each dolphin even has its own special name whistle! "
            "And get this: when they sleep, they keep one eye open to watch for sharks! "
            "How cool is that? See you tomorrow for more animal adventures!"
        ),
        "bg_color": (52, 152, 219),      # Friendly Sky/Ocean Blue
        "accent_color": (241, 196, 15),  # Sunshine Yellow
        "icon": "🐬"
    },
    {
        "title": "🦖 T-Rex Secrets You Didn't Know!",
        "topic": "Dinosaurs",
        "fact": (
            "Roar! Let's travel back in time to meet the mighty T-Rex! "
            "Did you know a T-Rex tooth could be as long as a banana? That's huge! "
            "Even though their arms were tiny, they had super sharp eyesight and an amazing sense of smell! "
            "Could you outrun a T-Rex? Scientists say kids on bicycles might be faster! "
            "Keep exploring, dino buddies!"
        ),
        "bg_color": (39, 174, 96),       # Jungle Green
        "accent_color": (230, 126, 34),  # Dinosaur Orange
        "icon": "🦖"
    },
    {
        "title": "🚀 Super Cool Facts About the Moon!",
        "topic": "Space",
        "fact": (
            "Blast off into space! Did you know the Moon has zero wind and zero rain? "
            "That means astronaut footprints on the moon will stay there for millions of years! "
            "Also, if you jumped on the Moon, you could jump six times higher than on Earth! "
            "You would look like a bouncing superhero! "
            "Reach for the stars, space explorers!"
        ),
        "bg_color": (44, 62, 80),        # Deep Space Navy
        "accent_color": (243, 156, 18),  # Glowing Star Gold
        "icon": "🌙"
    },
    {
        "title": "🐘 How Amazing Are Elephants?",
        "topic": "Elephants",
        "fact": (
            "Elephants are the gentle giants of the world! "
            "An elephant's trunk has over forty thousand muscles! "
            "They use it to drink water, pick up tiny peanuts, and even give each other friendly hugs! "
            "Elephants also love swimming and use their trunk like a natural snorkel! "
            "Give yourself a giant hug and follow for more fun facts!"
        ),
        "bg_color": (142, 68, 173),      # Playful Purple
        "accent_color": (46, 204, 113),  # Mint Green
        "icon": "🐘"
    },
    {
        "title": "🐝 Why Bees Are Earth's Superheroes!",
        "topic": "Honeybees",
        "fact": (
            "Buzz buzz! Meet nature's hardest little workers: honeybees! "
            "Did you know bees do a special waggle dance to tell their friends where flowers are? "
            "Without bees helping plants grow, we wouldn't have delicious apples, berries, or chocolate! "
            "A single honeybee visits thousands of flowers every day! "
            "Thank you, little bees!"
        ),
        "bg_color": (243, 156, 18),      # Honey Yellow
        "accent_color": (41, 128, 185),  # Bright Blue
        "icon": "🐝"
    },
    {
        "title": "🐙 The Octopus Has Three Hearts!",
        "topic": "Sea Creatures",
        "fact": (
            "Dive deep under the sea with the eight-legged octopus! "
            "Did you know an octopus has three hearts and blue blood? "
            "They can change their color and skin texture in less than a second to blend into coral! "
            "And since they don't have bones, they can squeeze through tiny holes the size of a coin! "
            "Nature is truly magical!"
        ),
        "bg_color": (22, 160, 133),      # Turquoise Ocean
        "accent_color": (231, 76, 60),   # Coral Red
        "icon": "🐙"
    }
]

# High quality child-friendly neural voice
TTS_VOICE = "en-US-AnaNeural"

# ==========================================
# 2. AUDIO GENERATION (Edge-TTS)
# ==========================================
async def generate_speech(text: str, output_path: str):
    """Generates friendly, clear voiceover for kids."""
    print(f"Generating voiceover with voice: {TTS_VOICE}")
    # Slightly energetic speed and clear pitch
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate="+4%", pitch="+2Hz")
    await communicate.save(output_path)
    print(f"Voiceover saved to {output_path}")

# ==========================================
# 3. VIDEO FRAME & VISUAL GENERATION
# ==========================================
def create_kids_frame(topic_data: dict, width=1080, height=1920) -> Image.Image:
    """Creates a colorful, high-contrast, child-friendly 9:16 vertical slide."""
    img = Image.new("RGB", (width, height), color=topic_data["bg_color"])
    draw = ImageDraw.Draw(img)

    # Decorative playful top banner
    accent = topic_data["accent_color"]
    draw.rectangle([(0, 0), (width, 220)], fill=accent)

    # Try loading default system fonts or fallback
    try:
        font_header = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        font_topic = ImageFont.truetype("DejaVuSans-Bold.ttf", 54)
        font_body = ImageFont.truetype("DejaVuSans.ttf", 46)
        font_footer = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
    except IOError:
        try:
            font_header = ImageFont.truetype("arialbd.ttf", 64)
            font_topic = ImageFont.truetype("arialbd.ttf", 54)
            font_body = ImageFont.truetype("arial.ttf", 46)
            font_footer = ImageFont.truetype("arialbd.ttf", 42)
        except IOError:
            font_header = font_topic = font_body = font_footer = ImageFont.load_default()

    # Banner Title
    header_text = "✨ FUN FACTS FOR KIDS ✨"
    draw.text((width // 2, 110), header_text, fill=(20, 20, 20), font=font_header, anchor="mm")

    # Topic Card (Rounded container)
    card_x0, card_y0 = 60, 280
    card_x1, card_y1 = width - 60, 520
    draw.rounded_rectangle([(card_x0, card_y0), (card_x1, card_y1)], radius=35, fill=(255, 255, 255))
    draw.rounded_rectangle([(card_x0, card_y0), (card_x1, card_y1)], radius=35, outline=accent, width=8)

    title_text = f"{topic_data['icon']} {topic_data['topic']} {topic_data['icon']}"
    draw.text((width // 2, (card_y0 + card_y1) // 2), title_text, fill=(30, 30, 30), font=font_topic, anchor="mm")

    # Fact Content Card
    body_x0, body_y0 = 60, 570
    body_x1, body_y1 = width - 60, height - 320
    draw.rounded_rectangle([(body_x0, body_y0), (body_x1, body_y1)], radius=35, fill=(255, 255, 255))
    draw.rounded_rectangle([(body_x0, body_y0), (body_x1, body_y1)], radius=35, outline=accent, width=8)

    # Word wrap the script text
    words = topic_data["fact"].split()
    lines = []
    current_line = []
    max_chars_per_line = 28

    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) >= max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = []
    if current_line:
        lines.append(" ".join(current_line))

    # Draw lines with comfortable spacing
    line_y = body_y0 + 70
    for line in lines:
        draw.text((width // 2, line_y), line, fill=(35, 35, 35), font=font_body, anchor="mm")
        line_y += 68

    # Bottom Call to Action Card
    cta_x0, cta_y0 = 60, height - 260
    cta_x1, cta_y1 = width - 60, height - 80
    draw.rounded_rectangle([(cta_x0, cta_y0), (cta_x1, cta_y1)], radius=30, fill=accent)
    draw.text(
        (width // 2, (cta_y0 + cta_y1) // 2),
        "⭐ Like & Subscribe for Daily Fun! ⭐",
        fill=(20, 20, 20),
        font=font_footer,
        anchor="mm"
    )

    return img

def build_video(topic_data: dict, audio_path: str, output_path: str):
    """Combines PIL frame and narration into MP4 format."""
    print("Compositing video...")
    audio = AudioFileClip(audio_path)
    duration = audio.duration + 0.5  # Slight trailing buffer

    # Create background frame
    pil_frame = create_kids_frame(topic_data)
    frame_np = np.array(pil_frame)

    # Convert to MoviePy ImageClip
    video_clip = ImageClip(frame_np).set_duration(duration)
    final_video = video_clip.set_audio(audio)

    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        logger=None
    )
    print(f"Video successfully rendered: {output_path} (Duration: {duration:.1f}s)")

# ==========================================
# 4. YOUTUBE UPLOADER (COPPA COMPLIANT)
# ==========================================
def upload_to_youtube(video_path: str, topic_data: dict) -> str:
    """Uploads video to YouTube with selfDeclaredMadeForKids=True."""
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    privacy = os.environ.get("YT_PRIVACY", "public")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError(
            "Missing YouTube credentials! Ensure YT_CLIENT_ID, YT_CLIENT_SECRET, "
            "and YT_REFRESH_TOKEN environment variables are set."
        )

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    youtube = build("youtube", "v3", credentials=creds)

    title = f"{topic_data['title']} | Fun Kids Facts #Shorts"
    description = (
        f"{topic_data['fact']}\n\n"
        "🔔 Subscribe to our channel for new fun educational videos every day!\n\n"
        "#Shorts #Kids #FunFacts #Learning #Education #Animals #Science"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": [
                "kids", "fun facts", "learning for kids", "education",
                "preschool", "children", topic_data["topic"].lower(), "shorts"
            ],
            "categoryId": "27",  # 27 = Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            # CRITICAL COPPA REQUIREMENT FOR KIDS VIDEOS
            "selfDeclaredMadeForKids": True,
        }
    }

    print(f"Uploading '{title}' to YouTube (Privacy: {privacy})...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"SUCCESS! Uploaded video to YouTube: {video_url}")
    return video_id

# ==========================================
# 5. MAIN FLOW
# ==========================================
def main():
    print(f"=== Starting Kids Video Automation ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
    
    # Pick a topic (random or day-based)
    topic_data = random.choice(KIDS_TOPICS)
    print(f"Selected Topic: {topic_data['title']}")

    audio_file = "narration.mp3"
    video_file = "kids_video_output.mp4"

    # 1. Audio
    asyncio.run(generate_speech(topic_data["fact"], audio_file))

    # 2. Video
    build_video(topic_data, audio_file, video_file)

    # 3. Upload
    upload_to_youtube(video_file, topic_data)

    print("=== Automation Completed Successfully ===")

if __name__ == "__main__":
    main()

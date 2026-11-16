#!/usr/bin/env python3
"""
LALAFUN EPISODIC STORYLINE ENGINE
Orchestrates 3-Act narrative story episodes with characters, dialogue, dramatic tension,
wobbling mystery props, magical reveals, and celebratory resolutions.
"""

import os
import sys
import math
import random
import asyncio
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Audio & Video tools
import edge_tts
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoClip
)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Studio Modules
from story_catalog import EPISODES
from animator import StudioAnimator
from music_generator import generate_nursery_music
from sfx_generator import generate_all_sfx
from story_props import (
    create_golden_egg,
    create_cracking_egg,
    create_baby_dragon_reveal,
    create_magic_cake
)
from cartoon_assets import (
    create_musical_note,
    create_sparkle_star
)

VOICE_NAME = "en-US-AnaNeural"

# ==========================================
# 1. STORY SOUNDTRACK & NARRATIVE SFX MIXER
# ==========================================
async def generate_story_voiceover(episode: dict, output_path: str):
    """Generates continuous warm narrative story voiceover."""
    full_text = " ".join([act["narration"] for act in episode["acts"]])
    print(f"Synthesizing story narrative with {VOICE_NAME}...")
    communicate = edge_tts.Communicate(full_text, VOICE_NAME, rate="+4%", pitch="+2Hz")
    await communicate.save(output_path)

def build_story_soundtrack(episode: dict, voice_path: str, output_soundtrack_path: str) -> float:
    """
    Mixes voiceover, story music box, and narrative sound effect cues.
    """
    generate_all_sfx()
    voice_clip = AudioFileClip(voice_path)
    intro_dur = 2.5
    outro_dur = 3.5
    total_duration = intro_dur + voice_clip.duration + outro_dur

    # Music Box Track (pleasant story melody)
    music_temp = "music_temp.wav"
    generate_nursery_music("twinkle", total_duration, music_temp, bpm=108)
    music_clip = AudioFileClip(music_temp).volumex(0.24)
    voice_clip = voice_clip.volumex(1.0).set_start(intro_dur)

    # Narrative Sound Cues timed to story beats
    sfx_clips = [music_clip, voice_clip]

    # Intro Sparkle
    sfx_clips.append(AudioFileClip("sfx_sparkle.wav").volumex(0.35).set_start(0.2))

    # Act 2 Transition (Suspense & Wobble Boing)
    act1_end = intro_dur + 14.0
    sfx_clips.append(AudioFileClip("sfx_whoosh.wav").volumex(0.30).set_start(act1_end - 0.2))
    sfx_clips.append(AudioFileClip("sfx_boing.wav").volumex(0.35).set_start(act1_end + 1.5))
    sfx_clips.append(AudioFileClip("sfx_boing.wav").volumex(0.35).set_start(act1_end + 3.0))

    # Act 3 Reveal (Pop & Celebratory Fanfare)
    act2_end = act1_end + 15.0
    sfx_clips.append(AudioFileClip("sfx_pop.wav").volumex(0.40).set_start(act2_end))
    sfx_clips.append(AudioFileClip("sfx_fanfare.wav").volumex(0.35).set_start(act2_end + 0.3))
    sfx_clips.append(AudioFileClip("sfx_sparkle.wav").volumex(0.35).set_start(act2_end + 3.5))

    # Outro Sparkle
    sfx_clips.append(AudioFileClip("sfx_sparkle.wav").volumex(0.35).set_start(total_duration - outro_dur + 0.3))

    composite_audio = CompositeAudioClip(sfx_clips).set_duration(total_duration)
    composite_audio.write_audiofile(output_soundtrack_path, fps=44100, logger=None)
    print(f"Mastered Story Soundtrack ready: {output_soundtrack_path} ({total_duration:.1f}s)")
    return total_duration

# ==========================================
# 2. MULTI-ACT CINEMATIC STORY COMPOSITOR
# ==========================================
class StorylineDirector:
    def __init__(self, episode: dict, total_duration: float, width=720, height=1280):
        self.episode = episode
        self.total_duration = total_duration
        self.intro_dur = 2.5
        self.outro_dur = 3.5
        self.width = width
        self.height = height

        # Load 3D background
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "assets", "backgrounds", "cocomelon_meadow.png")
        if os.path.exists(bg_path):
            self.bg_base = Image.open(bg_path).convert("RGBA")
            if self.bg_base.size != (width, height):
                self.bg_base = self.bg_base.resize((width, height), Image.LANCZOS)
        else:
            self.bg_base = Image.new("RGBA", (width, height), (135, 206, 235, 255))

        # Character Rig
        self.animator = StudioAnimator("LEO_THE_BEAR", bpm=108, target_height=520)

        # Pre-render Story Props
        print("Pre-rendering episodic story props...")
        self.prop_egg = create_golden_egg(size=260)
        self.prop_cracking = create_cracking_egg(size=275)
        self.prop_dragon = create_baby_dragon_reveal(size=320)
        self.prop_cake = create_magic_cake(size=300)

        # Ambient Effects
        self.note_pink = create_musical_note(size=75, color=(255, 64, 129))
        self.star_sprite = create_sparkle_star(size=80)

        # Fonts
        try:
            self.font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
            self.font_act = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
            self.font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
            self.font_cta = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
        except IOError:
            try:
                self.font_title = ImageFont.truetype("arialbd.ttf", 36)
                self.font_act = ImageFont.truetype("arialbd.ttf", 26)
                self.font_sub = ImageFont.truetype("arialbd.ttf", 30)
                self.font_cta = ImageFont.truetype("arialbd.ttf", 24)
            except IOError:
                self.font_title = self.font_act = self.font_sub = self.font_cta = ImageFont.load_default()

    def render_frame(self, t: float) -> np.ndarray:
        # Determine Current Story Act
        story_t = t - self.intro_dur
        is_intro = (t < self.intro_dur)
        is_outro = (t >= self.total_duration - self.outro_dur)

        if is_intro:
            act_idx = 0
            act_name = "STORYTIME ADVENTURE"
            camera_zoom = 1.00
        elif is_outro:
            act_idx = 2
            act_name = "HAPPY ENDING"
            camera_zoom = 1.03
        else:
            if story_t < 14.0:
                act_idx = 0
                act_name = "ACT 1: THE DISCOVERY"
                camera_zoom = 1.00 + 0.02 * (story_t / 14.0)
            elif story_t < 29.0:
                act_idx = 1
                act_name = "ACT 2: WHAT'S INSIDE?!"
                # Closer dramatic suspense camera zoom!
                camera_zoom = 1.05 + 0.03 * ((story_t - 14.0) / 15.0)
            else:
                act_idx = 2
                act_name = "ACT 3: A NEW BEST FRIEND!"
                camera_zoom = 1.04

        # 1. Dynamic Camera Zoom
        zw = int(self.width * camera_zoom)
        zh = int(self.height * camera_zoom)
        zoomed_bg = self.bg_base.resize((zw, zh), Image.BILINEAR)
        cx = (zw - self.width) // 2
        cy = (zh - self.height) // 2
        frame = zoomed_bg.crop((cx, cy, cx + self.width, cy + self.height)).copy()
        draw = ImageDraw.Draw(frame)

        # ----------------------------------------------------
        # SCENE A: INTRO TITLE CARD (0.0s to 2.5s)
        # ----------------------------------------------------
        if is_intro:
            card_w, card_h = 650, 230
            ix0 = (self.width - card_w) // 2
            iy0 = 210
            draw.rounded_rectangle([ix0 + 4, iy0 + 6, ix0 + card_w + 4, iy0 + card_h + 6], radius=30, fill=(0, 0, 0, 50))
            draw.rounded_rectangle([ix0, iy0, ix0 + card_w, iy0 + card_h], radius=30, fill=(255, 238, 88), outline=(255, 143, 0), width=6)
            draw.text((self.width // 2, iy0 + 60), "📖 LALAFUN STORYTIME 📖", fill=(40, 40, 40), font=self.font_title, anchor="mm")
            draw.text((self.width // 2, iy0 + 140), self.episode["title"], fill=(216, 27, 96), font=self.font_sub, anchor="mm")

            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=False)
            frame.alpha_composite(char_sprite, ((self.width - char_sprite.width) // 2, int(580 + hop)))

        # ----------------------------------------------------
        # SCENE C: OUTRO CELEBRATION (Last 3.5s)
        # ----------------------------------------------------
        elif is_outro:
            card_w, card_h = 660, 680
            ox0 = (self.width - card_w) // 2
            oy0 = 180
            draw.rounded_rectangle([ox0, oy0, ox0 + card_w, oy0 + card_h], radius=35, fill=(255, 255, 255), outline=(255, 64, 129), width=7)
            draw.text((self.width // 2, oy0 + 60), "🎉 THE END! 🎉", fill=(216, 27, 96), font=self.font_title, anchor="mm")
            draw.text((self.width // 2, oy0 + 115), "Subscribe for Leo's next adventure!", fill=(70, 70, 70), font=self.font_sub, anchor="mm")

            # YouTube End Screen Placeholders
            draw.ellipse([self.width // 2 - 80, oy0 + 165, self.width // 2 + 80, oy0 + 325], fill=(255, 240, 245), outline=(255, 64, 129), width=5)
            draw.text((self.width // 2, oy0 + 245), "SUBSCRIBE", fill=(216, 27, 96), font=self.font_sub, anchor="mm")

            draw.rounded_rectangle([ox0 + 60, oy0 + 360, ox0 + card_w - 60, oy0 + 570], radius=20, fill=(240, 248, 255), outline=(33, 150, 243), width=5)
            draw.text((self.width // 2, oy0 + 465), "▶ NEXT STORY EPISODE", fill=(25, 118, 210), font=self.font_sub, anchor="mm")

            # Dancing Leo + Friend at bottom
            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=False)
            thumb = char_sprite.resize((230, 230), Image.BILINEAR)
            frame.alpha_composite(thumb, ((self.width - 230) // 2, self.height - 290))

        # ----------------------------------------------------
        # SCENE B: STORYLINE IN ACTION (Acts 1, 2, and 3)
        # ----------------------------------------------------
        else:
            # 1. Top Story Header & Act Badge
            top_w, top_h = 620, 68
            bx0 = (self.width - top_w) // 2
            by0 = 35
            draw.rounded_rectangle([bx0 + 3, by0 + 5, bx0 + top_w + 3, by0 + top_h + 5], radius=22, fill=(0, 0, 0, 45))
            draw.rounded_rectangle([bx0, by0, bx0 + top_w, by0 + top_h], radius=22, fill=(255, 238, 88), outline=(255, 143, 0), width=5)
            draw.text((self.width // 2, by0 + top_h // 2), f"✨ {act_name} ✨", fill=(40, 40, 40), font=self.font_act, anchor="mm")

            # 2. Prop & Character Positioning by Story Act
            char_sprite, hop = self.animator.get_frame_pose(t, is_singing=(act_idx == 2))

            if act_idx == 0:
                # Act 1: The Discovery
                # Leo is on the left, looking curiously at the golden egg on the right
                char_x = int(self.width * 0.10)
                char_y = int(540 + hop)
                frame.alpha_composite(char_sprite, (char_x, char_y))

                # Shiny Golden Egg in the meadow
                egg_pulse = 1.0 + 0.04 * math.sin(t * 3.5)
                ew, eh = int(self.prop_egg.width * egg_pulse), int(self.prop_egg.height * egg_pulse)
                egg_scaled = self.prop_egg.resize((ew, eh), Image.BILINEAR)
                frame.alpha_composite(egg_scaled, (int(self.width * 0.52), 620))

            elif act_idx == 1:
                # Act 2: The Wobbling Mystery
                # Leo is leaning back in suspense
                char_x = int(self.width * 0.06)
                char_y = int(550 + hop)
                frame.alpha_composite(char_sprite, (char_x, char_y))

                # Egg shakes and wobbles aggressively!
                wobble_angle = 12.0 * math.sin(t * 16.0)
                wobble_egg = self.prop_cracking.rotate(wobble_angle, resample=Image.BICUBIC)
                frame.alpha_composite(wobble_egg, (int(self.width * 0.48), 610))

                # Floating question marks / exclamation marks
                draw.text((char_x + 220, char_y + 40), "❓", font=self.font_title)
                draw.text((int(self.width * 0.65), 540), "💥", font=self.font_title)

            else:
                # Act 3: The Magical Reveal & Celebration!
                # Leo and Baby Dragon dancing side-by-side
                char_x = int(self.width * 0.08)
                char_y = int(520 + hop)
                frame.alpha_composite(char_sprite, (char_x, char_y))

                # Baby Dragon bouncing joyfully
                dragon_hop = -abs(28.0 * math.sin(t * 6.0))
                dragon_x = int(self.width * 0.50)
                dragon_y = int(540 + dragon_hop)
                frame.alpha_composite(self.prop_dragon, (dragon_x, dragon_y))

                # Magical sparkles & stars flying everywhere
                for idx, (sx, sy_base, spd) in enumerate([(180, 480, 45), (420, 430, 60), (580, 510, 50)]):
                    star_y = int(sy_base - ((t * spd) % 250))
                    star_x = int(sx + 15 * math.sin(t * 4.0 + idx))
                    frame.alpha_composite(self.star_sprite, (star_x, star_y))

            # 3. Floating Story Musical Notes
            for nx, ny_base, spd, phase in [(80, 720, 55, 0.0), (620, 680, 70, 2.0)]:
                cur_y = int(ny_base - ((t * spd) % 450))
                cur_x = int(nx + 18 * math.sin(t * 3.0 + phase))
                frame.alpha_composite(self.note_pink, (cur_x, cur_y))

            # 4. Narrative Story Captions (Bottom Subtitle Pill)
            # Find the active narration sentence
            cur_act = self.episode["acts"][act_idx]
            sentences = [s.strip() for s in cur_act["narration"].split(".") if len(s.strip()) > 3]
            s_idx = min(len(sentences) - 1, int((story_t % 14.5) / 4.8))
            current_caption = sentences[s_idx]

            card_w, card_h = 670, 185
            cx0 = (self.width - card_w) // 2
            cy0 = self.height - 235

            draw.rounded_rectangle([cx0 + 4, cy0 + 6, cx0 + card_w + 4, cy0 + card_h + 6], radius=28, fill=(0, 0, 0, 50))
            draw.rounded_rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], radius=28, fill=(255, 255, 255), outline=(255, 64, 129), width=6)

            # Speaker / Narrative indicator
            draw.rounded_rectangle([cx0 + 25, cy0 + 15, cx0 + 220, cy0 + 55], radius=12, fill=(255, 238, 88))
            draw.text((cx0 + 122, cy0 + 35), "🐻 LEO'S STORY", fill=(50, 50, 50), font=self.font_act, anchor="mm")

            # Word wrap caption line
            draw.text((self.width // 2, cy0 + 115), current_caption, fill=(216, 27, 96), font=self.font_sub, anchor="mm")

        # Convert RGBA to RGB for MoviePy
        rgb_out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_out.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_out)

def render_story_video(episode: dict, audio_path: str, output_path: str, duration: float):
    """Composites the complete episodic animated story."""
    print("Beginning Episodic Storyline composition...")
    director = StorylineDirector(episode, duration, width=720, height=1280)

    audio_clip = AudioFileClip(audio_path)
    video = VideoClip(lambda t: director.render_frame(t), duration=duration).set_audio(audio_clip)

    video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None
    )
    print(f"Episodic Story Video rendered successfully: {output_path} ({duration:.1f}s)")

# ==========================================
# 3. YOUTUBE UPLOADER (COPPA COMPLIANT)
# ==========================================
def upload_to_youtube(video_path: str, episode: dict) -> str:
    """Uploads episodic story video to YouTube marked as Made for Kids."""
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    privacy = os.environ.get("YT_PRIVACY", "public")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials in environment!")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    youtube = build("youtube", "v3", credentials=creds)

    title = episode["youtube_title"]
    description = (
        f"Join Leo the Bear on an exciting storytime adventure: {episode['title']}! 🐻✨\n\n"
        f"Storyline:\n"
        + "\n\n".join([f"✨ {act['act_name']}:\n{act['narration']}" for act in episode["acts"]])
        + "\n\n🔔 Subscribe to Lalafun Stories for brand new daily adventures for kids!\n\n"
        "#Shorts #KidsStory #BedtimeStory #Lalafun #Cocomelon #ChildrenCartoon #ToddlerLearning #Storytime"
    )

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": episode["tags"],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True,  # Mandatory COPPA flag
        }
    }

    print(f"Publishing '{title}' to YouTube ({privacy})...")
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    vid_id = response.get("id")
    video_url = f"https://youtu.be/{vid_id}"
    print(f"SUCCESS! Story live at: {video_url}")
    return vid_id

# ==========================================
# 4. MAIN ENTRY POINT
# ==========================================
def main():
    print(f"=== Lalafun Episodic Story Engine Started ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}) ===")
    episode = random.choice(EPISODES)
    print(f"Selected Story Episode: {episode['title']}")

    voice_file = "story_voice.mp3"
    soundtrack_file = "story_soundtrack.wav"
    output_video_file = "lalafun_story_episode.mp4"

    # 1. Narrative Voiceover
    asyncio.run(generate_story_voiceover(episode, voice_file))

    # 2. Sound Design & Foley Soundtrack
    duration = build_story_soundtrack(episode, voice_file, soundtrack_file)

    # 3. Multi-Act Story Composition
    render_story_video(episode, soundtrack_file, output_video_file, duration)

    # 4. YouTube Upload
    upload_to_youtube(output_video_file, episode)

    print("=== Lalafun Story Episode Finished Successfully ===")

if __name__ == "__main__":
    main()

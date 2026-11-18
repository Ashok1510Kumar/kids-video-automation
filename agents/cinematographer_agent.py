#!/usr/bin/env python3
"""
AGENT 3: CINEMATOGRAPHER & ANIMATION AGENT (@RicksClips3000 Style)
Stages, animates, and renders the 30 FPS micro-documentary short:
- Authentic Rick's Clips Character Rigging (bean head, conjoined eyes, floating brows, costumes)
- Conversational staging with dynamic presentation display board
- Fluid 30 FPS motion with cubic easing and alpha cross-dissolves
- Pure Floating Viral Subtitles & Headlines:
  * ZERO bounding boxes, ZERO dialogue bubbles, ZERO rectangles
  * 4px black stroke for 100% legibility on any background
  * Safe-zone calibrated word wrapping (avoids YouTube Shorts UI overlays)
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, VideoClip

from character_rick import render_ricks_clips_character
from environment_rick import (
    create_studio_workshop_environment,
    create_airplane_window_prop,
    create_airplane_in_flight_prop,
    create_railroad_diagram_prop,
    create_bridge_diagram_prop,
    create_technical_blueprint_prop
)
from draw_utils import draw_floating_subtitles
from smooth_motion import smooth_crossfade

class RicksSceneDirector:
    def __init__(self, episode: dict, total_duration: float, width=720, height=1280):
        self.episode = episode
        self.total_duration = total_duration
        self.width = width
        self.height = height

        # 1. Base Studio Environment (Opaque, zero alpha artifacts)
        self.env_bg = create_studio_workshop_environment(width, height)

        # 2. Dynamic Story Props based on topic
        self._init_props()

        # 3. Pre-render Rick's Clips character rigs
        self._init_characters()

        # 4. Typography
        self._init_fonts()

    def _init_props(self):
        ep_id = self.episode.get("id", "").lower()
        title = self.episode.get("title", "").lower()
        topic_key = f"{ep_id} {title}"

        print(f"[AGENT 3: CINEMATOGRAPHER] Staging visual props for: '{self.episode.get('title')}'...")

        if any(k in topic_key for k in ["plane", "window", "comet", "flight", "air"]):
            p1 = create_airplane_in_flight_prop((540, 280))
            p2 = create_airplane_window_prop((540, 280), window_type="SQUARE_STRESS")
            p3 = create_airplane_window_prop((540, 280), window_type="SQUARE_STRESS")
            p4 = create_airplane_window_prop((540, 280), window_type="OVAL_SAFE")
        elif any(k in topic_key for k in ["rail", "train", "track", "kink", "gap"]):
            p1 = create_railroad_diagram_prop((540, 280), hot_sun_kink=False)
            p2 = create_railroad_diagram_prop((540, 280), hot_sun_kink=False)
            p3 = create_railroad_diagram_prop((540, 280), hot_sun_kink=True)
            p4 = create_railroad_diagram_prop((540, 280), hot_sun_kink=False)
        elif any(k in topic_key for k in ["bridge", "roller", "seismic", "cable", "absorber"]):
            p1 = create_bridge_diagram_prop((540, 280), failure_mode=False)
            p2 = create_bridge_diagram_prop((540, 280), failure_mode=False)
            p3 = create_bridge_diagram_prop((540, 280), failure_mode=True)
            p4 = create_bridge_diagram_prop((540, 280), failure_mode=False)
        else:
            p1 = create_technical_blueprint_prop((540, 280), title=self.episode.get("title", "SCHEMATIC"), subtitle="INVESTIGATION IN PROGRESS", mode="NORMAL")
            p2 = create_technical_blueprint_prop((540, 280), title=self.episode.get("title", "SCHEMATIC"), subtitle="INTUITIVE DESIGN ASSUMPTION", mode="NORMAL")
            p3 = create_technical_blueprint_prop((540, 280), title="STRUCTURAL STRESS ANOMALY", subtitle="CRITICAL FAILURE / WEAR ACCELERATION", mode="DISASTER")
            p4 = create_technical_blueprint_prop((540, 280), title="OPTIMIZED ENGINEERING SOLUTION", subtitle="PHYSICS-BACKED DESIGN EQUILIBRIUM", mode="NORMAL")

        self.beat_props = [p1, p2, p3, p4]

    def _init_characters(self):
        print("[AGENT 3: CINEMATOGRAPHER] Rigging character animation poses...")
        self.char_narrator_talk = render_ricks_clips_character(
            costume="NARRATOR", eye_expression="NEUTRAL", mouth_expression="SPEAKING", arm_pose="POINT_RIGHT"
        )
        self.char_narrator_shock = render_ricks_clips_character(
            costume="NARRATOR", eye_expression="WIDE_SHOCK", mouth_expression="OPEN_O", arm_pose="SHOCKED_HANDS", sweat_drop=True, brow_angle=18.0
        )
        self.char_narrator_smile = render_ricks_clips_character(
            costume="NARRATOR", eye_expression="JOY_ARC", mouth_expression="SMILE", arm_pose="POINT_RIGHT"
        )
        self.char_boss_angry = render_ricks_clips_character(
            costume="BOSS", eye_expression="WIDE_SHOCK", mouth_expression="TEETH_GRIMACE", arm_pose="SHOCKED_HANDS", sweat_drop=True, brow_angle=20.0
        )
        self.char_engineer_skeptical = render_ricks_clips_character(
            costume="ENGINEER", eye_expression="SKEPTICAL", mouth_expression="SPEAKING", arm_pose="IDLE", brow_angle=12.0
        )

    def _init_fonts(self):
        for font_name in ["DejaVuSans-Bold.ttf", "arialbd.ttf"]:
            try:
                self.font_hook = ImageFont.truetype(font_name, 32)
                self.font_caption = ImageFont.truetype(font_name, 30)
                self.font_badge = ImageFont.truetype(font_name, 22)
                return
            except IOError:
                continue
        self.font_hook = self.font_caption = self.font_badge = ImageFont.load_default()

    def get_current_prop(self, beat_idx: int, t_in_beat: float) -> Image.Image:
        cur_idx = min(len(self.beat_props) - 1, beat_idx)
        cur_prop = self.beat_props[cur_idx]

        # Smooth 0.4s cross-fade transition on beat changes
        transition_duration = 0.4
        if beat_idx > 0 and t_in_beat < transition_duration:
            prev_prop = self.beat_props[beat_idx - 1]
            progress = t_in_beat / transition_duration
            return smooth_crossfade(prev_prop, cur_prop, progress)

        return cur_prop

    def render_frame(self, t: float) -> np.ndarray:
        frame = self.env_bg.copy()
        draw = ImageDraw.Draw(frame)

        # Timeline and beat calculation
        beats = self.episode["beats"]
        num_beats = len(beats)
        beat_dur = max(1.0, (self.total_duration - 1.0) / float(num_beats))
        cur_beat_idx = min(num_beats - 1, int(t / beat_dur))
        t_in_beat = t % beat_dur
        cur_beat = beats[cur_beat_idx]

        # ---------------------------------------------------------
        # 1. FLOATING TOP HOOK (NO BOXES, NO BORDERS)
        # ---------------------------------------------------------
        if t < 6.5:
            draw_floating_subtitles(
                draw=draw,
                text=self.episode["hook_line"],
                center_pos=(self.width // 2, 115),
                font=self.font_hook,
                max_width=580,
                fill_color=(255, 225, 0),      # High-CTR Bright Yellow
                stroke_color=(0, 0, 0),         # Bold 4px Black Stroke
                stroke_width=4,
                line_spacing=8
            )

        # ---------------------------------------------------------
        # 2. PRESENTATION DISPLAY SCREEN (SMOOTH CROSS-DISSOLVES)
        # ---------------------------------------------------------
        screen_x = 90
        screen_y = 230
        active_prop = self.get_current_prop(cur_beat_idx, t_in_beat)
        frame.alpha_composite(active_prop, (screen_x, screen_y))

        # ---------------------------------------------------------
        # 3. CHARACTER ANIMATION RIG (NATURAL IDLE & EMOTIONS)
        # ---------------------------------------------------------
        # Gentle harmonic breathing idle sway
        idle_bounce = int(3.5 * math.sin(t * 5.0))
        role = cur_beat.get("character_role", "NARRATOR")

        if role == "BOSS":
            char_sprite = self.char_boss_angry
        elif role == "ENGINEER":
            char_sprite = self.char_engineer_skeptical
        elif cur_beat_idx == 2:
            char_sprite = self.char_narrator_shock
        elif cur_beat_idx == 3:
            char_sprite = self.char_narrator_smile
        else:
            char_sprite = self.char_narrator_talk

        char_x = int(self.width * 0.22)
        char_y = 520 + idle_bounce
        frame.alpha_composite(char_sprite, (char_x, char_y))

        # ---------------------------------------------------------
        # 4. PURE FLOATING SUBTITLES (NO BOXES, NO BORDERS)
        # ---------------------------------------------------------
        # Sentence splitting for comfortable rapid reading
        sentences = [s.strip() for s in cur_beat["narration"].split(".") if len(s.strip()) > 3]
        if not sentences:
            sentences = [cur_beat["narration"]]
        s_idx = min(len(sentences) - 1, int(t_in_beat / (beat_dur / max(1, len(sentences)))))
        current_sentence = sentences[s_idx]

        # Centered at y=1060: perfectly positioned in Shorts safe zone
        # (Above title/sound overlay, away from right action icons)
        draw_floating_subtitles(
            draw=draw,
            text=current_sentence,
            center_pos=(self.width // 2, self.height - 210),
            font=self.font_caption,
            max_width=560,
            fill_color=(255, 255, 255),      # Crisp White Text
            stroke_color=(0, 0, 0),          # Bold 4px Black Outline
            stroke_width=4,
            line_spacing=8
        )

        # ---------------------------------------------------------
        # 5. FLOATING OUTRO CALLOUT (LAST 2.5 SECONDS, NO BOX)
        # ---------------------------------------------------------
        if t >= self.total_duration - 2.5:
            draw.text(
                (self.width // 2, self.height - 290),
                "SUBSCRIBE FOR DAILY MYSTERIES!",
                font=self.font_badge,
                fill=(255, 225, 0),
                stroke_width=3,
                stroke_fill=(0, 0, 0),
                anchor="mm"
            )

        # Convert to RGB numpy array for MoviePy
        rgb_canvas = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        rgb_canvas.paste(frame, (0, 0), mask=frame.split()[3])
        return np.array(rgb_canvas)

class CinematographerAgent:
    def __init__(self, width=720, height=1280, fps=30):
        self.width = width
        self.height = height
        self.fps = fps

    def film_and_render(self, episode: dict, audio_path: str, output_video_path: str, duration: float):
        """
        Coordinates full scene rendering and video encoding at silky-smooth 30 FPS.
        """
        print(f"[AGENT 3: CINEMATOGRAPHER] Initiating 30 FPS filming session ({duration:.1f}s)...")
        director = RicksSceneDirector(episode, duration, width=self.width, height=self.height)
        audio_clip = AudioFileClip(audio_path)

        video = VideoClip(lambda t: director.render_frame(t), duration=duration).set_audio(audio_clip)

        video.write_videofile(
            output_video_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            logger=None
        )
        print(f"[AGENT 3: CINEMATOGRAPHER] Filming complete! Rendered video: {output_video_path} (30 FPS, {duration:.1f}s)")

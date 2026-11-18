#!/usr/bin/env python3
"""
AGENT 2: AUDIO ENGINEER AGENT (@RicksClips3000 Style)
Produces crisp, broadcast-quality audio tracks:
- High-velocity 175 WPM conversational American male voiceover (edge-tts en-US-GuyNeural)
- Syncopated lo-fi groove backing music (ducked at -18dB)
- Precise foley sound effects synchronized with story beats (pop, boing, whoosh, fanfare)
- Balanced master audio output ready for video composition
"""

import asyncio
from moviepy.editor import AudioFileClip, CompositeAudioClip
import edge_tts

from music_generator import generate_nursery_music
from sfx_generator import generate_all_sfx

VOICE_NAME = "en-US-GuyNeural"

class AudioEngineerAgent:
    def __init__(self, voice_name: str = VOICE_NAME, rate: str = "+9%"):
        self.voice_name = voice_name
        self.rate = rate

    async def _synthesize_voice(self, full_text: str, output_voice_path: str):
        print(f"[AGENT 2: AUDIO ENGINEER] Synthesizing voiceover with {self.voice_name} at {self.rate} speed...")
        communicate = edge_tts.Communicate(full_text, self.voice_name, rate=self.rate, pitch="+0Hz")
        await communicate.save(output_voice_path)

    def produce_soundtrack(self, episode: dict, voice_path: str, output_soundtrack_path: str) -> float:
        """
        Synthesizes voice, generates sound effects, composes lo-fi groove,
        and masters the final composite audio soundtrack.
        Returns total audio duration in seconds.
        """
        print("[AGENT 2: AUDIO ENGINEER] Assembling narration script text...")
        full_text = " ".join([beat["narration"] for beat in episode["beats"]])

        # 1. Synthesize Voiceover
        asyncio.run(self._synthesize_voice(full_text, voice_path))

        # 2. Measure voice duration and compute total timeline
        voice_clip = AudioFileClip(voice_path)
        intro_lead = 0.5
        outro_tail = 2.0
        total_duration = intro_lead + voice_clip.duration + outro_tail

        print(f"[AGENT 2: AUDIO ENGINEER] Raw voice duration: {voice_clip.duration:.1f}s. Total target runtime: {total_duration:.1f}s")

        # 3. Generate Foley SFX and Backing Groove
        generate_all_sfx()
        music_temp = "music_temp.wav"
        print("[AGENT 2: AUDIO ENGINEER] Generating syncopated lo-fi groove music...")
        generate_nursery_music("groove", total_duration, music_temp, bpm=114)

        # 4. Master and Mix Layers
        # Backing music ducked to 18% (-18dB) so speech is crystal clear
        music_clip = AudioFileClip(music_temp).volumex(0.18)
        voice_clip = voice_clip.volumex(1.0).set_start(intro_lead)

        sfx_layers = [music_clip, voice_clip]

        # Calculate beat timestamps for sound effects
        num_beats = len(episode["beats"])
        beat_dur = voice_clip.duration / max(1, num_beats)

        # Beat 1: Intro pop
        sfx_layers.append(AudioFileClip("sfx_pop.wav").volumex(0.32).set_start(intro_lead + 0.3))

        # Beat 2: Tension / Boing
        t_beat2 = intro_lead + beat_dur
        sfx_layers.append(AudioFileClip("sfx_boing.wav").volumex(0.35).set_start(t_beat2))

        # Beat 3: Scientific disaster / Whoosh
        t_beat3 = intro_lead + (beat_dur * 2)
        sfx_layers.append(AudioFileClip("sfx_whoosh.wav").volumex(0.30).set_start(t_beat3))

        # Beat 4: Resolution / Fanfare
        t_beat4 = intro_lead + (beat_dur * 3)
        sfx_layers.append(AudioFileClip("sfx_fanfare.wav").volumex(0.30).set_start(t_beat4))

        composite_audio = CompositeAudioClip(sfx_layers).set_duration(total_duration)
        composite_audio.write_audiofile(output_soundtrack_path, fps=44100, logger=None)

        print(f"[AGENT 2: AUDIO ENGINEER] Soundtrack successfully mastered: {output_soundtrack_path} ({total_duration:.1f}s)")
        return total_duration

if __name__ == "__main__":
    agent = AudioEngineerAgent()
    sample_ep = {
        "beats": [
            {"narration": "Why do engineers deliberately leave gaps between steel train tracks?"},
            {"narration": "In the 1800s, an arrogant railroad tycoon ordered his workers to weld all rails tight with zero gaps."},
            {"narration": "When summer heat struck, the expanding steel had nowhere to go, twisting the entire railway into violent sun kinks."},
            {"narration": "Those tiny expansion gaps absorb thermal expansion, keeping high-speed trains safely on the tracks!"}
        ]
    }
    agent.produce_soundtrack(sample_ep, "sample_voice.mp3", "sample_soundtrack.wav")

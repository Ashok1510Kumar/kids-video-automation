#!/usr/bin/env python3
"""
RICKS CLIPS GROOVE & SOUNDTRACK GENERATOR (@RicksClips3000 Style)
Synthesizes modern, syncopated lo-fi funk/groove tracks and story melodies in pure Python.
"""

import math
import struct
import wave

NOTE_FREQS = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00,
    'REST': 0.0
}

# Rick's Clips Syncopated Lo-Fi Groove Bass & Chords (A minor / D minor funk groove)
GROOVE_PATTERN = [
    # Beat 1: Punchy Root Bass
    ('A3', 0.5), ('REST', 0.25), ('A3', 0.25),
    # Beat 2: Syncopated chord stab
    ('C4', 0.5), ('E4', 0.5),
    # Beat 3: Walking Bass
    ('D3', 0.5), ('F3', 0.25), ('G3', 0.25),
    # Beat 4: Funky resolution
    ('A3', 0.5), ('REST', 0.5),
]

def generate_nursery_music(melody_name: str, target_duration: float, output_wav: str, bpm: int = 115):
    """
    Synthesizes a steady syncopated storytelling groove track looping to target_duration.
    """
    sample_rate = 44100
    beat_sec = 60.0 / bpm
    raw_samples = []
    current_time = 0.0

    while current_time < target_duration + 1.0:
        for note_name, beats in GROOVE_PATTERN:
            if current_time >= target_duration + 1.0:
                break
            freq = NOTE_FREQS.get(note_name, 0.0)
            duration_sec = beats * beat_sec
            num_samples = int(sample_rate * duration_sec)

            for i in range(num_samples):
                t = i / sample_rate
                if freq == 0.0:
                    sample = 0.0
                else:
                    # Warm electric bass / Rhodes keyboard physical synthesis
                    env = math.exp(-t * 4.0)
                    tone = math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(2 * math.pi * freq * 2.0 * t)
                    sample = tone * env * 0.28
                raw_samples.append(sample)
            current_time += duration_sec

    # Trim to exact duration
    total_needed = int(sample_rate * target_duration)
    raw_samples = raw_samples[:total_needed]

    # Soft fade out at end
    fade_len = int(sample_rate * 1.5)
    start_fade = max(0, len(raw_samples) - fade_len)
    for idx in range(start_fade, len(raw_samples)):
        raw_samples[idx] *= (len(raw_samples) - idx) / float(fade_len)

    with wave.open(output_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = bytearray()
        for s in raw_samples:
            clipped = max(-1.0, min(1.0, s))
            packed.extend(struct.pack('<h', int(clipped * 32767.0)))
        wf.writeframes(packed)

    print(f"Generated Rick's Clips syncopated groove track: {output_wav} ({target_duration:.1f}s)")

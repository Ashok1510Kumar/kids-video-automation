#!/usr/bin/env python3
"""
STORY SOUND EFFECTS SYNTHESIZER
Synthesizes professional cartoon SFX for narrative beats:
- Pop! (discoveries, surprises)
- Boing! (bounces, wobbling, jumps)
- Sparkle Chime (magic, stars, fairy dust)
- Fanfare! (celebrations, victories, happy resolutions)
- Whoosh! (scene transitions, flying)
"""

import math
import struct
import wave

def write_wav(filename: str, samples: list, sample_rate=44100):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = bytearray()
        for s in samples:
            clipped = max(-1.0, min(1.0, s))
            packed.extend(struct.pack('<h', int(clipped * 32767.0)))
        wf.writeframes(packed)

def create_pop_sfx(output_path: str):
    sr = 44100
    duration = 0.12
    num_samples = int(sr * duration)
    samples = []
    for i in range(num_samples):
        t = i / sr
        freq = 300.0 + 1600.0 * (t / duration) ** 0.5
        env = math.exp(-t * 35.0)
        s = math.sin(2 * math.pi * freq * t) * env * 0.45
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_bounce_boing_sfx(output_path: str):
    sr = 44100
    duration = 0.32
    num_samples = int(sr * duration)
    samples = []
    for i in range(num_samples):
        t = i / sr
        wobble = math.sin(2 * math.pi * 14.0 * t) * 50.0
        freq = 200.0 + wobble - 60.0 * (t / duration)
        env = math.exp(-t * 9.0)
        s = math.sin(2 * math.pi * freq * t) * env * 0.42
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_sparkle_chime_sfx(output_path: str):
    sr = 44100
    duration = 0.90
    num_samples = int(sr * duration)
    samples = []
    freqs = [1046.5, 1318.5, 1567.98, 1975.5, 2093.0, 2637.0]
    for i in range(num_samples):
        t = i / sr
        s = 0.0
        for idx, f in enumerate(freqs):
            note_start = idx * 0.07
            if t >= note_start:
                nt = t - note_start
                env = math.exp(-nt * 6.5)
                s += math.sin(2 * math.pi * f * nt) * env * 0.14
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_fanfare_sfx(output_path: str):
    """Joyful celebratory fanfare chord (C - E - G - C) for story happy endings."""
    sr = 44100
    duration = 1.4
    num_samples = int(sr * duration)
    samples = []
    chords = [
        (0.00, 523.25),  # C5
        (0.18, 659.25),  # E5
        (0.36, 783.99),  # G5
        (0.54, 1046.50), # C6 triumphant bell
    ]
    for i in range(num_samples):
        t = i / sr
        s = 0.0
        for start_t, f in chords:
            if t >= start_t:
                nt = t - start_t
                env = math.exp(-nt * 3.5)
                # Harmonic richness: fundamental + 2nd harmonic
                tone = math.sin(2 * math.pi * f * nt) + 0.35 * math.sin(2 * math.pi * f * 2.0 * nt)
                s += tone * env * 0.22
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_whoosh_sfx(output_path: str):
    """Dynamic whoosh sound for scene transitions."""
    sr = 44100
    duration = 0.40
    num_samples = int(sr * duration)
    samples = []
    for i in range(num_samples):
        t = i / sr
        freq = 150.0 + 800.0 * math.sin(math.pi * (t / duration))
        env = math.sin(math.pi * (t / duration)) ** 2
        s = math.sin(2 * math.pi * freq * t) * env * 0.35
        samples.append(s)
    write_wav(output_path, samples, sr)

def generate_all_sfx():
    create_pop_sfx("sfx_pop.wav")
    create_bounce_boing_sfx("sfx_boing.wav")
    create_sparkle_chime_sfx("sfx_sparkle.wav")
    create_fanfare_sfx("sfx_fanfare.wav")
    create_whoosh_sfx("sfx_whoosh.wav")
    print("Generated full narrative SFX package (pop, boing, sparkle, fanfare, whoosh).")

if __name__ == "__main__":
    generate_all_sfx()

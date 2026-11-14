#!/usr/bin/env python3
"""
CARTOON SOUND EFFECTS SYNTHESIZER
Synthesizes professional cartoon sound effects (pops, boings, sparkle chimes)
in pure Python for audio polish and bouncy timing.
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
    """Cartoon 'Pop!' sound when lyrics or buttons appear."""
    sr = 44100
    duration = 0.12
    num_samples = int(sr * duration)
    samples = []
    for i in range(num_samples):
        t = i / sr
        # Rapid upward pitch sweep 300Hz -> 1800Hz with exponential decay
        freq = 300.0 + 1500.0 * (t / duration) ** 0.5
        env = math.exp(-t * 35.0)
        s = math.sin(2 * math.pi * freq * t) * env * 0.45
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_bounce_boing_sfx(output_path: str):
    """Bouncy spring 'Boing!' sound for character landings."""
    sr = 44100
    duration = 0.28
    num_samples = int(sr * duration)
    samples = []
    for i in range(num_samples):
        t = i / sr
        # Vibrating spring frequency with pitch wobble
        wobble = math.sin(2 * math.pi * 14.0 * t) * 45.0
        freq = 180.0 + wobble - 60.0 * (t / duration)
        env = math.exp(-t * 11.0)
        s = math.sin(2 * math.pi * freq * t) * env * 0.40
        samples.append(s)
    write_wav(output_path, samples, sr)

def create_sparkle_chime_sfx(output_path: str):
    """Magic sparkle shimmer for intro and stars."""
    sr = 44100
    duration = 0.85
    num_samples = int(sr * duration)
    samples = []
    # Arpeggio of sweet high frequencies (C6, E6, G6, B6, C7)
    freqs = [1046.5, 1318.5, 1567.98, 1975.5, 2093.0]
    for i in range(num_samples):
        t = i / sr
        s = 0.0
        for idx, f in enumerate(freqs):
            note_start = idx * 0.08
            if t >= note_start:
                nt = t - note_start
                env = math.exp(-nt * 7.0)
                s += math.sin(2 * math.pi * f * nt) * env * 0.15
        samples.append(s)
    write_wav(output_path, samples, sr)

def generate_all_sfx():
    create_pop_sfx("sfx_pop.wav")
    create_bounce_boing_sfx("sfx_boing.wav")
    create_sparkle_chime_sfx("sfx_sparkle.wav")
    print("Generated cartoon SFX package: sfx_pop.wav, sfx_boing.wav, sfx_sparkle.wav")

if __name__ == "__main__":
    generate_all_sfx()

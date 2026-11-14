#!/usr/bin/env python3
"""
Nursery Rhyme Melody Synthesizer
Generates cheerful music box / glockenspiel melodies in pure Python (no external sound libraries).
"""

import math
import struct
import wave

# Musical note frequencies (Hz)
NOTE_FREQS = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C6': 1046.50, 'REST': 0.0
}

# Classic Nursery Rhyme Melodies: (Note, Duration in beats)
MELODIES = {
    "twinkle": [
        ('C5', 1), ('C5', 1), ('G5', 1), ('G5', 1), ('A5', 1), ('A5', 1), ('G5', 2),
        ('F5', 1), ('F5', 1), ('E5', 1), ('E5', 1), ('D5', 1), ('D5', 1), ('C5', 2),
        ('G5', 1), ('G5', 1), ('F5', 1), ('F5', 1), ('E5', 1), ('E5', 1), ('D5', 2),
        ('G5', 1), ('G5', 1), ('F5', 1), ('F5', 1), ('E5', 1), ('E5', 1), ('D5', 2),
        ('C5', 1), ('C5', 1), ('G5', 1), ('G5', 1), ('A5', 1), ('A5', 1), ('G5', 2),
        ('F5', 1), ('F5', 1), ('E5', 1), ('E5', 1), ('D5', 1), ('D5', 1), ('C5', 2),
    ],
    "wheels_on_bus": [
        ('C5', 1), ('F5', 1), ('F5', 1), ('F5', 1), ('F5', 1.5), ('A5', 0.5), ('C6', 1), ('A5', 1),
        ('F5', 2), ('G5', 1.5), ('E5', 0.5), ('C5', 2),
        ('A5', 1.5), ('F5', 0.5), ('C5', 2),
        ('C5', 1), ('F5', 1), ('F5', 1), ('F5', 1), ('F5', 1.5), ('A5', 0.5), ('C6', 1), ('A5', 1),
        ('F5', 1), ('G5', 1), ('C5', 1), ('E5', 1), ('F5', 2),
    ],
    "old_macdonald": [
        ('F5', 1), ('F5', 1), ('F5', 1), ('C5', 1), ('D5', 1), ('D5', 1), ('C5', 2),
        ('A5', 1), ('A5', 1), ('G5', 1), ('G5', 1), ('F5', 2), ('REST', 1),
        ('C5', 1), ('F5', 1), ('F5', 1), ('F5', 1), ('C5', 1), ('D5', 1), ('D5', 1), ('C5', 2),
        ('A5', 1), ('A5', 1), ('G5', 1), ('G5', 1), ('F5', 2),
    ],
    "happy_and_you_know_it": [
        ('C5', 0.75), ('C5', 0.25), ('F5', 1), ('F5', 1), ('F5', 1), ('F5', 1),
        ('E5', 1), ('F5', 1), ('G5', 2), ('REST', 0.5),
        ('C5', 0.75), ('C5', 0.25), ('G5', 1), ('G5', 1), ('G5', 1), ('G5', 1),
        ('F5', 1), ('G5', 1), ('A5', 2), ('REST', 0.5),
        ('F5', 0.75), ('F5', 0.25), ('B5', 1), ('B5', 1), ('B5', 1), ('B5', 1),
        ('A5', 1), ('F5', 1), ('D5', 1.5), ('REST', 0.5),
        ('D5', 0.75), ('D5', 0.25), ('C5', 1), ('A5', 1), ('G5', 1), ('E5', 1), ('F5', 2),
    ]
}

def generate_nursery_music(melody_name: str, target_duration: float, output_wav: str, bpm: int = 110):
    """
    Synthesizes a pleasant music box / glockenspiel track looping until target_duration.
    """
    sample_rate = 44100
    beat_duration = 60.0 / bpm
    notes = MELODIES.get(melody_name, MELODIES["twinkle"])

    raw_samples = []
    current_time = 0.0

    # Loop melody until reaching target_duration
    while current_time < target_duration + 1.0:
        for note_name, beats in notes:
            if current_time >= target_duration + 1.0:
                break
            freq = NOTE_FREQS.get(note_name, 0.0)
            duration_sec = beats * beat_duration
            num_samples = int(sample_rate * duration_sec)

            for i in range(num_samples):
                t = i / sample_rate
                if freq == 0.0:
                    sample = 0.0
                else:
                    # Glockenspiel / Music box physical model:
                    # Fundamental + 2nd Harmonic + 3rd Harmonic + exponential decay envelope
                    env = math.exp(-t * 3.2)
                    vibrato = math.sin(2 * math.pi * 5.0 * t) * 0.005
                    val1 = math.sin(2 * math.pi * (freq * (1 + vibrato)) * t)
                    val2 = 0.45 * math.sin(2 * math.pi * (freq * 2.002) * t) * math.exp(-t * 4.5)
                    val3 = 0.20 * math.sin(2 * math.pi * (freq * 3.003) * t) * math.exp(-t * 6.0)
                    sample = (val1 + val2 + val3) * env * 0.35

                raw_samples.append(sample)
            current_time += duration_sec

    # Trim to exact target duration
    total_needed = int(sample_rate * target_duration)
    raw_samples = raw_samples[:total_needed]

    # Apply soft fade-out in the last 1.5 seconds
    fade_samples = int(sample_rate * 1.5)
    start_fade = max(0, len(raw_samples) - fade_samples)
    for idx in range(start_fade, len(raw_samples)):
        factor = (len(raw_samples) - idx) / float(fade_samples)
        raw_samples[idx] *= factor

    # Write 16-bit PCM mono WAV file
    with wave.open(output_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed_data = bytearray()
        for s in raw_samples:
            clipped = max(-1.0, min(1.0, s))
            int_val = int(clipped * 32767.0)
            packed_data.extend(struct.pack('<h', int_val))
        wf.writeframes(packed_data)

    print(f"Generated cheerful music box background: {output_wav} ({target_duration:.1f}s)")

#!/usr/bin/env python3
"""
GOOGLE GEMINI SCRIPT GENERATION FLOW (@RicksClips3000 Style)
Uses Google Gemini API to dynamically research, write, and structure viral,
high-retention 45-second micro-documentary scripts.
"""

import os
import json
import random
import requests
from stories_rick import RICKS_EPISODES

# Rich topic inspirations for Google Gemini
TOPIC_PROMPTS = [
    "Why bridges have giant rubber shock absorbers or expansion rollers underneath them",
    "Why nuclear cooling towers are shaped like giant curved hourglasses",
    "Why submarine hulls are circular cylinders instead of rectangular ships",
    "Why highway overpasses are intentionally built in zig-zag shapes in earthquake zones",
    "Why bullet trains in Japan were redesigned with kingfisher bird beaks to stop sonic booms",
    "Why elevator cables are designed to hold 10 times the weight of the elevator cab",
    "Why ancient Roman aqueducts survived 2,000 years without modern steel reinforcement",
    "Why cruise ship hulls have a giant bulbous nose underwater at the front",
    "Why skyscraper windows are made of double-pane tempered glass that can flex in hurricanes"
]

SYSTEM_PROMPT = """You are the master scriptwriter for a viral YouTube Shorts channel like @RicksClips3000.
Your specialty is fascinating engineering paradoxes, weird design choices, and historical technology mysteries.

STRICT FORMAT & PACING RULES:
1. Total length: Exactly 110 to 135 words (at 175 words per minute, this takes exactly 40-45 seconds).
2. The Hook (0-6s): A counter-intuitive paradox that immediately stops scrolling.
3. The Conflict / Trap (6-20s): A stubborn boss or intuitive common-sense mistake.
4. The Technical / Scientific Payoff (20-38s): Clear physical demonstration of why the flaw or weird design is actually genius.
5. The Punchline / Lesson (38-45s): Snappy, memorable takeaway.

You MUST reply ONLY with valid, clean JSON matching this exact structure:
{
  "id": "slug_topic",
  "title": "Short descriptive topic title",
  "youtube_title": "Catchy YouTube Title with Emojis #Shorts #Engineering",
  "hook_line": "The opening paradox question (under 12 words)",
  "beats": [
    {
      "beat_name": "THE PARADOX HOOK",
      "character_role": "NARRATOR",
      "narration": "First sentence posing the paradox.",
      "prop_type": "NORMAL"
    },
    {
      "beat_name": "THE COMMON SENSE TRAP",
      "character_role": "BOSS",
      "narration": "The intuitive demand or common mistake.",
      "prop_type": "NORMAL"
    },
    {
      "beat_name": "THE DISASTER & SCIENCE",
      "character_role": "ENGINEER",
      "narration": "The physical consequence and why physics requires this design.",
      "prop_type": "DISASTER"
    },
    {
      "beat_name": "THE PUNCHLINE",
      "character_role": "NARRATOR",
      "narration": "The witty engineering moral of the story.",
      "prop_type": "NORMAL"
    }
  ],
  "tags": ["engineering", "science", "curiosity", "history", "fun facts", "ricksclips", "shorts"]
}
"""

def generate_script_with_gemini(api_key: str) -> dict:
    """Calls Google Gemini API to generate a fresh, dynamic story script."""
    topic = random.choice(TOPIC_PROMPTS)
    print(f"Calling Google Gemini Flow for topic: '{topic}'...")

    candidate_models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{SYSTEM_PROMPT}\n\nWrite an episode about: {topic}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }

        try:
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                if raw_text.startswith("```json"):
                    raw_text = raw_text.split("```json", 1)[1].rsplit("```", 1)[0].strip()
                elif raw_text.startswith("```"):
                    raw_text = raw_text.split("```", 1)[1].rsplit("```", 1)[0].strip()
                script_json = json.loads(raw_text)
                print(f"Google Gemini generated script using {model}: '{script_json.get('title')}'")
                return script_json
            else:
                print(f"Gemini {model} returned ({res.status_code}): {res.text}. Trying next candidate...")
        except Exception as e:
            print(f"Gemini generation exception on {model}: {e}")

    return None

def get_daily_episode() -> dict:
    """
    Primary: Generates a brand new, dynamic script via Google Gemini.
    Fallback: Uses the curated high-retention episode bank if no key is present.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if gemini_key:
        generated = generate_script_with_gemini(gemini_key)
        if generated and "beats" in generated and len(generated["beats"]) >= 4:
            return generated
        print("Gemini response was invalid or empty, falling back to curated episode.")

    # Graceful fallback to curated catalog
    print("Using curated high-retention episode from catalog.")
    return random.choice(RICKS_EPISODES)

if __name__ == "__main__":
    ep = get_daily_episode()
    print("Episode Title:", ep.get("title"))
    print("Hook:", ep.get("hook_line"))
    for idx, b in enumerate(ep.get("beats", [])):
        print(f"[{b.get('character_role')}]: {b.get('narration')}")

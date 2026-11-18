#!/usr/bin/env python3
"""
AGENT 1: SCREENWRITER AGENT (Google Flow / Gemini API)
Researches, structures, and writes viral 45-second micro-documentary scripts
modeled after @RicksClips3000 (Rick's Clips).

Story Structure:
1. Beat 1: The Paradox Hook (0-6s) - Counter-intuitive mystery or question.
2. Beat 2: The Common Sense Trap (6-20s) - Why intuitive thinking fails; stubborn boss/engineer demand.
3. Beat 3: The Scientific Breakdown (20-38s) - Physics, engineering disaster, or underlying mechanism.
4. Beat 4: The Genius Solution / Punchline (38-45s) - Clever payoff and witty takeaway.
"""

import os
import json
import random
import requests
from stories_rick import RICKS_EPISODES

CURATED_TOPICS = [
    "Why airplane windows are oval instead of square (The 1954 Comet crashes)",
    "Why engineers deliberately leave gaps between steel train tracks (Sun kinks)",
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

SYSTEM_PROMPT = """You are the master screenwriter for a viral YouTube Shorts channel modeled after @RicksClips3000.
Your specialty is fascinating engineering paradoxes, weird design choices, and historical technology mysteries.

STRICT FORMAT & PACING RULES:
1. Total length: Write a detailed, complete narration of 90 to 125 words (at 175 words per minute, this takes 35-45 seconds).
2. The Hook (0-6s): A punchy paradox question that immediately stops the user from scrolling. (1-2 full sentences).
3. The Conflict / Trap (6-20s): Introduce a character dialogue (like an impatient tycoon, airline executive, or intuitive designer) making a stubborn common-sense demand. (2-3 sentences).
4. The Technical / Scientific Payoff (20-38s): Clear physical demonstration of why the flaw or weird design is actually pure engineering genius. (2-3 sentences).
5. The Punchline / Lesson (38-45s): Snappy, memorable conclusion with a witty takeaway. (1-2 sentences).

You MUST reply ONLY with valid, clean JSON matching this exact schema:
{
  "id": "slug_topic",
  "title": "Short descriptive topic title",
  "youtube_title": "Catchy YouTube Title with Emojis #Shorts #Engineering",
  "hook_line": "The opening paradox question (under 12 words)",
  "beats": [
    {
      "beat_name": "THE PARADOX HOOK",
      "character_role": "NARRATOR",
      "narration": "Detailed first sentence posing the paradox.",
      "prop_type": "NORMAL"
    },
    {
      "beat_name": "THE COMMON SENSE TRAP",
      "character_role": "BOSS",
      "narration": "The boss or intuitive engineer demands a common-sense design.",
      "prop_type": "NORMAL"
    },
    {
      "beat_name": "THE DISASTER & SCIENCE",
      "character_role": "ENGINEER",
      "narration": "The physical breakdown explaining the hidden physics or catastrophic flaw.",
      "prop_type": "DISASTER"
    },
    {
      "beat_name": "THE PUNCHLINE",
      "character_role": "NARRATOR",
      "narration": "The witty engineering moral and genius resolution.",
      "prop_type": "NORMAL"
    }
  ],
  "tags": ["engineering", "science", "curiosity", "history", "fun facts", "ricksclips", "shorts"]
}
"""

class ScreenwriterAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_FLOW_ID") or os.environ.get("GOOGLE_FLOW_KEY")

    def write_script(self, topic: str = None) -> dict:
        """
        Executes the Screenwriter workflow:
        1. Dynamically queries Google Gemini API.
        2. Validates structure, word count, and beats.
        3. Seamlessly falls back to curated episodes if network or key fails.
        """
        if not topic:
            topic = random.choice(CURATED_TOPICS)

        print(f"[AGENT 1: SCREENWRITER] Brainstorming story on topic: '{topic}'...")

        if self.api_key:
            try:
                episode = self._generate_with_gemini(topic)
                if episode and self._validate_episode(episode):
                    print(f"[AGENT 1: SCREENWRITER] Successfully generated script via Google Flow: '{episode.get('title')}'")
                    return episode
                else:
                    print("[AGENT 1: SCREENWRITER] Gemini response did not meet strict quality checks. Using curated catalog.")
            except Exception as e:
                print(f"[AGENT 1: SCREENWRITER] Gemini API call exception ({e}). Falling back to curated catalog.")
        else:
            print("[AGENT 1: SCREENWRITER] GEMINI_API_KEY / GOOGLE_FLOW_ID not detected. Using curated high-retention catalog.")

        # Fallback to curated catalog
        episode = random.choice(RICKS_EPISODES)
        print(f"[AGENT 1: SCREENWRITER] Selected story from curated catalog: '{episode['title']}'")
        return episode

    def _discover_models(self) -> list:
        """Dynamically fetches active models supported by the user's API key."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
            res = requests.get(url, timeout=8)
            if res.status_code == 200:
                data = res.json()
                active = [
                    m["name"] for m in data.get("models", [])
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]
                if active:
                    # Sort flash models to the front
                    flash_first = sorted(active, key=lambda x: ("flash" in x, x), reverse=True)
                    print(f"[AGENT 1: SCREENWRITER] Discovered live models from Google API: {flash_first[:3]}")
                    return flash_first
        except Exception as e:
            print(f"[AGENT 1: SCREENWRITER] Model discovery notice: {e}")

        return ["models/gemini-2.5-flash", "models/gemini-1.5-flash", "models/gemini-pro"]

    def _generate_with_gemini(self, topic: str) -> dict:
        models = self._discover_models()

        for model in models:
            # Model names may already contain "models/" prefix
            clean_model = model if model.startswith("models/") else f"models/{model}"
            url = f"https://generativelanguage.googleapis.com/v1beta/{clean_model}:generateContent?key={self.api_key}"

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
                    print(f"[AGENT 1: SCREENWRITER] Google Gemini Flow success with {clean_model}!")
                    return json.loads(raw_text)
                else:
                    print(f"[AGENT 1: SCREENWRITER] Gemini {clean_model} returned {res.status_code}. Trying next candidate...")
            except Exception as e:
                print(f"[AGENT 1: SCREENWRITER] Request error for {clean_model}: {e}")

        return None

    def _validate_episode(self, ep: dict) -> bool:
        if not isinstance(ep, dict):
            return False
        if not ep.get("title") or not ep.get("hook_line") or not ep.get("beats"):
            return False
        if len(ep["beats"]) < 4:
            return False

        all_words = sum(len(b.get("narration", "").split()) for b in ep["beats"])
        print(f"[AGENT 1: SCREENWRITER] Script word count: {all_words} words (ideal: 90-135)")
        return all_words >= 60

if __name__ == "__main__":
    agent = ScreenwriterAgent()
    script = agent.write_script()
    print("Script preview:")
    print(json.dumps(script, indent=2))

#!/usr/bin/env python3
"""
RICKS CLIPS STORY CATALOG (@RicksClips3000 Narrative Formula)
Curated high-retention 45-second micro-documentaries & paradox stories:
- 0:00 - 0:06: Irresistible paradox hook ("Why do engineers deliberately break this?")
- 0:06 - 0:22: The Intuitive Common-Sense Trap & Conflict (Boss vs Reality)
- 0:22 - 0:42: The Mechanical / Scientific Payoff & Demonstration
- 0:42 - 0:48: Snappy ironic punchline
"""

RICKS_EPISODES = [
    {
        "id": "railroad_gaps",
        "title": "Why Railroads MUST Have Flaws Built Into Them",
        "youtube_title": "Why Perfect Railroads DON'T Work! 🚂💥 #Shorts #Engineering",
        "hook_line": "Why do engineers deliberately leave ugly gaps in brand-new train tracks?",
        "beats": [
            {
                "beat_name": "THE PARADOX HOOK",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "NEUTRAL", "mouth_expression": "SPEAKING", "arm_pose": "POINT_RIGHT", "brow_angle": -5.0, "sweat_drop": False},
                "narration": "In the 1800s, an arrogant railroad tycoon looked at his workers and screamed: 'Why are there gaps between my rails? Smooth them out! I want ZERO gaps!'",
                "duration": 10.0,
                "prop_visual": "RAILROAD_GAP_COIN"
            },
            {
                "beat_name": "THE COMMON SENSE TRAP",
                "character_role": "BOSS",
                "character_state": {"eye_expression": "WIDE_SHOCK", "mouth_expression": "TEETH_GRIMACE", "arm_pose": "SHOCKED_HANDS", "brow_angle": 15.0, "sweat_drop": True},
                "narration": "The engineers warned him. But the tycoon refused to listen and welded every single rail together seamless and perfect. Everything was great... until July arrived.",
                "duration": 11.0,
                "prop_visual": "WELDED_SEAMLESS_RAIL"
            },
            {
                "beat_name": "THE SCIENTIFIC DISASTER",
                "character_role": "ENGINEER",
                "character_state": {"eye_expression": "WIDE_SHOCK", "mouth_expression": "OPEN_O", "arm_pose": "SHOCKED_HANDS", "brow_angle": 20.0, "sweat_drop": True},
                "narration": "Steel expands when it heats up in the summer sun! With nowhere to grow, thousands of tons of pressure built up until suddenly... SNAP! The steel tracks twisted into a jagged S-curve known as a 'sun kink'!",
                "duration": 13.0,
                "prop_visual": "SUN_KINK_BUCKLE"
            },
            {
                "beat_name": "THE SNAPPY LESSON",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "SKEPTICAL", "mouth_expression": "SMILE", "arm_pose": "POINT_RIGHT", "brow_angle": -8.0, "sweat_drop": False},
                "narration": "That's why engineers still leave deliberate gaps today. Because in engineering, perfection isn't having zero flaws... it's knowing where to put them.",
                "duration": 11.0,
                "prop_visual": "ENGINEERING_DIAGRAM"
            }
        ],
        "tags": ["engineering", "trains", "science", "curiosity", "history", "fun facts", "ricksclips", "shorts"]
    },
    {
        "id": "airplane_windows",
        "title": "Why Airplane Windows Are NEVER Square",
        "youtube_title": "Why Airplane Windows Are NEVER Square! ✈️📐 #Shorts #Mystery",
        "hook_line": "Notice how every airplane window is oval? If you ever see a square window on a jet... RUN.",
        "beats": [
            {
                "beat_name": "THE PARADOX HOOK",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "NEUTRAL", "mouth_expression": "SPEAKING", "arm_pose": "POINT_RIGHT", "brow_angle": -5.0, "sweat_drop": False},
                "narration": "In 1954, the world's most luxurious jetliner, the De Havilland Comet, suddenly began falling out of the sky at cruising altitude. No one could figure out why.",
                "duration": 10.0,
                "prop_visual": "RETRO_AIRPLANE"
            },
            {
                "beat_name": "THE INVESTIGATION",
                "character_role": "ENGINEER",
                "character_state": {"eye_expression": "SKEPTICAL", "mouth_expression": "SPEAKING", "arm_pose": "IDLE", "brow_angle": 10.0, "sweat_drop": False},
                "narration": "Investigators submerged an entire passenger plane inside a giant water tank and pressurized the cabin over and over again until the metal ruptured.",
                "duration": 11.0,
                "prop_visual": "WATER_TANK_TEST"
            },
            {
                "beat_name": "THE SCIENTIFIC DISCOVERY",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "WIDE_SHOCK", "mouth_expression": "OPEN_O", "arm_pose": "SHOCKED_HANDS", "brow_angle": 18.0, "sweat_drop": True},
                "narration": "The culprit? Square windows! Pressure naturally flows around curved edges. But sharp 90-degree corners concentrate mechanical stress by over 300 percent, causing microscopic cracks to rip the fuselage apart!",
                "duration": 13.0,
                "prop_visual": "CORNER_STRESS_DIAGRAM"
            },
            {
                "beat_name": "THE SNAPPY LESSON",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "JOY_ARC", "mouth_expression": "SMILE", "arm_pose": "POINT_RIGHT", "brow_angle": -5.0, "sweat_drop": False},
                "narration": "Engineers immediately rounded the corners, and flying became the safest way to travel on Earth. Curves literally save lives!",
                "duration": 11.0,
                "prop_visual": "OVAL_WINDOW_PLANE"
            }
        ],
        "tags": ["aviation", "airplanes", "engineering mystery", "science facts", "history", "ricksclips", "shorts"]
    },
    {
        "id": "ancient_dragon_urn",
        "title": "The 1,800-Year-Old Jar That Caught Earthquakes",
        "youtube_title": "The Ancient Urn That Warned an Empire! 🐉🏺 #Shorts #History",
        "hook_line": "In 132 AD, an ancient scientist heard a metallic clink that saved an entire empire.",
        "beats": [
            {
                "beat_name": "THE PARADOX HOOK",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "NEUTRAL", "mouth_expression": "SPEAKING", "arm_pose": "POINT_RIGHT", "brow_angle": -5.0, "sweat_drop": False},
                "narration": "In ancient China, court advisors mocked inventor Zhang Heng when he brought a giant bronze vase covered in eight dragons into the emperor's palace.",
                "duration": 10.0,
                "prop_visual": "BRONZE_DRAGON_URN"
            },
            {
                "beat_name": "THE RIDICULE",
                "character_role": "BOSS",
                "character_state": {"eye_expression": "SKEPTICAL", "mouth_expression": "SPEAKING", "arm_pose": "IDLE", "brow_angle": -15.0, "sweat_drop": False},
                "narration": "One quiet morning, a loud CLANG rang out as the northwest dragon dropped a bronze ball into a toad's mouth. The advisors laughed: 'The ground didn't even shake!'",
                "duration": 11.0,
                "prop_visual": "DRAGON_BALL_DROP"
            },
            {
                "beat_name": "THE DISCOVERY",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "WIDE_SHOCK", "mouth_expression": "OPEN_O", "arm_pose": "SHOCKED_HANDS", "brow_angle": 18.0, "sweat_drop": True},
                "narration": "Three days later, exhausted messengers arrived on horseback. A devastating earthquake had struck Longxi—400 miles away to the exact northwest! Inside the jar, an inverted pendulum had detected seismic shockwaves before any human could feel them!",
                "duration": 13.0,
                "prop_visual": "SEISMIC_PENDULUM"
            },
            {
                "beat_name": "THE SNAPPY LESSON",
                "character_role": "NARRATOR",
                "character_state": {"eye_expression": "JOY_ARC", "mouth_expression": "SMILE", "arm_pose": "POINT_RIGHT", "brow_angle": -5.0, "sweat_drop": False},
                "narration": "It was the world's very first seismoscope, built over 1,700 years before modern earthquake sensors. Talk about legendary engineering!",
                "duration": 11.0,
                "prop_visual": "ANCIENT_INVENTION"
            }
        ],
        "tags": ["ancient history", "earthquake", "inventions", "science", "china", "legendary", "ricksclips", "shorts"]
    }
]

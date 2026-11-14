#!/usr/bin/env python3
"""
CHARACTER BIBLE (Lalafun / Studio Production Standard)
Defines recurring characters with fixed silhouettes, color palettes, eye styles,
and standardized facial expressions/phonemes to prevent character drift.
"""

# ==========================================
# 1. COLOR PALETTES & ATTRIBUTES
# ==========================================
CHARACTERS = {
    "LEO_THE_BEAR": {
        "name": "Leo the Bear",
        "role": "Playful Leader & Big Brother",
        "personality": "Energetic, kind, loves dancing and honey treats",
        "colors": {
            "fur_base": (255, 179, 71),       # Warm Honey Amber (#FFB347)
            "fur_shadow": (230, 138, 34),     # Deep Caramel Outline
            "snout_belly": (255, 245, 230),   # Warm Ivory (#FFF5E6)
            "inner_ear": (255, 182, 193),     # Soft Baby Pink
            "outfit_primary": (74, 144, 226), # Sky Blue Dungarees (#4A90E2)
            "outfit_accent": (255, 221, 89),  # Sunshine Yellow Buttons
            "eyes": (45, 30, 20),             # Deep Espresso Brown
            "nose": (50, 35, 25),             # Dark Chocolate
            "blush": (255, 138, 128, 175)     # Rosy Coral Blush
        },
        "proportions": {
            "head_to_body_ratio": 1.15,       # Chibi / Kawaii toddler proportions
            "ear_size_ratio": 0.32,
            "eye_spacing": 0.44,              # Distance between eyes relative to head width
            "snout_offset_y": 0.12            # Slightly low snout for cute baby look
        }
    },
    "LALA_THE_BUNNY": {
        "name": "Lala the Bunny",
        "role": "Sweet Singer & Music Lover",
        "personality": "Gentle, imaginative, loves singing nursery rhymes",
        "colors": {
            "fur_base": (253, 246, 240),      # Soft Powder White (#FDF6F0)
            "fur_shadow": (224, 210, 200),    # Soft Dove Grey Outline
            "snout_belly": (255, 255, 255),   # Pure Snow White
            "inner_ear": (248, 187, 208),     # Pastel Bubblegum Pink
            "outfit_primary": (255, 148, 194),# Strawberry Milk Dress (#FF94C2)
            "outfit_accent": (255, 255, 255), # White Polka Dots
            "eyes": (55, 45, 60),             # Deep Plum
            "nose": (255, 128, 171),          # Strawberry Pink
            "blush": (255, 128, 171, 160)     # Sweet Pink Blush
        },
        "proportions": {
            "head_to_body_ratio": 1.10,
            "ear_length_ratio": 0.85,         # Tall floppy bunny ears
            "eye_spacing": 0.46,
            "snout_offset_y": 0.10
        }
    },
    "PIP_THE_DUCKLING": {
        "name": "Pip the Duckling",
        "role": "Curious Toddler & Comic Relief",
        "personality": "Wobbly, enthusiastic, loves splashing and making funny sounds",
        "colors": {
            "fur_base": (255, 235, 59),       # Bright Lemon Yellow (#FFEB3B)
            "fur_shadow": (245, 124, 0),      # Tangerine Outline
            "snout_belly": (255, 249, 196),   # Pale Lemon Tummy
            "inner_ear": (255, 235, 59),
            "outfit_primary": (0, 188, 212),  # Turquoise Sailor Bow (#00BCD4)
            "outfit_accent": (255, 255, 255), # Sailor Stripes
            "eyes": (33, 33, 33),             # Charcoal Black
            "nose": (255, 112, 67),           # Orange Beak
            "blush": (255, 138, 101, 180)     # Peach Blush
        },
        "proportions": {
            "head_to_body_ratio": 1.25,       # Extra chubby baby proportions
            "eye_spacing": 0.48,
            "snout_offset_y": 0.14
        }
    }
}

# ==========================================
# 2. STANDARDIZED PHONEMES & EXPRESSIONS
# ==========================================
# 6 Fixed Facial Expressions / Mouth Shapes for Lip Sync
EXPRESSIONS = {
    "REST": {
        "description": "Closed friendly resting smile",
        "mouth_open": 0.0,
        "mouth_width": 1.0,
        "eye_scale_y": 1.0
    },
    "A_PHONEME": {
        "description": "Wide open singing mouth for vowels 'Ah', 'Ha', 'Star'",
        "mouth_open": 0.85,
        "mouth_width": 1.15,
        "eye_scale_y": 0.95
    },
    "O_PHONEME": {
        "description": "Rounded O shape for 'Oh', 'You', 'Round', 'Moon'",
        "mouth_open": 0.70,
        "mouth_width": 0.65,
        "eye_scale_y": 1.05
    },
    "E_PHONEME": {
        "description": "Wide smiling teeth/mouth for 'Ee', 'Me', 'Beep'",
        "mouth_open": 0.35,
        "mouth_width": 1.30,
        "eye_scale_y": 0.90
    },
    "BLINK": {
        "description": "Eyes completely closed during natural blinking cycle",
        "mouth_open": 0.15,
        "mouth_width": 1.0,
        "eye_scale_y": 0.05
    },
    "JOY_SMILE": {
        "description": "Curved happy arc eyes (^^) during joyful chorus",
        "mouth_open": 0.60,
        "mouth_width": 1.20,
        "eye_scale_y": -1.0  # Inverted arc flag
    }
}

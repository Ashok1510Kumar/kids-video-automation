#!/usr/bin/env python3
"""
STORY CATALOG (Lalafun / Cocomelon Episodic Narrative Engine)
Defines 3-Act narrative story episodes with characters, dialogue, dramatic tension,
mystery discoveries, sound effect cues, and joyful resolutions.
"""

EPISODES = [
    {
        "id": "mystery_egg",
        "title": "🥚 Leo and the Mystery Golden Egg!",
        "youtube_title": "Leo and the Mystery Golden Egg! 🥚✨ Kids Storytime #Shorts",
        "hook": "What is inside the giant golden egg?!",
        "acts": [
            {
                "act_name": "ACT 1: THE DISCOVERY",
                "scene_type": "GARDEN_DISCOVERY",
                "narration": "One sunny morning, Leo the little bear was exploring the flower garden, when suddenly... he stopped! Right in the green grass was a giant, glowing golden egg! 'Whoa!' whispered Leo. 'Where did this come from?'",
                "duration": 14.0,
                "character_emotion": "CURIOUS",
                "prop": "GOLDEN_EGG",
                "sfx": ["sfx_sparkle.wav", "sfx_pop.wav"]
            },
            {
                "act_name": "ACT 2: THE WOBBLING MYSTERY",
                "scene_type": "SUSPENSE_CLOSEUP",
                "narration": "Leo walked closer on tiptoe. Shhh! Suddenly, the egg began to WOBBLE! Wiggle, wobble, wiggle, wobble! CRACK! A little crack appeared right down the middle! 'Oh my goodness!' gasped Leo. 'Something is trying to get out!'",
                "duration": 15.0,
                "character_emotion": "SURPRISED",
                "prop": "CRACKING_EGG",
                "sfx": ["sfx_boing.wav", "sfx_pop.wav"]
            },
            {
                "act_name": "ACT 3: THE MAGICAL REVEAL & FRIENDSHIP",
                "scene_type": "CELEBRATION_DANCE",
                "narration": "POP! Out leaped a tiny baby glitter dragon with sparkly purple wings! It sneezed: ACHOO! and blew magical rainbow sparkles all over Leo's nose! Leo giggled with joy and gave his sweet new friend a gentle bear hug. Best friends forever!",
                "duration": 16.0,
                "character_emotion": "JOYFUL_DANCE",
                "prop": "BABY_DRAGON_SPARKLES",
                "sfx": ["sfx_sparkle.wav", "sfx_boing.wav", "sfx_fanfare.wav"]
            }
        ],
        "tags": ["kids story", "leo the bear", "mystery egg", "bedtime story", "toddler cartoon", "lalafun", "cocomelon", "shorts"]
    },
    {
        "id": "lost_star",
        "title": "⭐ The Little Star That Lost Its Way!",
        "youtube_title": "The Little Star That Fell From the Sky! ⭐🚀 Kids Cartoon Story #Shorts",
        "hook": "Can Leo help the little star fly back home?",
        "acts": [
            {
                "act_name": "ACT 1: THE FALLEN STAR",
                "scene_type": "GARDEN_DISCOVERY",
                "narration": "As the sun began to set, Leo saw a warm golden glow behind the sunflower bush. It wasn't a firefly... it was a real, baby star sitting on a leaf, sniffling softly! 'Don't cry, little star,' said Leo kindly. 'I'll help you get home!'",
                "duration": 14.0,
                "character_emotion": "CURIOUS",
                "prop": "BABY_STAR",
                "sfx": ["sfx_sparkle.wav"]
            },
            {
                "act_name": "ACT 2: THE BALLOON ROCKET",
                "scene_type": "SUSPENSE_CLOSEUP",
                "narration": "Leo had a brilliant idea! He gathered four giant, colorful helium balloons: red, blue, yellow, and green! He carefully tied them to the star. 'Hold on tight!' called Leo. Three... two... one... LIFT OFF! The little star began to float higher and higher into the clouds!",
                "duration": 15.0,
                "character_emotion": "SURPRISED",
                "prop": "BALLOON_STAR",
                "sfx": ["sfx_boing.wav", "sfx_sparkle.wav"]
            },
            {
                "act_name": "ACT 3: SAFE IN THE SKY",
                "scene_type": "CELEBRATION_DANCE",
                "narration": "WHOOSH! With a cheerful twinkle, the star zoomed back into space right beside the smiling Moon! It beamed brighter than ever and winked down at Leo: 'Thank you, Leo!' Leo waved goodbye happily. Sweet dreams, little star!",
                "duration": 16.0,
                "character_emotion": "JOYFUL_DANCE",
                "prop": "TWINKLE_MOON",
                "sfx": ["sfx_fanfare.wav", "sfx_sparkle.wav"]
            }
        ],
        "tags": ["bedtime story", "little star", "kids cartoon", "space for kids", "lalafun", "cocomelon", "shorts"]
    },
    {
        "id": "rainbow_cake",
        "title": "🎂 The Great Bouncy Rainbow Cake!",
        "youtube_title": "The Bouncy Rainbow Cake Adventure! 🎂🌈 Kids Storytime #Shorts",
        "hook": "What happens when you add too much magic yeast?",
        "acts": [
            {
                "act_name": "ACT 1: BAKING IN THE KITCHEN",
                "scene_type": "GARDEN_DISCOVERY",
                "narration": "Today was a very special day! Leo the bear put on his chef hat to bake a surprise Rainbow Birthday Cake for all his animal friends! He mixed strawberries, sweet honey, and blueberries in a big wooden bowl. Yummy!",
                "duration": 14.0,
                "character_emotion": "CURIOUS",
                "prop": "CHEF_BOWL",
                "sfx": ["sfx_pop.wav", "sfx_sparkle.wav"]
            },
            {
                "act_name": "ACT 2: IT'S GROWING!",
                "scene_type": "SUSPENSE_CLOSEUP",
                "narration": "Leo added a tiny pinch of magic baking powder. But UH-OH! The cake began to rumble! Gurgle, gurgle, PUFF! The cake started growing bigger, and bigger, and BIGGER until it was as tall as a house! 'Whoa!' cried Leo, jumping back in surprise!",
                "duration": 15.0,
                "character_emotion": "SURPRISED",
                "prop": "GIANT_CAKE",
                "sfx": ["sfx_boing.wav", "sfx_pop.wav"]
            },
            {
                "act_name": "ACT 3: THE BOUNCY TRAMPOLINE PARTY",
                "scene_type": "CELEBRATION_DANCE",
                "narration": "BOING! Leo touched the giant frosted cake, and it bounced like a giant trampoline! All his friends came running and hopped onto the fluffy strawberry frosting, bouncing up into the rainbow clouds and catching delicious treats in the air! What a magical day!",
                "duration": 16.0,
                "character_emotion": "JOYFUL_DANCE",
                "prop": "CAKE_PARTY",
                "sfx": ["sfx_boing.wav", "sfx_fanfare.wav", "sfx_sparkle.wav"]
            }
        ],
        "tags": ["baking cartoon", "funny kids story", "rainbow cake", "children storytime", "lalafun", "cocomelon", "shorts"]
    }
]

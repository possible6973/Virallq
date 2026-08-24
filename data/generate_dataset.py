import pandas as pd
import numpy as np
import random
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.feature_extraction import extract_script_features, FEATURE_NAMES

HOOK_TEMPLATES_HIGH = [
    "Stop scrolling if you have {amount} budget and want {benefit}!",
    "Here are 3 secret AI tools that feel illegal to know in 2026!",
    "90% of people make this 1 huge mistake with their {topic}!",
    "Eating {food} every morning? You might be stopping your weight loss!",
    "How I built a {business} brand with ₹0 in inventory costs!",
    "The {rule} budgeting rule is failing in 2026, do this instead!",
    "Secret real estate trick developers don't want you to know!"
]

HOOK_TEMPLATES_LOW = [
    "Hello guys welcome back to my channel today we will talk about {topic}.",
    "Today I am sharing some random tips on how to improve your life.",
    "This is a flat in city center call for details.",
    "Just another day working on projects and drinking coffee.",
    "Hey friends check out this new app I downloaded yesterday."
]

BODY_TEMPLATES_HIGH = [
    "Look at this luxury setup with modular kitchen and balcony. Located 10 mins from IT park. Comment 'HOME' below and I will DM you the direct tour!",
    "Number 1 tool generates pitch decks in 30 seconds. Number 2 creates realistic AI voices. Comment 'AI' for direct links sent to your inbox!",
    "Instead of 50/30/20, use 40% for essentials, 30% invested immediately, and 30% for skills. Save this reel and share with a friend!",
    "Swap instant oats for 3 whole eggs with spinach. This keeps hunger suppressed for 5 hours. Double tap if you want the 7-day meal plan!"
]

BODY_TEMPLATES_LOW = [
    "It has nice rooms and good lighting. Hope you guys like it. Let me know what you think.",
    "It is very important to manage your time and work hard every day. Subscribe for more videos.",
    "Thank you for watching this video. Do not forget to like and share if you enjoyed it."
]

def generate_synthetic_dataset(num_samples: int = 600, output_path: str = "data/datasets/reel_dataset.csv"):
    np.random.seed(42)
    random.seed(42)
    
    rows = []
    
    for i in range(num_samples):
        is_high = (i % 2 == 0) # Balanced 50/50 dataset
        
        if is_high:
            hook = random.choice(HOOK_TEMPLATES_HIGH).format(
                amount="₹50 Lakhs", benefit="a dream home", topic="resume", food="oats",
                business="Shopify", rule="50/30/20"
            )
            body = random.choice(BODY_TEMPLATES_HIGH)
            script_text = f"{hook}\n{body}"
            # High viral potential label (1)
            target_score = random.uniform(80.0, 98.0)
            viral_label = 1
        else:
            hook = random.choice(HOOK_TEMPLATES_LOW).format(topic="real estate")
            body = random.choice(BODY_TEMPLATES_LOW)
            script_text = f"{hook}\n{body}"
            # Lower viral potential label (0)
            target_score = random.uniform(40.0, 74.0)
            viral_label = 0
            
        feats = extract_script_features(script_text, target_duration=30)
        feats['script_text'] = script_text
        feats['target_score'] = round(target_score, 2)
        feats['viral_label'] = viral_label
        rows.append(feats)
        
    df = pd.DataFrame(rows)
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    print(f"Generated benchmark dataset with {len(df)} samples at: {out_file}")
    return df

if __name__ == "__main__":
    generate_synthetic_dataset()

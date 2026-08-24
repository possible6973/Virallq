import sys
import os
from pathlib import Path

# Ensure root directory in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from database.crud import add_viral_script, get_all_viral_scripts
from database.models import ViralScript

SEED_VIRAL_SCRIPTS = [
    {
        "category": "Real Estate",
        "topic": "50 Lakh Budget 2BHK Home Tour",
        "audience": "First-time home buyers in urban India",
        "hook": "Stop scrolling if you have 50 Lakhs budget and want a dream home!",
        "script_text": (
            "Stop scrolling if you have 50 Lakhs budget and want a dream home! "
            "Today we are inside a 2BHK luxury flat with a private balcony and modular kitchen. "
            "Look at this wooden flooring in the master bedroom, and the building includes a rooftop gym! "
            "Located just 10 mins from the IT park. Most people think 50 Lakhs gets you nothing in 2026, "
            "but this developer is giving 0% brokerage for the next 5 buyers! "
            "Comment 'HOME' below and I will DM you the direct location and virtual tour video immediately!"
        ),
        "duration": 30,
        "views": 1450000,
        "likes": 98000,
        "comments": 4200,
        "shares": 15600,
        "engagement_rate": 8.1,
        "performance_label": "High Potential"
    },
    {
        "category": "Real Estate",
        "topic": "Rental Yield vs Capital Growth Formula",
        "audience": "Real estate investors & NRI buyers",
        "hook": "99% of people buy real estate for the wrong reasons. Here is the math!",
        "script_text": (
            "99% of people buy real estate for the wrong reasons. Here is the math! "
            "Residential apartments give only 3% rental yield, while commercial shop plots yield 8% to 11%. "
            "If your goal is monthly cash flow, buy commercial assets near upcoming metro lines. "
            "If your goal is 10-year wealth multiplication, buy land parcels in satellite growth corridors. "
            "Comment 'INVEST' for our free real estate yield calculator sheet!"
        ),
        "duration": 35,
        "views": 890000,
        "likes": 64000,
        "comments": 2100,
        "shares": 11200,
        "engagement_rate": 8.7,
        "performance_label": "High Potential"
    },
    {
        "category": "Finance & Wealth",
        "topic": "Salary Distribution Rule (50/30/20 Myth)",
        "audience": "Young professionals and salaried employees",
        "hook": "The 50/30/20 budgeting rule is failing in 2026, do this instead!",
        "script_text": (
            "The 50/30/20 budgeting rule is failing in 2026, do this instead! "
            "If you earn ₹60,000 per month, inflation will eat 60% of your paycheck in rent and food alone. "
            "Here is the modified 40-30-30 breakdown smart investors use: "
            "40% for essentials, 30% invested immediately in index funds before spending, and 30% for skill development and lifestyle. "
            "Save this reel before your next salary credit date and share with a friend who needs financial clarity!"
        ),
        "duration": 35,
        "views": 2100000,
        "likes": 185000,
        "comments": 6300,
        "shares": 34000,
        "engagement_rate": 10.7,
        "performance_label": "High Potential"
    },
    {
        "category": "Finance & Wealth",
        "topic": "Credit Card Points Flying Free Strategy",
        "audience": "Travel enthusiasts and cardholders",
        "hook": "How I booked a ₹1.5 Lakh business class flight for just ₹900!",
        "script_text": (
            "How I booked a ₹1.5 Lakh business class flight for just ₹900! "
            "Stop redeeming credit card reward points for cheap toaster gadgets! "
            "Transfer your HDFC or Axis points directly to Singapore Airlines or Vistara KrisFlyer at a 1:1 ratio. "
            "1 point = ₹1.50 value when redeemed for flights instead of 25 paise on gift vouchers. "
            "Comment 'FLY' to get my complete credit card point optimizer guide!"
        ),
        "duration": 30,
        "views": 1750000,
        "likes": 145000,
        "comments": 7800,
        "shares": 38000,
        "engagement_rate": 10.9,
        "performance_label": "High Potential"
    },
    {
        "category": "Tech & AI",
        "topic": "3 AI Tools That Feel Illegal to Know",
        "audience": "Students, freelancers, and content creators",
        "hook": "Here are 3 secret AI tools that will double your productivity in 5 minutes!",
        "script_text": (
            "Here are 3 secret AI tools that will double your productivity in 5 minutes! "
            "Number 1: Gamma App — converts your text notes into stunning pitch decks in 30 seconds. "
            "Number 2: ElevenLabs — generates human-like AI voiceovers in any language. "
            "Number 3: ViralIQ — predicts reel virality score before you hit publish! "
            "Which one will you try first? Comment 'AI' for the exact direct links sent to your inbox!"
        ),
        "duration": 28,
        "views": 3200000,
        "likes": 290000,
        "comments": 12000,
        "shares": 89000,
        "engagement_rate": 12.2,
        "performance_label": "High Potential"
    },
    {
        "category": "Tech & AI",
        "topic": "ChatGPT Prompt Engineering Secret",
        "audience": "Developers & AI users",
        "hook": "Stop writing bad prompts! Use this 1 master formula instead.",
        "script_text": (
            "Stop writing bad prompts! Use this 1 master formula instead. "
            "Don't just type 'Write a blog post'. "
            "Use: [Role] + [Context] + [Specific Task] + [Format Constraint] + [Tone]. "
            "Example: 'Act as a senior copywriter. I am launching a SaaS app for creators. Write 3 short email headers under 8 words.' "
            "Comment 'PROMPT' for my 50+ copy-paste master prompts library!"
        ),
        "duration": 30,
        "views": 2400000,
        "likes": 198000,
        "comments": 8900,
        "shares": 47000,
        "engagement_rate": 10.5,
        "performance_label": "High Potential"
    },
    {
        "category": "Fitness & Health",
        "topic": "Fat Loss Breakfast Swap Secret",
        "audience": "Fitness enthusiasts & weight loss seekers",
        "hook": "Eating oats for breakfast every morning? You might be stopping your fat loss!",
        "script_text": (
            "Eating oats for breakfast every morning? You might be stopping your fat loss! "
            "Instant oats spike your blood sugar faster than 2 slices of white bread. "
            "Instead, swap it for 3 whole eggs with spinach or a high-protein paneer scramble. "
            "This keeps your ghrelin hunger hormone suppressed for 5 hours straight. "
            "Double tap if you want a complete 7-day high-protein Indian breakfast plan!"
        ),
        "duration": 25,
        "views": 980000,
        "likes": 67000,
        "comments": 1800,
        "shares": 9400,
        "engagement_rate": 8.0,
        "performance_label": "High Potential"
    },
    {
        "category": "E-commerce & Business",
        "topic": "Zero Investment Dropshipping Store",
        "audience": "Aspiring entrepreneurs",
        "hook": "How I started a print-on-demand brand with ₹0 in inventory costs!",
        "script_text": (
            "How I started a print-on-demand brand with ₹0 in inventory costs! "
            "Step 1: Design viral quotes on Canva for free. "
            "Step 2: Connect Printrove to a free Shopify trial. "
            "Step 3: Post organic Instagram Reels showing aesthetic mockup videos. "
            "When a customer orders, Printrove prints and ships it directly, while you keep the profit margin! "
            "Comment 'BIZ' to get my step-by-step supplier checklist!"
        ),
        "duration": 40,
        "views": 1800000,
        "likes": 142000,
        "comments": 8900,
        "shares": 27000,
        "engagement_rate": 9.8,
        "performance_label": "High Potential"
    },
    {
        "category": "Education & Career",
        "topic": "Resume Bullet Points Formula",
        "audience": "Job seekers & college students",
        "hook": "90% of resumes get rejected by ATS because of this 1 huge mistake!",
        "script_text": (
            "90% of resumes get rejected by ATS because of this 1 huge mistake! "
            "You write: 'Managed social media accounts'. "
            "Recruiters want: 'Increased organic reel reach by 240% in 90 days resulting in 500+ inbound leads'. "
            "Use the Action + Metric + Result formula for every single bullet point. "
            "Save this video right now and rewrite your resume before applying to your next job!"
        ),
        "duration": 32,
        "views": 2500000,
        "likes": 210000,
        "comments": 4500,
        "shares": 52000,
        "engagement_rate": 10.6,
        "performance_label": "High Potential"
    }
]

def seed_database():
    init_db()
    existing = get_all_viral_scripts()
    if len(existing) < len(SEED_VIRAL_SCRIPTS):
        print("Seeding database with expanded viral script library records...")
        for item in SEED_VIRAL_SCRIPTS:
            vs = ViralScript(
                id=None,
                category=item["category"],
                topic=item["topic"],
                audience=item["audience"],
                hook=item["hook"],
                script_text=item["script_text"],
                duration=item["duration"],
                views=item["views"],
                likes=item["likes"],
                comments=item["comments"],
                shares=item["shares"],
                engagement_rate=item["engagement_rate"],
                performance_label=item["performance_label"]
            )
            add_viral_script(vs)
        print(f"Successfully seeded expanded viral scripts into SQLite!")
    else:
        print(f"Database contains {len(existing)} viral scripts.")

if __name__ == "__main__":
    seed_database()

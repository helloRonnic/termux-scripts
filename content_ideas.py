# content_ideas.py — Script #2
# What this does:
# → Reads your latest trend report from trending_prompts.py
# → Extracts the top repos, models, and tags
# → Generates ready-to-use content ideas for YouTube, Instagram, Newsletter
# → Saves everything to a dated content calendar file
# No extra libraries needed — uses only what's already installed

import os
import glob
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# STEP 1 — FIND THE LATEST TREND REPORT
# Automatically finds the most recent file
# so you never have to type the filename
# ─────────────────────────────────────────

def find_latest_report():
    # Look for all files matching the pattern prompts_YYYY-MM-DD.txt
    files = glob.glob("/data/data/com.termux/files/home/scripts/prompts_*.txt")

    if not files:
        return None, None

    # Sort by date in filename — most recent last
    files.sort()
    latest = files[-1]

    # Extract the date from the filename
    basename = os.path.basename(latest)
    date_str = basename.replace("prompts_", "").replace(".txt", "")

    return latest, date_str

# ─────────────────────────────────────────
# STEP 2 — PARSE THE TREND REPORT
# Reads the .txt file and extracts:
# → Top repo names and descriptions
# → Top model names
# → Trending tags
# ─────────────────────────────────────────

def parse_trend_report(filepath):
    repos = []
    models = []
    tags = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_section = None

        for line in lines:
            line = line.strip()

            # Detect which section we are in
            if "GITHUB — TOP AI PROMPT" in line:
                current_section = "repos"
            elif "HUGGING FACE — TRENDING" in line:
                current_section = "models"
            elif "TRENDING STYLE TAGS" in line:
                current_section = "tags"
            elif "CONTENT IDEAS" in line:
                current_section = None

            # Extract repo names (lines starting with a number and have stars)
            if current_section == "repos":
                if line.startswith("About  :") and line != "About  :":
                    desc = line.replace("About  :", "").strip()
                    if desc and len(desc) > 10:
                        repos.append(desc)

            # Extract model names
            if current_section == "models":
                if "/" in line and "likes" not in line and "Downloads" not in line:
                    if not line.startswith("→") and not line.startswith("["):
                        models.append(line.strip())

            # Extract tags (lines starting with #)
            if current_section == "tags":
                if line.startswith("#"):
                    tag = line.split()[0].replace("#", "")
                    if tag:
                        tags.append(tag)

    except Exception as e:
        print(f"  ❌ Error reading report: {e}")

    return repos[:8], models[:8], tags[:10]

# ─────────────────────────────────────────
# STEP 3 — GENERATE CONTENT IDEAS
# Takes extracted data and builds
# platform-specific content ideas
# ─────────────────────────────────────────

def generate_ideas(repos, models, tags, report_date):

    ideas = {
        "youtube_titles": [],
        "instagram_hooks": [],
        "newsletter_subjects": [],
        "weekly_calendar": []
    }

    # ── YouTube Title Templates ──
    # These are proven title formats for AI content

    if models:
        ideas["youtube_titles"].extend([
            f"I Tested {models[0].split('/')[-1]} — The Most Downloaded AI Model Right Now",
            f"Why Everyone Is Switching To {models[0].split('/')[-1]} (Honest Review)",
            f"{models[0].split('/')[-1]} vs {models[1].split('/')[-1] if len(models) > 1 else 'Midjourney'} — Which Is Better?",
        ])

    if tags:
        ideas["youtube_titles"].extend([
            f"The Best #{tags[0].replace('-', ' ').title()} AI Prompts That Actually Work",
            f"How To Use {tags[1].replace('-', ' ').title() if len(tags) > 1 else 'AI Prompts'} To Create Viral Content",
            f"I Made 100 AI Images Using Only #{tags[0].replace('-', ' ').title()} — Here's What Happened",
        ])

    if repos:
        ideas["youtube_titles"].extend([
            f"This Free GitHub Repo Has 10,000+ AI Prompts (Most People Don't Know It Exists)",
            f"I Tried Every Prompt From The Most Starred AI Repo On GitHub",
        ])

    # ── Instagram Carousel Hooks ──
    # First line is the hook — must stop the scroll

    if models:
        ideas["instagram_hooks"].extend([
            f"🔥 The #1 most downloaded AI image model has {models[0].split('/')[-1]} — here's why creators love it (swipe for prompts)",
            f"Stop using basic prompts. These {models[0].split('/')[-1]} prompts went viral this week 👇",
            f"AI creators are switching to {models[0].split('/')[-1]}. Here's what changed (and the exact prompts to try)",
        ])

    if tags:
        ideas["instagram_hooks"].extend([
            f"#{tags[0].replace('-', ' ')} is trending in AI art right now. Here are 5 prompts you can steal today 🎨",
            f"If you're making AI content and not using #{tags[1].replace('-', ' ') if len(tags) > 1 else tags[0].replace('-', ' ')} prompts, you're leaving views on the table",
        ])

    # ── Newsletter Subject Lines ──
    # Short, curiosity-driven, feel personal

    if models and tags:
        ideas["newsletter_subjects"].extend([
            f"The AI model with 1M+ downloads (and how to use it)",
            f"This week's trending AI prompts — {len(tags)} styles worth trying",
            f"What's actually working in AI art this week",
            f"{models[0].split('/')[-1]} is everywhere. Here's my honest take.",
        ])

    # ── 7-Day Content Calendar ──
    # One post idea per day, starting tomorrow

    today = datetime.now()
    calendar_items = []

    post_ideas = []

    if models:
        post_ideas.append({
            "platform": "YouTube Short",
            "idea": f"Quick demo: Generate an image using {models[0].split('/')[-1]} with a simple prompt"
        })
        post_ideas.append({
            "platform": "Instagram Reel",
            "idea": f"Before/after: Basic prompt vs optimised {models[0].split('/')[-1]} prompt — show the difference"
        })

    if tags:
        post_ideas.append({
            "platform": "Instagram Carousel",
            "idea": f"5 trending #{tags[0].replace('-', ' ')} prompts with example images — slide format"
        })
        post_ideas.append({
            "platform": "YouTube Video",
            "idea": f"Full tutorial: How to use #{tags[0].replace('-', ' ')} style in AI image generation"
        })

    post_ideas.append({
        "platform": "Newsletter",
        "idea": "Weekly roundup: Top 3 trending models + 5 prompts to try this weekend"
    })

    post_ideas.append({
        "platform": "Instagram Post",
        "idea": "Poll: Which AI image model do you use most? (engagement booster)"
    })

    post_ideas.append({
        "platform": "YouTube Short",
        "idea": "I found a GitHub repo with 10,000+ free AI prompts — here's the link"
    })

    # Assign a day to each idea
    for i, item in enumerate(post_ideas[:7]):
        post_day = today + timedelta(days=i+1)
        calendar_items.append({
            "date": post_day.strftime("%A, %b %d"),
            "platform": item["platform"],
            "idea": item["idea"]
        })

    ideas["weekly_calendar"] = calendar_items

    return ideas

# ─────────────────────────────────────────
# STEP 4 — SAVE TO FILE
# ─────────────────────────────────────────

def save_ideas(ideas, report_date):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"content_ideas_{today}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"CONTENT IDEAS REPORT\n")
        f.write(f"Generated : {today}\n")
        f.write(f"Based on  : Trend report from {report_date}\n")
        f.write("=" * 55 + "\n\n")

        # YouTube Titles
        f.write("[ 1. YOUTUBE TITLES — READY TO USE ]\n")
        f.write("Copy any of these directly into YouTube Studio\n")
        f.write("-" * 50 + "\n\n")
        for i, title in enumerate(ideas["youtube_titles"], 1):
            f.write(f"{i}. {title}\n\n")

        # Instagram Hooks
        f.write("\n[ 2. INSTAGRAM CAROUSEL HOOKS ]\n")
        f.write("Use as first slide text — designed to stop the scroll\n")
        f.write("-" * 50 + "\n\n")
        for i, hook in enumerate(ideas["instagram_hooks"], 1):
            f.write(f"{i}. {hook}\n\n")

        # Newsletter Subjects
        f.write("\n[ 3. NEWSLETTER SUBJECT LINES ]\n")
        f.write("Paste directly into your email platform\n")
        f.write("-" * 50 + "\n\n")
        for i, subject in enumerate(ideas["newsletter_subjects"], 1):
            f.write(f"{i}. {subject}\n\n")

        # Weekly Calendar
        f.write("\n[ 4. YOUR 7-DAY CONTENT CALENDAR ]\n")
        f.write("One post per day — all based on today's trends\n")
        f.write("-" * 50 + "\n\n")
        for item in ideas["weekly_calendar"]:
            f.write(f"  {item['date']}\n")
            f.write(f"  Platform : {item['platform']}\n")
            f.write(f"  Idea     : {item['idea']}\n\n")

        # Quick action
        f.write("\n" + "=" * 55 + "\n")
        f.write("[ YOUR #1 PRIORITY TODAY ]\n")
        f.write("=" * 55 + "\n\n")
        if ideas["youtube_titles"]:
            f.write(f"Make this video FIRST — it uses today's top trend:\n\n")
            f.write(f"  → {ideas['youtube_titles'][0]}\n\n")
        f.write("Why: It uses the most downloaded AI model right now.\n")
        f.write("These videos get found by search for months after posting.\n")

    return filename

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("  CONTENT IDEA GENERATOR")
    print("  Reads your trend report → outputs content ideas")
    print("=" * 55 + "\n")

    # Find latest report
    filepath, report_date = find_latest_report()

    if not filepath:
        print("  ❌ No trend report found.")
        print("  → Run trending_prompts.py first, then try again\n")
        return

    print(f"  📄 Found trend report: prompts_{report_date}.txt")
    print(f"  📊 Extracting data...\n")

    # Parse it
    repos, models, tags = parse_trend_report(filepath)

    print(f"  ✅ Extracted:")
    print(f"     {len(repos)} repo descriptions")
    print(f"     {len(models)} trending models")
    print(f"     {len(tags)} style tags\n")

    if not models and not tags:
        print("  ⚠️  Could not extract enough data from report.")
        print("  → Try running trending_prompts.py again first\n")
        return

    # Generate ideas
    print("  💡 Generating content ideas...")
    ideas = generate_ideas(repos, models, tags, report_date)

    # Preview
    print("\n" + "=" * 55)
    print("  PREVIEW — TOP IDEAS")
    print("=" * 55)

    print("\n  🎬 TOP YOUTUBE TITLES:\n")
    for i, title in enumerate(ideas["youtube_titles"][:3], 1):
        print(f"  {i}. {title[:70]}...")

    print("\n  📅 THIS WEEK'S CALENDAR:\n")
    for item in ideas["weekly_calendar"][:3]:
        print(f"  {item['date']} → [{item['platform']}]")
        print(f"     {item['idea'][:60]}...\n")

    # Save
    filename = save_ideas(ideas, report_date)

    total_ideas = (len(ideas["youtube_titles"]) +
                   len(ideas["instagram_hooks"]) +
                   len(ideas["newsletter_subjects"]))

    print("=" * 55)
    print(f"  ✅ Generated {total_ideas} content ideas")
    print(f"  📄 Saved to: {filename}")
    print(f"  💡 Read it: cat {filename}")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    main()

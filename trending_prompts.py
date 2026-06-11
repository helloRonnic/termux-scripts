# trending_prompts.py — VERSION 3 (CONFIRMED WORKING SOURCES)
# Debug results showed:
# GitHub API   → 200 ✅ confirmed working
# HuggingFace  → fixed wrong parameter (was "trending", now "likes")
#
# What this gives you:
# → Top starred AI prompt repositories = real prompts the community loves
# → Trending text-to-image models = what tools/styles are hot right now
# → Trending tags from the AI art community = YouTube/Instagram topic ideas

import requests
from datetime import datetime
from collections import Counter

# ─────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────

# We search GitHub for these topics — all return prompt-rich repos
GITHUB_SEARCHES = [
    "midjourney prompts",
    "stable diffusion prompts",
    "AI image prompts",
    "leonardo AI prompts"
]

# How many repos to grab per search
REPOS_PER_SEARCH = 5

# ─────────────────────────────────────────
# HEADERS
# These make our requests look like a real browser
# Without this, some APIs block us immediately
# ─────────────────────────────────────────

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
    "Accept": "application/json"
}

# ─────────────────────────────────────────
# SOURCE 1 — GITHUB API
# Confirmed working (200) from debug test
# Finds most-starred AI prompt repos
# Stars = community validation = these prompts WORK
# ─────────────────────────────────────────

def get_github_trending():
    all_results = []
    seen_repos = set()  # Prevents duplicate repos appearing twice

    for query in GITHUB_SEARCHES:
        url = "https://api.github.com/search/repositories"

        params = {
            "q": query,          # Search term
            "sort": "stars",     # Sort by most starred
            "order": "desc",     # Highest stars first
            "per_page": REPOS_PER_SEARCH
        }

        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=15)

            if response.status_code == 200:
                data = response.json()
                repos = data.get("items", [])

                for repo in repos:
                    repo_name = repo["full_name"]

                    # Skip if we already added this repo from another search
                    if repo_name in seen_repos:
                        continue
                    seen_repos.add(repo_name)

                    all_results.append({
                        "name": repo_name,
                        "description": repo.get("description") or "No description",
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "topics": repo.get("topics", []),
                        "url": repo.get("html_url", ""),
                        "search_query": query
                    })

            elif response.status_code == 403:
                print(f"  ⚠️  GitHub rate limit hit — waiting is needed")
                break

            else:
                print(f"  ⚠️  GitHub returned {response.status_code} for '{query}'")

        except requests.exceptions.ConnectionError:
            print("  ❌  No internet connection")
            return []

        except Exception as e:
            print(f"  ❌  GitHub error: {e}")

    # Sort all collected repos by stars — highest first
    all_results.sort(key=lambda x: x["stars"], reverse=True)

    # Return top 15 unique repos
    return all_results[:15]

# ─────────────────────────────────────────
# SOURCE 2 — HUGGING FACE API
# Fixed: "trending" was wrong, "likes" is correct
# Gets the most-liked text-to-image AI models
# These model names = content gold for your audience
# ─────────────────────────────────────────

def get_huggingface_models():
    url = "https://huggingface.co/api/models"

    params = {
        "sort": "likes",            # Fixed: was "trending" — now "likes" ✅
        "filter": "text-to-image",  # Only image generation models
        "limit": 12,
        "direction": -1             # Descending order
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)

        if response.status_code == 200:
            models = response.json()
            results = []

            for m in models:
                results.append({
                    "name": m.get("id", "Unknown"),
                    "likes": m.get("likes", 0),
                    "downloads": m.get("downloads", 0),
                    "tags": m.get("tags", [])
                })

            return results

        else:
            print(f"  ⚠️  HuggingFace returned {response.status_code}")
            return []

    except Exception as e:
        print(f"  ❌  HuggingFace error: {e}")
        return []

# ─────────────────────────────────────────
# EXTRACT TRENDING TAGS
# Collects all topic tags from GitHub repos
# Counts which ones appear most = trending styles
# ─────────────────────────────────────────

def extract_trending_tags(github_results):
    all_tags = []
    for repo in github_results:
        all_tags.extend(repo.get("topics", []))

    if not all_tags:
        return []

    # Count occurrences and return top 15
    tag_counts = Counter(all_tags)
    return tag_counts.most_common(15)

# ─────────────────────────────────────────
# SAVE TO FILE
# ─────────────────────────────────────────

def save_to_file(github_results, hf_results, trending_tags):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"prompts_{today}.txt"

    with open(filename, "w", encoding="utf-8") as f:

        f.write(f"TRENDING AI IMAGE PROMPTS REPORT\n")
        f.write(f"Date    : {today}\n")
        f.write(f"Sources : GitHub API + HuggingFace API\n")
        f.write("=" * 55 + "\n\n")

        # ── Section 1: GitHub Repos ──
        if github_results:
            f.write("[ 1. GITHUB — TOP AI PROMPT REPOSITORIES ]\n")
            f.write("Most-starred collections = community-validated prompts\n")
            f.write("-" * 50 + "\n\n")

            for i, repo in enumerate(github_results, 1):
                f.write(f"{i}. {repo['name']}\n")
                f.write(f"   About  : {repo['description']}\n")
                f.write(f"   Stars  : ⭐ {repo['stars']:,}\n")
                f.write(f"   Forks  : 🍴 {repo['forks']:,}\n")
                if repo['topics']:
                    f.write(f"   Tags   : {', '.join(repo['topics'][:6])}\n")
                f.write(f"   Browse : {repo['url']}\n")
                f.write("\n")

        # ── Section 2: HuggingFace Models ──
        if hf_results:
            f.write("\n[ 2. HUGGING FACE — TRENDING IMAGE AI MODELS ]\n")
            f.write("Most-liked models = what creators are using RIGHT NOW\n")
            f.write("Use these model names in your content titles\n")
            f.write("-" * 50 + "\n\n")

            for i, m in enumerate(hf_results, 1):
                f.write(f"{i}. {m['name']}\n")
                f.write(f"   Likes     : ❤️  {m['likes']:,}\n")
                f.write(f"   Downloads : 📥 {m['downloads']:,}\n\n")

        # ── Section 3: Trending Tags ──
        if trending_tags:
            f.write("\n[ 3. TRENDING STYLE TAGS — FROM AI ART COMMUNITY ]\n")
            f.write("These tags = what styles people are searching for\n")
            f.write("Each tag = one YouTube video or Instagram post idea\n")
            f.write("-" * 50 + "\n\n")

            for tag, count in trending_tags:
                bar = "█" * min(count * 3, 20)
                f.write(f"  #{tag:<25} {bar} ({count}x)\n")

        # ── Section 4: Content Ideas ──
        f.write("\n\n" + "=" * 55 + "\n")
        f.write("[ 4. CONTENT IDEAS — USE THESE RESULTS TODAY ]\n")
        f.write("=" * 55 + "\n\n")
        f.write("YOUTUBE IDEAS:\n")
        f.write("  → 'I tested the #1 most starred AI prompt repo'\n")
        f.write("  → 'Top 5 trending AI image models this week'\n")
        f.write("  → 'Best [tag] AI prompts — with examples'\n\n")
        f.write("INSTAGRAM IDEAS:\n")
        f.write("  → Carousel: '10 prompts from the most starred GitHub repo'\n")
        f.write("  → Reel: Before/after using a trending model\n")
        f.write("  → Story poll: 'Which AI model should I test next?'\n\n")
        f.write("NEWSLETTER IDEAS:\n")
        f.write("  → 'This week in AI art: top repos + trending models'\n")
        f.write("  → Curate 5 prompts from top GitHub repo + credit source\n\n")
        f.write("PRODUCT IDEAS:\n")
        f.write("  → PDF: 'Top 50 prompts from GitHub's most starred repos'\n")
        f.write("  → Sell this script on Gumroad: 'AI Trend Finder for Creators'\n")

    return filename

# ─────────────────────────────────────────
# MAIN — Runs everything in order
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("  TRENDING AI PROMPT FINDER v3")
    print("  GitHub ✅ + HuggingFace ✅ (Fixed)")
    print("=" * 55 + "\n")

    # ── Step 1: GitHub ──
    print("  🔍 Searching GitHub for trending prompt repos...")
    github_results = get_github_trending()

    if github_results:
        print(f"  ✅ Found {len(github_results)} unique prompt repositories\n")
    else:
        print("  ⚠️  GitHub returned nothing — check internet\n")

    # ── Step 2: HuggingFace ──
    print("  🔍 Fetching trending image models from HuggingFace...")
    hf_results = get_huggingface_models()

    if hf_results:
        print(f"  ✅ Found {len(hf_results)} trending text-to-image models\n")
    else:
        print("  ⚠️  HuggingFace returned nothing\n")

    # ── Step 3: Extract Tags ──
    trending_tags = extract_trending_tags(github_results)

    # ── Step 4: Preview ──
    if github_results or hf_results:

        print("=" * 55)
        print("  PREVIEW — TOP RESULTS")
        print("=" * 55)

        if github_results:
            print("\n  📌 TOP 5 TRENDING PROMPT REPOS:\n")
            for i, repo in enumerate(github_results[:5], 1):
                desc = repo['description']
                if len(desc) > 55:
                    desc = desc[:55] + "..."
                print(f"  {i}. ⭐{repo['stars']:,} — {repo['name']}")
                print(f"     {desc}\n")

        if hf_results:
            print("\n  🤖 TOP 5 TRENDING IMAGE MODELS:\n")
            for i, m in enumerate(hf_results[:5], 1):
                print(f"  {i}. {m['name']}")
                print(f"     ❤️  {m['likes']:,} likes  |  📥 {m['downloads']:,} downloads\n")

        if trending_tags:
            print("\n  🏷️  TOP TRENDING STYLE TAGS:\n")
            for tag, count in trending_tags[:8]:
                print(f"     #{tag}")

        # ── Save file ──
        filename = save_to_file(github_results, hf_results, trending_tags)
        total = len(github_results) + len(hf_results)

        print(f"\n" + "=" * 55)
        print(f"  ✅ DONE! {total} results collected and saved")
        print(f"  📄 File: {filename}")
        print(f"  💡 Read it: cat {filename}")
        print("=" * 55 + "\n")

    else:
        print("\n  ❌ No data collected. Check your internet.\n")

if __name__ == "__main__":
    main()

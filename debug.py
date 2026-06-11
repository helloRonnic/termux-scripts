# debug.py
# This tests 4 different sources and shows us exactly what each one returns
# Run this first — takes 30 seconds — then tell me what you see

import requests

headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"}

# ── TEST 1: Civitai ──
print("\n--- Testing Civitai ---")
try:
    r = requests.get(
        "https://civitai.com/api/v1/images",
        params={"limit": 3, "sort": "Most Reactions", "period": "Week", "nsfw": "None"},
        headers=headers,
        timeout=20
    )
    print(f"Status code : {r.status_code}")
    print(f"Response    : {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# ── TEST 2: Lexica ──
print("\n--- Testing Lexica ---")
try:
    r2 = requests.get(
        "https://lexica.art/api/v1/search",
        params={"q": "fantasy", "n": 3},
        headers=headers,
        timeout=15
    )
    print(f"Status code : {r2.status_code}")
    print(f"Response    : {r2.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# ── TEST 3: GitHub API (no key needed) ──
print("\n--- Testing GitHub API ---")
try:
    r3 = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": "midjourney prompts", "sort": "stars", "order": "desc"},
        headers=headers,
        timeout=15
    )
    print(f"Status code : {r3.status_code}")
    if r3.status_code == 200:
        data = r3.json()
        print(f"Total results: {data.get('total_count', 0)}")
        print(f"First result : {data['items'][0]['full_name'] if data.get('items') else 'none'}")
    else:
        print(f"Response: {r3.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# ── TEST 4: Hugging Face API (no key needed) ──
print("\n--- Testing Hugging Face ---")
try:
    r4 = requests.get(
        "https://huggingface.co/api/spaces",
        params={"sort": "trending", "limit": 5},
        headers=headers,
        timeout=15
    )
    print(f"Status code : {r4.status_code}")
    if r4.status_code == 200:
        data = r4.json()
        print(f"Got {len(data)} spaces")
        print(f"First space : {data[0].get('id', 'unknown') if data else 'none'}")
    else:
        print(f"Response: {r4.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Done. Paste all output above to Claude ---")

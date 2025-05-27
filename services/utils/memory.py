import json
import os

MEMORY_FILE = "data/memory/seen_urls.json"

def load_seen_urls():
    if not os.path.exists(MEMORY_FILE):
        return set()
    with open(MEMORY_FILE, "r") as f:
        return set(json.load(f))

def save_seen_urls(seen_urls):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(seen_urls), f, indent=2)

def is_new_url(url, seen_urls):
    return url not in seen_urls

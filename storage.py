# storage.py

import csv
import json
import os
from datetime import datetime
from config import OUTPUT_CSV

def save_to_csv(tweets, filename=None):
    """
    Save tweets to a single CSV file.
    ✅ Overwrites old data every time.
    ❌ Does NOT create new timestamped files.
    """

    # Use default CSV path from config
    filename = filename or OUTPUT_CSV

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    if not tweets:
        print("⚠️ No tweets to save.")
        return None

    # Always overwrite old CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["author", "timestamp", "tweet_url", "text"])
        writer.writeheader()
        writer.writerows(tweets)

    print(f"✅ Saved {len(tweets)} fresh tweets to {filename} (old data replaced)")
    return filename


def save_to_json(tweets, filename="tweets_output.json"):
    """
    Save tweets to a single JSON file.
    ✅ Overwrites old data every time.
    ❌ Does NOT create multiple files.
    """

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    if not tweets:
        print("⚠️ No tweets to save to JSON.")
        return None

    # Always overwrite old JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)

    print(f"💾 Tweets also saved as JSON: {filename}")
    return filename

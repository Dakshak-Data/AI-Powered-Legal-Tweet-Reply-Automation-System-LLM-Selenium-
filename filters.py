# filters.py

import re
from config import LEGAL_KEYWORDS

def filter_legal_tweets(tweets):
    """Filter tweets containing legal keywords."""
    legal_tweets = []
    for tweet in tweets:
        text = tweet["text"].lower()
        if any(re.search(rf"\b{kw}\b", text) for kw in LEGAL_KEYWORDS):
            legal_tweets.append(tweet)

    print(f"Filtered {len(legal_tweets)} legal-related tweets from {len(tweets)} total.")
    return legal_tweets

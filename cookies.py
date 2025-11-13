# cookies.py

import os
import json
from config import COOKIES_DIR

def save_cookies(driver, filename="twitter_cookies.json"):
    """Save cookies from a Selenium session to a JSON file."""
    os.makedirs(COOKIES_DIR, exist_ok=True)
    filepath = os.path.join(COOKIES_DIR, filename)

    cookies = driver.get_cookies()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    print(f"Cookies saved to {filepath}")


def load_cookies(driver, filename="twitter_cookies.json"):
    """Load cookies into Selenium from a JSON file."""
    filepath = os.path.join(COOKIES_DIR, filename)

    if not os.path.exists(filepath):
        print("Cookie file not found — please log in manually first.")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for cookie in cookies:
        if "expiry" in cookie:
            try:
                cookie["expiry"] = int(cookie["expiry"])
            except:
                cookie.pop("expiry", None)
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Failed to add cookie {cookie.get('name', '')}: {e}")

    print("Cookies loaded successfully.")
    return True

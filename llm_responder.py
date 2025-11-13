import os
import json
import time
import requests
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the Chrome driver setup
from driver_setup import setup_driver

# Load Gemini API key
load_dotenv()
LLM_API_KEY = os.getenv("LLM_API_KEY")


# =-=-=-=-=][''/] LLM REPLY GENERATION 
def generate_reply(tweet_text):
    """Send tweet text to Gemini and get a polite, factual reply."""
    if not LLM_API_KEY:
        raise ValueError("Missing LLM_API_KEY in .env")

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a polite, neutral assistant replying to social or legal tweets. "
                            "Always stay factual and calm. Avoid politics, personal opinions, or bias.\n\n"
                            f"Tweet: {tweet_text}\n\n"
                            "Write a short, polite, factual public reply."
                        )
                    }
                ]
            }
        ]
    }

    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={LLM_API_KEY}"
    )

    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code != 200:
        print(" LLM API error:", response.text)
        return None

    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return None


# ================== TWITTER AUTOMATION ==================
def comment_on_tweet(driver, tweet_url, reply_text):
    """Visit a tweet and post a reply (robust final version with dynamic button detection)."""
    try:
        driver.get(tweet_url)
        print(f"Opening: {tweet_url}")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
        )
        time.sleep(1.5)

        # Open reply modal
        reply_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='reply']"))
        )
        driver.execute_script("arguments[0].click();", reply_btn)
        print("Reply modal opened...")

        # Wait for reply modal to appear
        modal = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )

        # Find the active textbox
        textarea = WebDriverWait(modal, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        textarea.click()
        textarea.send_keys(reply_text)
        print("⌨yped reply text...")

        # Give UI time to enable button
        time.sleep(2)

        # Look for visible reply/post buttons dynamically
        button_selectors = [
            "//div[@role='dialog']//div[@data-testid='tweetButton']",
            "//div[@role='dialog']//div[@data-testid='tweetButtonInline']",
            "//div[@role='dialog']//button[@data-testid='tweetButton']",
            "//div[@role='dialog']//button[@data-testid='tweetButtonInline']",
            "//div[@role='dialog']//div[@data-testid='tweetButtonBottomBar']",
            "//div[@role='dialog']//div[contains(@aria-label, 'Reply') and @role='button']"
        ]

        reply_button = None
        for selector in button_selectors:
            try:
                reply_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if reply_button.is_displayed():
                    break
            except:
                continue

        if not reply_button:
            raise Exception("Could not find visible Reply button in modal (new X layout).")

        # Scroll to and click 
        driver.execute_script("arguments[0].scrollIntoView(true);", reply_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", reply_button)
        print("Clicked Reply button...")

        # Confirm modal closed
        try:
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            print("Reply successfully posted and modal closed.")
        except:
            print("Modal still open — possible click delay, retrying once...")
            driver.execute_script("arguments[0].click();", reply_button)
            time.sleep(3)

    except Exception as e:
        print(f" Failed to post reply on {tweet_url}: {e}")




# ================== MAIN PROCESS ==================
def process_tweets(input_file="twitter_legal_foryou.json", output_file="twitter_replies.json"):
    """Load tweets, generate LLM replies, and post comments via Selenium."""
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        tweets = json.load(f)

    print(" Launching Chrome using your real profile...")
    driver = setup_driver()  # Use persistent Chrome profile
    results = []

    for tweet in tweets:
        text = tweet.get("text", "")
        author = tweet.get("author", "")
        link = tweet.get("link") or tweet.get("tweet_url")  # lllllllllllllbaseeeee on linkkkkkkk

        if not link:
            print(f"Skipping tweet from {author} — missing 'link' key.")
            continue

        print(f"\n👤 {author}: {text[:80]}...")
        reply = generate_reply(text)
        if not reply:
            print("No reply generated.")
            continue

        print(f"AI Reply: {reply}")
        comment_on_tweet(driver, link, reply)

        tweet["ai_reply"] = reply
        results.append(tweet)

    # Save results
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nAll replies saved to {output_file}")
    print("🏁 Done — AI replies posted successfully!")


if __name__ == "__main__":

    process_tweets()


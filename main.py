# main.py

import time
from driver_setup import setup_driver
from scraper import scroll_page, extract_tweets
from filters import filter_legal_tweets
from storage import save_to_csv, save_to_json
from cookies import load_cookies, save_cookies
from config import SCROLL_PAUSE, MAX_SCROLLS
from llm_responder import process_tweets  # NEW Import LLM function


def main():
    print("\n🐦 Twitter 'For You' Legal Scraper + AI Responder")

    driver = setup_driver()

    print("🔗 Opening Twitter Home Page...")
    driver.get("https://twitter.com/home")
    time.sleep(5)

    # Try to load cookies, or ask user to login
    if not load_cookies(driver):
        print("\nPlease log in manually in this browser window.")
        input("After login, press ENTER here to save cookies...")
        save_cookies(driver)
    else:
        driver.refresh()
        time.sleep(5)

    print("⌛ Waiting for 'For You' page to load...")
    time.sleep(10)

    # Scroll to load tweets
    scroll_page(driver, max_scrolls=25, pause_time=3)

    # Save HTML snapshot (optional)
    html_data = driver.page_source
    with open("twitter_raw_page.html", "w", encoding="utf-8") as f:
        f.write(html_data)
    print("✅ Full raw HTML page saved as twitter_raw_page.html")

    #  Extract and display tweets
    all_tweets = extract_tweets(driver)
    print(f"📋 Extracted {len(all_tweets)} total tweets.")

    for i, t in enumerate(all_tweets, 1):
        print(f"\nTweet #{i}")
        print("Author:", t['author'])
        print("Text:", t['text'])
        print("URL:", t['tweet_url'])

    # Filter only legal-related tweets
    filtered = filter_legal_tweets(all_tweets)
    print(f"\n⚖️ Filtered {len(filtered)} legal tweets.")

    if not filtered:
        print("🚫 No legal tweets found. Exiting.")
        driver.quit()
        return

    # Save to CSV + JSON
    csv_file = save_to_csv(filtered)
    if csv_file:
        json_file = csv_file.replace(".csv", ".json")
        save_to_json(filtered, filename=json_file)
        print(f"✅ Filtered tweets saved to {json_file}")

        # Send to LLM for reply generation
        print("\n🤖 Sending tweets to LLM for AI reply generation...")
        process_tweets(json_file, "twitter_replies.json")  # <<=== MAIN ADDITION
        print("🏁 All replies saved in twitter_replies.json")

    else:
        print("No tweets to save — skipping LLM step.")

    # Cleanup
    driver.quit()
    print("✅ Browser closed. Task complete.")


if __name__ == "__main__":
    main()

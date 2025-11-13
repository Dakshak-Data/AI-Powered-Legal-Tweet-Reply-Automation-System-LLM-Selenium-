import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
def scroll_page(driver, max_scrolls=30, pause_time=2, save_html=False):
    """Scroll through Twitter feed, continuously extract all tweets (author + text + link),
    and immediately save after each scroll to avoid DOM tweet loss."""
    print("\n🌀 Scrolling through Twitter feed and scraping as we go...")
    body = driver.find_element(By.TAG_NAME, "body")
    all_tweets = []
    seen_links = set()  # Avoid duplicates by URL

    os.makedirs("data", exist_ok=True)  # Directory for backups

    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        # Extract tweets currently visible in DOM
        tweet_articles = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")

        for article in tweet_articles:
            try:
                # Extract tweet text
                text_blocks = article.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
                text = "\n".join([t.text.strip() for t in text_blocks if t.text.strip()])

                # Extract author handle
                try:
                    author_el = article.find_element(By.XPATH, ".//span[contains(text(), '@')]")
                    author = author_el.text.strip()
                except:
                    author = "Unknown"

                # Extract tweet link
                try:
                    link_el = article.find_element(By.XPATH, ".//a[contains(@href, '/status/')]")
                    tweet_url = link_el.get_attribute("href")
                except:
                    tweet_url = None

                # Avoid duplicates & add
                if tweet_url and tweet_url not in seen_links:
                    seen_links.add(tweet_url)
                    all_tweets.append({
                        "author": author,
                        "text": text,
                        "tweet_url": tweet_url
                    })
            except Exception:
                continue

        print(f"Scroll {i+1}/{max_scrolls} | Total unique tweets so far: {len(all_tweets)}")

        # Save tweets *after each scroll* (to prevent loss if DOM unloads old ones)
        partial_path = f"data/tweets_after_scroll_{i+1}.json"
        with open(partial_path, "w", encoding="utf-8") as f:
            import json
            json.dump(all_tweets, f, indent=2, ensure_ascii=False)
        print(f"Saved visible tweets snapshot: {partial_path}")

        # Optional HTML snapshot for debugging
        if save_html:
            os.makedirs("snapshots", exist_ok=True)
            html_path = f"snapshots/body_scroll_{i+1}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"Saved HTML snapshot: {html_path}")

        # Scroll smoothly
        driver.execute_script("window.scrollBy(0, 1200)")  # smaller scroll step
        time.sleep(pause_time)

        # Check if new tweets loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more new tweets loaded. Stopping scroll.")
            break
        last_height = new_height

    # Final save (after all scrolls)
    with open("data/all_tweets_final.json", "w", encoding="utf-8") as f:
        import json
        json.dump(all_tweets, f, indent=2, ensure_ascii=False)

    print(f"\nScrolling complete. Total unique tweets collected: {len(all_tweets)}")
    print("Final tweets saved to data/all_tweets_final.json")

    # Also save text version for reference
    with open("all_tweets.txt", "w", encoding="utf-8") as f:
        for tw in all_tweets:
            f.write(f"{tw['author']}\n{tw['text']}\n{tw['tweet_url']}\n" + "-"*80 + "\n")

    print(" Saved all tweets to all_tweets.txt\n")
    return all_tweets


def extract_tweets(driver):
    """Extract tweets from the loaded Twitter timeline."""
    print("Extracting tweets from page...")
    tweets = []
    seen = set()

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
        )
    except Exception:
        print("No tweets detected within wait time.")
        return tweets

    tweet_articles = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
    raw_html_list = []  # store all tweet HTMLs

    for i, tweet in enumerate(tweet_articles, 1):
        html = tweet.get_attribute("outerHTML")
        raw_html_list.append(html)

        print(f"\nTweet #{i} raw HTML:\n{html[:500]}...\n{'-'*100}")  # first 500 chars for preview

# Save all raw HTML tweets to a single file
    with open("raw_tweets.html", "w", encoding="utf-8") as f:
        f.write("\n\n".join(raw_html_list))

    print(f"Saved {len(raw_html_list)} raw tweets to raw_tweets.html")
    print("dddddddddddddddddd",tweet_articles)
    
    print(f"Found {len(tweet_articles)} tweet containers.")
    
    print("\n----- RAW TWEETS ON SCREEN -----\n")
    for i, el in enumerate(tweet_articles, 1):
        try:
            text_blocks = el.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
            full_text = " ".join([tb.text for tb in text_blocks if tb.text.strip()])
            print(f"Tweet #{i}: {full_text}\n{'-'*80}")
        except Exception as e:
            print(f"Couldn't extract tweet #{i}: {e}")


    for article in tweet_articles:
        try:
            # Extract text
            text = ""
            text_parts = article.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
            for t in text_parts:
                text += " " + t.text.strip()

            text = text.strip()
            if not text or text in seen:
                continue
            seen.add(text)

            # Handle (username)
            try:
                handle_el = article.find_element(By.XPATH, './/div[@dir="ltr"]/span[contains(text(),"@")]')
                handle = handle_el.text.strip()
            except:
                handle = ""

            # Tweet URL + timestamp
            try:
                link_el = article.find_element(By.XPATH, './/time/..')
                tweet_url = link_el.get_attribute("href")
                timestamp = article.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            except:
                tweet_url, timestamp = "", ""

            tweets.append({
                "author": handle,
                "timestamp": timestamp,
                "tweet_url": tweet_url,
                "text": text
            })

        except Exception as e:
            continue

    print(f"Extracted {len(tweets)} unique tweets.\n")
    return tweets

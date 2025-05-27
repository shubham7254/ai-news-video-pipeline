from agents.base_agent import BaseAgent
from services.scraper.theverge_scraper import scrape_techcrunch
from services.utils.memory import load_seen_urls, save_seen_urls, is_new_url
import json
import os

class NewsScraperAgent(BaseAgent):
    def run(self, input_data=None):
        print("🕵️ Running NewsScraperAgent...")

        all_articles = scrape_techcrunch()
        seen_urls = load_seen_urls()
        new_articles = []

        for article in all_articles:
            url = article.get("url", "")
            content = article.get("content", "").strip().lower()
            title = article.get("title", "").lower()

            # ⛔️ Skip URLs known to be useless (login pages, author links, etc.)
            if any(skip_word in url for skip_word in ["login", "signup", "author", "account", "privacy", "advertise"]):
                print(f"⚠️ Skipping non-news URL: {url}")
                continue

            # ⛔️ Skip articles with poor/short content
            if len(content.split()) < 50 or title.startswith("sign in"):
                print(f"⚠️ Skipping irrelevant or short content: {title}")
                continue

            if is_new_url(url, seen_urls):
                new_articles.append(article)
                seen_urls.add(url)

        if not new_articles:
            print("🌙 No new articles to process.")
            return None

        # Save seen urls
        save_seen_urls(seen_urls)

        # Save fresh news
        os.makedirs("data/raw_news", exist_ok=True)
        with open("data/raw_news/news.json", "w") as f:
            json.dump(new_articles, f, indent=2)

        print(f"✅ Saved {len(new_articles)} new articles to data/raw_news/news.json")
        return new_articles


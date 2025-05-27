from agents.base_agent import BaseAgent
import json
from services.summarizer.local_summarizer import summarize_text
import os

class SummarizerAgent(BaseAgent):
    def run(self, input_data=None):
        print("🧠 Running SummarizerAgent...")

        raw_path = "data/raw_news/news.json"
        summary_path = "data/summaries/summaries.json"
        skipped_path = "data/summaries/skipped_summaries.json"

        if not os.path.exists(raw_path):
            print("❌ news.json not found. Run NewsScraperAgent first.")
            return

        with open(raw_path, "r") as f:
            news_items = json.load(f)

        summaries = []
        skipped = []

        for item in news_items:
            title = item.get("title", "").strip()
            url = item.get("url")
            content = item.get("content", "").strip()

            if not content or len(content) < 100:
                print(f"⚠️ Skipping short/empty content: {url}")
                skipped.append({**item, "reason": "Content too short"})
                continue

            print(f"✏️ Summarizing: {title}...")

            # Better prompt style
            prompt = (
                f"Summarize the following article in a clear and concise way "
                f"for a 30-second YouTube Shorts news video:\n\n{content}"
            )
            summary = summarize_text(prompt)

            # Heuristic: If model echoes prompt or fails
            if (
                "Summarize the following" in summary or
                summary.strip() == "" or
                len(summary.strip()) < 40
            ):
                print(f"⚠️ Skipping low-quality or prompt-like summary: {title}")
                skipped.append({**item, "reason": "Low-quality summary"})
                continue

            summaries.append({
                "title": title,
                "url": url,
                "summary": summary
            })

        # Save summaries
        if not summaries:
            print("❌ No valid summaries.")
            return

        os.makedirs("data/summaries", exist_ok=True)

        with open(summary_path, "w") as f:
            json.dump(summaries, f, indent=2)

        # Save skipped items
        if skipped:
            with open(skipped_path, "w") as f:
                json.dump(skipped, f, indent=2)

        print(f"✅ Saved {len(summaries)} summaries to {summary_path}")
        if skipped:
            print(f"⚠️ {len(skipped)} articles were skipped and logged to {skipped_path}")
        return summaries

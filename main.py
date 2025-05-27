import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from agents.news_scraper_agent import NewsScraperAgent
from agents.planner_agent import PlannerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.video_creator_agent import VideoCreatorAgent
from agents.uploader_agent import UploaderAgent

if __name__ == "__main__":
    print("🚀 Starting Daily AI News Pipeline")

    # Step 1: Scrape fresh news
    news_agent = NewsScraperAgent()
    news = news_agent.run()

    if not news:
        print("📭 No new news to process. Exiting pipeline.")
        exit()

    # Step 2: Decide whether to continue
    planner = PlannerAgent()
    decision = planner.run()

    if not decision.get("publish", False):
        print("🛑 Planner decided to skip publishing today.")
        exit()

    # Step 3: Summarize new articles
    summarizer = SummarizerAgent()
    summarizer.run()

    # Step 4: Generate video and audio
    video_agent = VideoCreatorAgent()
    video_agent.run()

    # Step 5: Upload video
    uploader = UploaderAgent()
    uploader.run()

    print("✅ Daily AI pipeline complete!")

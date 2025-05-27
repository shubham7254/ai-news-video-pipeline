# 📰 AI News Video Pipeline 🎥

An autonomous multi-agent system that scrapes trending AI news, summarizes it, generates voiceovers, creates videos, and optionally uploads them to YouTube — all in one pipeline.

---

## 📌 Features

- 🌐 **NewsScraperAgent** — Scrapes latest AI-related news articles.
- 🧠 **SummarizerAgent** — Generates concise summaries using a local model.
- 🗓 **PlannerAgent** — Chooses which summaries to turn into videos.
- 🧑‍💻 **VideoCreatorAgent** — Creates narrated video clips from summaries + TTS audio using `MoviePy`.
- ☁️ **UploaderAgent** — Authenticates with YouTube and uploads the video automatically.

---

## 🛠 Tech Stack

- **Python 3.10+**
- `moviepy`, `edge-tts`, `transformers`, `google-auth`
- **YouTube Data API v3**
- Optional: `Docker`, `GitHub Actions`

---

## 🧩 Project Structure

ai-news-video-pipeline/
├── agents/ # All agent classes
├── data/
│ ├── audio/ # TTS audio files
│ ├── raw_news/ # Scraped news articles
│ ├── summaries/ # Generated summaries
│ └── videos/ # Final video clips
├── services/ # Functional modules for scraping, TTS, etc.
├── workflows/ # Pipeline orchestration
├── tests/ # Unit tests
├── main.py # Main entry point
├── requirements.txt
└── Dockerfile # (Optional) for containerized execution

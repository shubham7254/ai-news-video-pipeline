import os

base_dirs = {
    "agents": [
        "base_agent.py",
        "news_scraper_agent.py",
        "summarizer_agent.py",
        "video_creator_agent.py",
        "uploader_agent.py",
        "coordinator_agent.py"
    ],
    "workflows": ["daily_pipeline.py"],
    "services/scraper": ["theverge_scraper.py"],
    "services/summarizer": ["local_summarizer.py"],
    "services/tts": ["edge_tts_service.py"],
    "services/video": ["moviepy_editor.py"],
    "services/uploader": ["youtube_api.py"],
    "services/utils": ["logger.py", "config.py", "helpers.py"],
    "data/raw_news": [],
    "data/summaries": [],
    "data/videos": [],
    "tests/test_agents": [],
}

root_files = [
    ".env",
    "Dockerfile",
    "requirements.txt",
    "README.md",
    "main.py"
]

def create_structure():
    for dir_path, files in base_dirs.items():
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "__init__.py"), "w") as f:
            pass  # make it a package
        for file in files:
            open(os.path.join(dir_path, file), "w").close()

    for file in root_files:
        open(file, "w").close()

    print("✅ Folder structure created successfully!")

if __name__ == "__main__":
    create_structure()

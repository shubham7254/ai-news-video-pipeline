from agents.base_agent import BaseAgent
import os
import json
import asyncio
from services.tts.edge_tts_service import generate_tts
from services.video.video_maker import make_video

class VideoCreatorAgent(BaseAgent):
    def run(self, input_data=None):
        print("🎬 Running VideoCreatorAgent...")

        # Load summaries
        summary_file = "data/summaries/summaries.json"
        if not os.path.exists(summary_file):
            print("❌ summaries.json not found. Run SummarizerAgent first.")
            return

        with open(summary_file, "r") as f:
            summaries = json.load(f)

        # Create folders if missing
        os.makedirs("data/audio", exist_ok=True)
        os.makedirs("data/videos", exist_ok=True)

        # Loop through summaries and generate video/audio if not done
        for idx, item in enumerate(summaries):
            if "video_path" in item and os.path.exists(item["video_path"]):
                print(f"✅ Skipping summary {idx+1} (already has video).")
                continue

            text = item["summary"]
            audio_path = f"data/audio/voice_{idx+1}.mp3"
            text_path = f"data/audio/text_{idx+1}.txt"
            video_path = f"data/videos/video_{idx+1}.mp4"

            # Save the summary text
            with open(text_path, "w") as tf:
                tf.write(text)

            # Generate TTS and Video
            asyncio.run(generate_tts(text, audio_path))
            make_video(audio_path, text_path, video_path)

            # Update the item with paths
            item["audio_path"] = audio_path
            item["text_path"] = text_path
            item["video_path"] = video_path

            print(f"🎥 Video created: {video_path}")

        # Save updated summaries back
        with open(summary_file, "w") as f:
            json.dump(summaries, f, indent=2)

        print("✅ All videos processed and linked in summaries.json.")

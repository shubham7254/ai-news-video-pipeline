from agents.base_agent import BaseAgent
import os
import json
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class UploaderAgent(BaseAgent):
    def run(self, input_data=None):
        print("📤 Running UploaderAgent...")

        # Step 1: Authenticate
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
                creds = flow.run_local_server(port=0)
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)

        # Step 2: Load Summaries
        summary_file = "data/summaries/summaries.json"
        if not os.path.exists(summary_file):
            print("❌ summaries.json not found.")
            return

        with open(summary_file, "r") as f:
            summaries = json.load(f)

        youtube = build("youtube", "v3", credentials=creds)

        # Step 3: Upload videos that haven't been uploaded yet
        for idx, item in enumerate(summaries):
            video_path = item.get("video_path")
            if not video_path or not os.path.exists(video_path):
                print(f"⚠️ Video file missing for summary {idx+1}, skipping.")
                continue

            if item.get("uploaded"):
                print(f"✅ Video {idx+1} already uploaded.")
                continue

            title = item.get("title", f"AI News #{idx+1}")
            description = item.get("summary", "")

            request_body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["AI", "TechNews", "MachineLearning"],
                    "categoryId": "28",  # Science & Tech
                },
                "status": {
                    "privacyStatus": "public"
                }
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

            try:
                print(f"📤 Uploading: {video_path}")
                request = youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=media
                )
                response = request.execute()
                video_id = response["id"]
                print(f"✅ Uploaded successfully! Video ID: {video_id}")

                item["uploaded"] = True
                item["youtube_id"] = video_id

            except Exception as e:
                print(f"❌ Failed to upload {video_path}: {e}")
                continue

        # Save updated summaries
        with open(summary_file, "w") as f:
            json.dump(summaries, f, indent=2)

        print("📦 All pending videos uploaded.")

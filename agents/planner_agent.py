from agents.base_agent import BaseAgent
import json
import os
from dotenv import load_dotenv
load_dotenv()
import os
import re
from groq import Groq

class PlannerAgent(BaseAgent):
    def run(self, input_data=None):
        print("🧭 Running PlannerAgent...")

        # Load scraped news
        with open("data/raw_news/news.json", "r") as f:
            news_items = json.load(f)

        prompt = self.build_prompt(news_items)
        decision = self.ask_llm(prompt)

        with open("data/summaries/planner_decision.json", "w") as f:
            json.dump(decision, f, indent=2)

        print("✅ Planner decision saved!")
        return decision

    def build_prompt(self, news_items):
        articles = "\n".join([f"- {item['title']}" for item in news_items])
        prompt = f"""
You are an intelligent planner for an AI news agent system.

Here are today's AI headlines:

{articles}

🔧 Respond ONLY with a valid JSON object (no explanations, no markdown).

Use this exact structure:
{{
  "selected_titles": ["<exact titles>"],
  "tone": "<Friendly | Professional | Excited>",
  "publish": true/false
}}
"""

        return prompt


    def ask_llm(self, prompt):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Groq supports this
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.choices[0].message.content)



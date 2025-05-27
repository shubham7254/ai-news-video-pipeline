import edge_tts
import asyncio

async def generate_tts(text, output_path="data/summaries/voice.mp3", voice="en-US-AriaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

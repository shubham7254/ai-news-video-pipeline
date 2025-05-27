import moviepy.config as mpy_config
mpy_config.change_settings({"FFMPEG_BINARY": "/opt/homebrew/bin/ffmpeg"})
from moviepy.editor import ColorClip, TextClip, AudioFileClip, CompositeVideoClip

import os

def make_video(audio_path, text_path, output_path="data/videos/final_video.mp4"):
    # Load text summary
    with open(text_path, "r") as f:
        text = f.read()

    # Use a simple background (color or image)
    clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=30)

    # Overlay text
    txt_clip = TextClip(text, fontsize=40, color='white', size=(1000, None), method='caption')
    txt_clip = txt_clip.set_position("center").set_duration(30)

    # Add voice-over
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)

    final = CompositeVideoClip([clip, txt_clip])
    final.write_videofile(output_path, fps=24)

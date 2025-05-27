from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text: str, max_tokens=100):
    instruction = (
        "Summarize the following article in a professional, clear way "
        "so it can be used in a 30-second news narration:\n\n"
    )
    summary = summarizer(instruction + text.strip(), max_length=max_tokens, min_length=50, do_sample=False)
    return summary[0]['summary_text']

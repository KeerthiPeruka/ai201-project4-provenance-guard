"""Detection signals: Groq LLM-based judgment and pure-Python stylometric
heuristics. Each function takes raw text and returns a single 0-1 score
representing how AI-generated the text appears to be.
"""
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def groq_detection_score(text):
    prompt = f"""
You are an AI content attribution assistant.

Estimate how likely the following text is AI-generated.

Return ONLY one decimal number from 0 to 1.
0 means very likely human-written.
1 means very likely AI-generated.

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        score = float(response.choices[0].message.content.strip())
        return max(0.0, min(score, 1.0))

    except Exception:
        return 0.50


def stylometric_score(text):
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(words) == 0 or len(sentences) == 0:
        return 0.50

    unique_words = set(words)
    type_token_ratio = len(unique_words) / len(words)

    sentence_lengths = []
    for sentence in sentences:
        sentence_words = re.findall(r"\b\w+\b", sentence)
        sentence_lengths.append(len(sentence_words))

    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    variance = 0
    for length in sentence_lengths:
        variance += (length - avg_sentence_length) ** 2
    variance = variance / len(sentence_lengths)

    punctuation_count = 0
    for char in text:
        if char in ",;:!?":
            punctuation_count += 1

    punctuation_density = punctuation_count / len(words)

    score = 0.50

    if type_token_ratio < 0.45:
        score += 0.15
    else:
        score -= 0.10

    if variance < 8:
        score += 0.20
    else:
        score -= 0.15

    if avg_sentence_length > 18:
        score += 0.10

    if punctuation_density < 0.05:
        score += 0.05
    else:
        score -= 0.05

    return max(0.0, min(score, 1.0))
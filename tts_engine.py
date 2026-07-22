import os
import requests
import json
import asyncio
import edge_tts
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgq9S3JGCKiA")

async def convert_tts(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, "en-US-AndrewMultilingualNeural")
    submaker = edge_tts.SubMaker()
    word_timings = []
    temp_edge = output_path + ".tmp.mp3"
    with open(temp_edge, "wb") as fp:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                fp.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                submaker.feed(chunk)
                words = chunk["text"].strip().split()
                if words:
                    start_sec = chunk["offset"] / 10000000.0
                    duration_sec = chunk["duration"] / 10000000.0
                    word_duration = duration_sec / len(words)
                    for idx, w in enumerate(words):
                        word_timings.append({
                            "word": w.strip(".,!?;:\"()[]{}'"),
                            "start": start_sec + (idx * word_duration),
                            "end": start_sec + ((idx + 1) * word_duration)
                        })
    if API_KEY:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                if os.path.exists(temp_edge):
                    os.remove(temp_edge)
                return word_timings
        except Exception:
            pass
    if os.path.exists(temp_edge):
        if os.path.exists(output_path):
            os.remove(output_path)
        os.rename(temp_edge, output_path)
    return word_timings

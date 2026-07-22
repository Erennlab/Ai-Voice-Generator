import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import uuid
from tts_engine import convert_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

desktop_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(desktop_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=output_dir), name="outputs")

jobs = {}

class TTSRequest(BaseModel):
    text: str

async def run_tts_generation(job_id: str, text: str, filename: str):
    jobs[job_id] = {"status": "processing", "progress": 20}
    try:
        output_file = os.path.join(output_dir, filename)
        timings = await convert_tts(text, output_file)
        jobs[job_id] = {
            "status": "completed",
            "progress": 100,
            "audio_url": f"/outputs/{filename}",
            "filename": filename,
            "timings": timings
        }
    except Exception as e:
        jobs[job_id] = {
            "status": "failed",
            "progress": 0,
            "error": str(e)
        }

@app.post("/api/tts")
def start_tts(req: TTSRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    filename = f"audio_{int(asyncio.get_event_loop().time())}.mp3"
    jobs[job_id] = {"status": "queued", "progress": 0}
    background_tasks.add_task(run_tts_generation, job_id, req.text, filename)
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/tts/{job_id}")
def check_tts_status(job_id: str):
    if job_id not in jobs:
        return {"status": "not_found"}
    return jobs[job_id]

# AI Voice Generator

A high-performance, real-time Text-to-Speech (TTS) engine that combines Microsoft Edge-TTS with ElevenLabs hyper-realistic voice synthesis. Features a modern, responsive web dashboard with progress tracking and direct MP3 exports.

## Features

*   Dual-Engine synthesis (Edge-TTS fallback + ElevenLabs premium support).
*   Word-level timing metadata generation.
*   FastAPI asynchronous backend.
*   Responsive dark-themed HTML5/CSS3 frontend.
*   One-click Windows startup batch script.

## Setup & Installation

### 1. Prerequisites

Ensure you have Python 3.10+ installed on your system.

### 2. Install Dependencies

Install the required packages using pip:

```bash
pip install fastapi uvicorn edge-tts requests python-dotenv
```

### 3. Environment Configuration

Create a `.env` file in the root folder and add your ElevenLabs API credentials:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id
```

If the `ELEVENLABS_API_KEY` is omitted, the application will automatically fall back to the premium Microsoft Edge-TTS engine for free synthesis.

## How to Run

Double-click `start.bat` on Windows, or manually start the server and open the interface:

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Then, open `index.html` in any web browser.

## License

MIT License. Feel free to use and modify for personal or commercial projects.

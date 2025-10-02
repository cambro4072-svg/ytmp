# 🎬 Universal Media Converter (Streamlit)

This repository contains a Streamlit app that converts media files using FFmpeg.  
Features:
- Styled UI with gradient background and custom buttons.
- Files are streamed to disk (prevents memory spikes).
- Auto-cleanup: temporary files older than 10 minutes are removed on each run.
- Manual cleanup button included.

## Files
- `App.py` — main Streamlit app
- `requirements.txt` — dependencies
- `README.md` — this file

## Run locally
1. Install Python (3.8+ recommended) and FFmpeg on your machine.
   - macOS (Homebrew): `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

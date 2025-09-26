# ASR-Automatic-Speech-Recognition-
Using Reverb-ASR, the application strives to offer robust verbose transcription of audio inputs.

# ASR – Automatic Speech Recognition API (Reverb)

This project exposes a **FastAPI** web service that performs **speech-to-text** using the Reverb ASR stack. Clients (for example, a microphone button on a website) upload an audio file to `/transcribe` and receive a **verbatim** transcript as JSON.

> **Important:** No Hugging Face account or token is required to run this project. Everything is installed directly from GitHub.  

---

## What’s in this repo

- `app/main.py` – the FastAPI service:
  - `GET /health` → responds with `{"status":"ok","model":"reverb_asr_v1"}`
  - `POST /transcribe` (form field `file`) → responds with `{ "text": "...", "words": [] }`
  - Handles audio conversion to **16 kHz mono WAV** with `ffmpeg`.
  - Deletes temporary files automatically.
- `requirements.txt` – all Python dependencies needed.
- `.gitignore` – ignores `.venv/`, local caches, and any `.env` secrets.

---

## Prerequisites

- **Python 3.10 or later**
- **ffmpeg** installed and accessible in PATH
- **git** and **pip**

---

## Setup Instructions

### Get the code and enter the folder
```bash
git clone https://github.com/sukesh46/ASR-Automatic-Speech-Recognition-.git
cd ASR-Automatic-Speech-Recognition-
```

---

## Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\Activate.ps1   # Windows PowerShell
python -m pip install -U pip setuptools wheel
```

---

## Install ffmpeg

Check if installed:
```bash
ffmpeg -version
```

If not installed:
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get update && sudo apt-get install -y ffmpeg`
- **Windows**: Download from ffmpeg.org and add it to PATH.

---

## Install dependencies
```bash
python -m pip install -r requirements.txt
```

---

## Install Reverb ASR
```bash
python -m pip install --no-deps "git+https://github.com/revdotcom/reverb.git"
```

---

## Run the API
```bash
export WANDB_MODE=disabled        # macOS/Linux
# Windows PowerShell: $env:WANDB_MODE="disabled"

uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

**Expected output**:
```
Uvicorn running on http://127.0.0.1:8080
Application startup complete.
```

---

## Testing the API

Open another terminal (no need to activate the venv):

### Health check
```bash
curl http://127.0.0.1:8080/health
```

### Response
```json
{"status":"ok","model":"reverb_asr_v1"}
```

---

## Transcription

Place a test audio file on your Desktop (e.g., harvard.wav). Then run:
```bash
curl -F "file=@/Users/<your-username>/Desktop/harvard.wav" http://127.0.0.1:8080/transcribe
```

**Example response**:
```json
{
  "text": "the stale smell of old beer lingers ...",
  "words": []
}
```

- `text` contains the full transcript.
- `words` is currently an empty array but reserved for future word-level timing output.

---

## Integration Notes

- This service is intended to be called from a frontend widget. A simple button can record audio, send it to `/transcribe`, and display the returned text.
- In `main.py`, CORS is currently set to allow all (`allow_origins=["*"]`). In production, restrict it to your actual domain.
- Temporary audio files are cleaned up after each request.
- No Hugging Face token is needed — everything runs locally.

---

## Troubleshooting

- **Can’t connect / curl fails**: Ensure Uvicorn shows *Application startup complete* and that you’re calling the right port. If 8080 is busy, run:
  ```bash
  uvicorn app.main:app --host 127.0.0.1 --port 8090 --reload
  ```

- **“Form data requires python-multipart”**: Run
  ```bash
  python -m pip install python-multipart
  ```

- **“ffmpeg not found”**: Install ffmpeg as shown above.
- **“Invalid output format”**: Make sure you’re on the correct `main.py` (the provided one, with no `format="text"` argument).
- **Address already in use**: Kill the process using the port or start Uvicorn on another port.

---

## License

This project uses Reverb ASR, licensed under the Apache License 2.0.








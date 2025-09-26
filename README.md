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

### 1) Get the code and enter the folder
```bash
git clone https://github.com/sukesh46/ASR-Automatic-Speech-Recognition-.git
cd ASR-Automatic-Speech-Recognition-

# app/main.py
import os
import tempfile
import subprocess
import shlex
from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import wenet  # comes from revdotcom/reverb install

# Load model once at startup
MODEL_ID = os.getenv("REVERB_MODEL", "reverb_asr_v1")
VERBATIMICITY = 1.0  # enforce word-for-word transcription
asr = wenet.load_model(MODEL_ID)

app = FastAPI(title="Reverb ASR API", version="1.0.0")

# Allow frontend widget to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except FileNotFoundError:
        return False

def _save_upload(upload: UploadFile) -> str:
    suffix = os.path.splitext(upload.filename or "")[1] or ".webm"
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp.write(upload.file.read())
    tmp.flush()
    tmp.close()
    return tmp.name

def _convert_to_wav16k(path_in: str) -> str:
    if not _ffmpeg_available():
        return path_in
    out_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    cmd = f'ffmpeg -y -i {shlex.quote(path_in)} -ac 1 -ar 16000 -f wav {shlex.quote(out_path)}'
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_path if proc.returncode == 0 else path_in

def _parse_ctm(ctm_text: str) -> List[Dict[str, Any]]:
    words = []
    for line in ctm_text.strip().splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        utt, ch, start, dur, word = parts[:5]
        try:
            s, d = float(start), float(dur)
        except ValueError:
            continue
        words.append({"word": word, "start": s, "end": s + d, "duration": d})
    return words

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_ID}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    src = _save_upload(file)
    wav = _convert_to_wav16k(src)
    try:
        text = asr.transcribe(wav, verbatimicity=1.0)  # no 'format' arg
        return JSONResponse({"text": text, "words": []})
    finally:
        for p in (src, wav):
            if p and os.path.exists(p):
                try: os.remove(p)
                except: pass
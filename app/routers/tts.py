import io
import time
import soundfile as sf
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.services.tts_service import TTSService

router = APIRouter(prefix="/api/tts", tags=["TTS"])

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "af_heart"
    speed: Optional[float] = 1.0

@router.post("")
def generate_speech(req: TTSRequest):
    try:
        # Generate Float32 audio samples and sample rate (usually 24000Hz)
        samples, sample_rate = TTSService.generate(req.text, voice=req.voice, speed=req.speed)
        
        # Write to in-memory bytes container as WAV
        wav_io = io.BytesIO()
        sf.write(wav_io, samples, sample_rate, format='WAV', subtype='PCM_16')
        wav_io.seek(0)
        
        return StreamingResponse(wav_io, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/benchmark")
def benchmark_tts():
    try:
        start_time = time.time()
        # Cold/warm start check + simple string generation
        samples, sample_rate = TTSService.generate("Benchmark test", voice="af_heart", speed=1.0)
        duration = time.time() - start_time
        
        return {
            "status": "success",
            "generation_time_sec": round(duration, 3),
            "samples_count": len(samples),
            "sample_rate": sample_rate,
            "audio_duration_sec": round(len(samples) / sample_rate, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

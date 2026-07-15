import io
import time
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
async def generate_speech(req: TTSRequest):
    try:
        audio_bytes = await TTSService.generate(req.text, voice=req.voice, speed=req.speed)
        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/benchmark")
async def benchmark_tts():
    try:
        start_time = time.time()
        audio_bytes = await TTSService.generate("Benchmark test", voice="af_heart", speed=1.0)
        duration = time.time() - start_time
        
        return {
            "status": "success",
            "generation_time_sec": round(duration, 3),
            "bytes_count": len(audio_bytes),
            "audio_type": "mp3"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

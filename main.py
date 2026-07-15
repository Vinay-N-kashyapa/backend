from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import llm, tts

app = FastAPI(title="PinIT Career OS API Server")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # To be restricted in production config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.services.tts_service import TTSService

# Register routers
app.include_router(llm.router)
app.include_router(tts.router)

@app.on_event("startup")
def startup_event():
    print("[Startup] Initializing Kokoro TTS Engine...")
    try:
        TTSService.initialize()
        print("[Startup] Kokoro TTS Engine successfully loaded. Running inference smoke test...")
        samples, sample_rate = TTSService.generate("Warmup", voice="af_heart", speed=1.0)
        print(f"[Startup] Smoke test success! Generated {len(samples)} samples at {sample_rate}Hz.")
    except Exception as e:
        import traceback
        print("[Startup] Failed to initialize or execute Kokoro TTS smoke test:")
        traceback.print_exc()

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "healthy", "service": "PinIT API Server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import llm, tts
from app.services.tts_service import TTSService

app = FastAPI(title="PinIT Career OS API Server")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Set to False to permit wildcard origins cleanly in modern browsers
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(llm.router)
app.include_router(tts.router)

@app.on_event("startup")
async def startup_event():
    print("[Startup] Initializing Edge TTS Service...")
    try:
        TTSService.initialize()
        # Non-blocking async warmup
        samples = await TTSService.generate("Warmup")
        print(f"[Startup] Edge TTS Warmup success! Generated {len(samples)} bytes.")
    except Exception as e:
        import traceback
        print("[Startup] Failed to initialize Edge TTS service:")
        traceback.print_exc()

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {"status": "healthy", "service": "PinIT API Server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

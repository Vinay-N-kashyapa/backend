import logging
import edge_tts

logger = logging.getLogger("pinit.tts")

# Map Kokoro voices to Edge TTS Premium Azure Neural voices
VOICE_MAPPING = {
    # Female Voices
    "af_heart": "en-US-AriaNeural",       # Warm, sweet US Female
    "af_nicole": "en-US-JennyNeural",      # Creative US Female
    "af_sky": "en-US-MichelleNeural",     # Friendly US Female
    "af_bella": "en-US-AriaNeural",       # Energetic US Female
    "af_sarah": "en-US-JennyNeural",      # Warm, socratic US Female
    "bf_emma": "en-GB-SoniaNeural",       # Professional UK Female
    "bf_isabella": "en-GB-SoniaNeural",   # Professional UK Female
    
    # Male Voices
    "am_liam": "en-US-GuyNeural",         # Clear, friendly US Male
    "am_fenrir": "en-US-SteffanNeural",    # Clean US Male
    "am_adam": "en-US-SteffanNeural",     # Wise US Male
    "bm_lewis": "en-GB-RyanNeural",       # Serious UK Male
    "bm_george": "en-GB-RyanNeural",      # UK Male
}

class TTSService:
    @classmethod
    def initialize(cls):
        logger.info("Edge TTS Service initialized (no local models to load).")

    @classmethod
    async def generate(cls, text: str, voice: str = "af_heart", speed: float = 1.0) -> bytes:
        # Resolve mapped voice, default to Aria (warm US female)
        edge_voice = VOICE_MAPPING.get(voice, "en-US-AriaNeural")
        
        # Calculate speed rate offset percentage (e.g. 1.0 -> "+0%", 1.2 -> "+20%", 0.8 -> "-20%")
        rate_percent = int((speed - 1.0) * 100)
        rate_str = f"{rate_percent:+}%" if rate_percent != 0 else "+0%"

        logger.info(f"Generating speech via Edge TTS: Voice={edge_voice}, Speed={rate_str}")
        
        communicate = edge_tts.Communicate(text, edge_voice, rate=rate_str)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
                
        return audio_data

import logging
import edge_tts

logger = logging.getLogger("pinit.tts")

# Map Kokoro voices to Edge TTS Premium Azure Neural voices
VOICE_MAPPING = {
    # ── Mentors ───────────────────────────────────────────────────────────
    "af_heart": "en-US-AriaNeural",             # Ms. Priya (Polished & Bright US Female - af_bella style)
    "am_liam": "en-IN-PrabhatNeural",             # Mr. Anish (Firm & Caring Indian Male)
    
    # ── Teachers ──────────────────────────────────────────────────────────
    "am_fenrir": "en-US-SteffanNeural",           # Mr. Kashyap (Structured US Male)
    "am_karthic": "en-US-ChristopherNeural",       # Mr. Karthic (Professional US Male)
    "bf_emma": "en-GB-SoniaNeural",               # Ms. Maya (Professional UK Female)
    "af_nicole": "en-US-AvaNeural",               # Ms. Divya (Creative/Energetic US Female)
    
    # ── Mission Avatars & Fallbacks ───────────────────────────────────────
    "bf_isabella": "en-GB-LibbyNeural",           # Ms. Shalini (Stoic/Silent UK Female)
    "af_sarah": "en-US-EmmaNeural",               # Ms. Sneha (Supportive US Female)
    
    # ── Interviewers ──────────────────────────────────────────────────────
    "bm_lewis": "en-GB-RyanNeural",               # Mr. Vikram / Mr. Abhijit (Strict UK Male)
    "am_adam": "en-US-BrianNeural",               # Mr. Aditya (Wise System Design US Male)
    "af_bella": "en-US-AriaNeural",               # Ms. Neha (High-Stress US Female)
    "bm_george": "en-GB-RyanNeural",              # Mr. Abhijit (UK Male Executive)
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

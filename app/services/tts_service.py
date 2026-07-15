import os
import urllib.request
import logging
from kokoro_onnx import Kokoro

logger = logging.getLogger("pinit.tts")

MODEL_PATH = "model.onnx"
VOICES_PATH = "voices.json"

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/v0.2.0/kokoro-v0.19.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/v0.2.0/voices.json"

class TTSService:
    _engine = None

    @classmethod
    def initialize(cls):
        if cls._engine is not None:
            return

        # Ensure files exist, download dynamically on startup if missing
        if not os.path.exists(MODEL_PATH):
            logger.info("Downloading Kokoro model.onnx...")
            try:
                urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
                logger.info("Kokoro model.onnx downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download Kokoro model.onnx: {e}")
                raise e

        if not os.path.exists(VOICES_PATH):
            logger.info("Downloading Kokoro voices.json...")
            try:
                urllib.request.urlretrieve(VOICES_URL, VOICES_PATH)
                logger.info("Kokoro voices.json downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download Kokoro voices.json: {e}")
                raise e

        try:
            cls._engine = Kokoro(MODEL_PATH, VOICES_PATH)
            logger.info("Kokoro TTS Engine successfully initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Kokoro engine: {e}")
            raise e

    @classmethod
    def generate(cls, text: str, voice: str = "af_heart", speed: float = 1.0):
        cls.initialize()
        if not cls._engine:
            raise RuntimeError("Kokoro engine is not initialized.")
        return cls._engine.create(text, voice=voice, speed=speed)

import os
import logging
import httpx
from kokoro_onnx import Kokoro

logger = logging.getLogger("pinit.tts")

MODEL_PATH = "kokoro-v1.0.onnx"
VOICES_PATH = "voices-v1.0.bin"

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

class TTSService:
    _engine = None

    @staticmethod
    def _download_file(url: str, dest_path: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        with httpx.Client(follow_redirects=True, timeout=120.0) as client:
            with client.stream("GET", url, headers=headers) as response:
                if response.status_code != 200:
                    raise RuntimeError(f"HTTP Error {response.status_code} while downloading {url}")
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)

    @classmethod
    def initialize(cls):
        if cls._engine is not None:
            return

        # Ensure files exist, download dynamically on startup if missing
        if not os.path.exists(MODEL_PATH):
            logger.info("Downloading Kokoro model...")
            try:
                cls._download_file(MODEL_URL, MODEL_PATH)
                logger.info("Kokoro model downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download Kokoro model: {e}")
                raise e

        if not os.path.exists(VOICES_PATH):
            logger.info("Downloading Kokoro voices...")
            try:
                cls._download_file(VOICES_URL, VOICES_PATH)
                logger.info("Kokoro voices downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download Kokoro voices: {e}")
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

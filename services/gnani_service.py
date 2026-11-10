
import os
from dotenv import load_dotenv

from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")

if not API_KEY:
    raise ValueError("GNANI_API_KEY missing in .env")

# Initialize Gnani clients
stt_client = GnaniSTTClient(api_key=API_KEY)
tts_client = GnaniTTSClient(api_key=API_KEY)


def transcribe_audio(audio_bytes, filename, language_code):

    result = stt_client.transcribe_bytes(
        audio_bytes,
        filename=filename,
        language_code=language_code
    )

    transcript = result.get("transcript", "")

    if not transcript:
        raise ValueError(f"Empty transcription: {result}")

    return {
        "transcript": transcript,
        "model": result.get("model", "Prisma")
    }


def generate_speech(text, language_code):

    audio = tts_client.synthesize(
        text,
        voice="Nalini",
        model="timbre-v2.5",
        language=language_code,
        speed=1.0,
        audio_config=AudioConfig(
            sample_rate=48000,
            encoding="linear_pcm",
            container="wav"
        )
    )

    return audio



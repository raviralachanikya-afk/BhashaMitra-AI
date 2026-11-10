
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from services.gnani_service import (
    transcribe_audio,
    generate_speech
)

from services.order_service import (
    extract_order,
    create_response
)

app = FastAPI(
    title="BhashaMitra AI",
    description="Multilingual voice ordering assistant for Indian shops",
    version="1.0.0"
)


LANGUAGES = {
    "Hindi": ("hi-IN", "hi"),
    "Telugu": ("te-IN", "te"),
    "Hinglish": ("hi-IN", "en")
}


class TextOrder(BaseModel):
    text: str
    language: str = "English"


@app.get("/")
def home():
    return {
        "message": "Welcome to BhashaMitra AI",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/process-text")
def process_text(request: TextOrder):

    if request.language not in LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    _, response_language = LANGUAGES[request.language]

    order = extract_order(request.text)

    response_text = create_response(
        order,
        response_language
    )

    return {
        "transcript": request.text,
        "order": order,
        "response": response_text
    }


@app.post("/process-audio")
async def process_audio(
    audio: UploadFile = File(...),
    language: str = Form(...)
):

    if language not in LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    language_code, response_language = LANGUAGES[language]

    if audio.content_type not in [
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp4",
        "audio/ogg",
        "audio/flac"
    ]:
        raise HTTPException(
            400,
            "Unsupported audio format"
        )

    audio_bytes = await audio.read()

    if len(audio_bytes) > 15 * 1024 * 1024:
        raise HTTPException(413, "Audio file too large")

    try:
        transcription = transcribe_audio(
            audio_bytes,
            audio.filename or "recording.wav",
            language_code
        )

        transcript = transcription.get("transcript", "")

        if not transcript:
            raise ValueError("Empty transcription received")

        order = extract_order(transcript)

        response_text = create_response(
            order,
            response_language
        )

        return {
            "transcript": transcript,
            "detected_language": transcription.get(
                "detected_language_code",
                language_code
            ),
            "model": transcription.get(
                "model",
                "prisma-v2.5"
            ),
            "order": order,
            "response": response_text
        }

    except Exception as error:
        raise HTTPException(502, str(error))


@app.post("/speak")
def speak(request: TextOrder):

    if request.language not in LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    language_code, _ = LANGUAGES[request.language]

    try:
        audio_bytes = generate_speech(
            request.text,
            language_code
        )

        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={
                "Content-Disposition":
                'inline; filename="bhashamitra_response.wav"'
            }
        )

    except Exception as error:
        raise HTTPException(502, str(error))

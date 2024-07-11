from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..audio_processing.youtube_audio_extractor import transcribe_youtube_video
from ..config.firebase_config import db

router = APIRouter()


class YouTubeURL(BaseModel):
    url: str

@router.post("/transcribe/")
async def transcribe_youtube(youtube_url: YouTubeURL):
    try:
        transcription = transcribe_youtube_video(youtube_url.url)

        # Firebase에 저장
        doc_ref = db.collection("transcriptions").add(
            {"url": youtube_url.url, "transcription": transcription}
        )

        return {"message": "변환 완료 그리괴 저장", "id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from .api.routes import router
from .config.firebase_config import initialize_firebase
from .audio_processing.youtube_audio_extractor import transcribe_youtube_video

app = FastAPI()

# 라우터 포함
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

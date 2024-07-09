from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to MyWikiDocs API"}


@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename, "message": "Audio uploaded successfully"}

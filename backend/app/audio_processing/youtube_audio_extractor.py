from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)
from dotenv import load_dotenv

load_dotenv()

# 로컬 파싱을 사용할지 여부를 설정하는 플래그
local = False

# 예제 YouTube URL 목록
urls = ["https://youtu.be/HQU2vbsbXkU?si=i9z6MsbFpyYMPMqh"]

# 오디오 파일을 저장할 디렉토리
save_dir = "/Users/jiminking/Documents/김지민/projects/mywiki"


# Transcribe the videos to text
if local:
    loader = GenericLoader(
        YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal()
    )
else:
    loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
docs = loader.load()

print(docs[0].page_content[0:500])
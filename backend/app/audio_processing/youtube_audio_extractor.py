from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)
import os

save_dir = "/Users/jiminking/Documents/김지민/projects/mywiki"
local = False


def transcribe_youtube_video(url):
    urls = [url]
    if local:
        loader = GenericLoader(
            YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal()
        )
    else:
        loader = GenericLoader(
            YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser()
        )

    docs = loader.load()
    return docs[0].page_content if docs else ""

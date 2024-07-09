import os
import io
import logging
import time
from typing import List
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

AudioSegment.converter = os.environ.get("FFMPEG_PATH", "/opt/homebrew/bin/ffmpeg")
AudioSegment.ffprobe = os.environ.get("FFPROBE_PATH", "/opt/homebrew/bin/ffprobe")

logging.basicConfig(level=logging.INFO)


def process_chunk(audio: AudioSegment, start_ms: int, end_ms: int) -> bytes:
    """
    오디오 청크를 처리하는 함수
    """
    part_of_audio = audio[start_ms:end_ms]
    buffer = io.BytesIO()
    part_of_audio.export(buffer, format="mp3")
    buffer.seek(0)
    return buffer.getvalue()


def split_audio(file_content: bytes, chunk_length_ms: int = 300000) -> List[bytes]:
    """
    오디오 파일을 분할하는 함수
    """
    start_time = time.time()

    try:
        audio = AudioSegment.from_file(io.BytesIO(file_content))
    except Exception as e:
        logging.error(f"Error processing audio: {e}")
        raise

    total_milliseconds = len(audio)
    total_chunks = int(total_milliseconds // chunk_length_ms + 1)

    logging.info(f"Total chunks: {total_chunks}")
    logging.info(f"Total milliseconds: {total_milliseconds}")

    # 파일명을 저장할 리스트
    output_chunks = []

    # ThreadPoolExecutor를 사용하여 오디오를 병렬 분할 처리
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(total_chunks):
            start_ms = i * chunk_length_ms
            end_ms = (
                start_ms + chunk_length_ms
                if i < total_chunks - 1
                else total_milliseconds
            )
            futures.append(executor.submit(process_chunk, audio, start_ms, end_ms))

        for future in futures:
            output_chunks.append(future.result())

    end_time = time.time()
    logging.info(f"Splitting audio took {end_time - start_time:.2f} seconds")

    return output_chunks


# 테스트 코드 (실제 사용 시 제거)
if __name__ == "__main__":
    filename = "/Users/jiminking/Documents/김지민/projects/myproject/wiset/20240701-1회차(음성).m4a"
    print(filename)

    with open(filename, "rb") as file:
        file_content = file.read()
    chunks = split_audio(file_content)
    logging.info(f"Number of chunks created: {len(chunks)}")

import os
import io
import logging
import time
from typing import List
from pydub import AudioSegment

AudioSegment.converter = os.environ.get("FFMPEG_PATH", "/opt/homebrew/bin/ffmpeg")
AudioSegment.ffprobe = os.environ.get("FFPROBE_PATH", "/opt/homebrew/bin/ffprobe")

logging.basicConfig(level=logging.INFO)


def split_audio(file_content: bytes, chunk_length_ms: int = 300000) -> List[bytes]:
    """
    오디오 파일을 분할하는 함수
    - Fastapi에서는 파일 내용을 받아서 처리하기 때문에 파일 경로가 아닌 파일 내용을 받음. str -> bytes
    """

    start_time = time.time()

    try:
        audio = AudioSegment.from_file(io.BytesIO(file_content))
    except Exception as e:
        logging.error(f"Error processing audio: {e}")
        raise

    # Pydub는 밀리초 단위로 시간을 계산함.
    total_milliseconds = len(audio)
    total_chunks = int(total_milliseconds // chunk_length_ms + 1)

    logging.info(f"Total chunks: {total_chunks}")
    logging.info(f"Total milliseconds: {total_milliseconds}")

    # 파일명을 저장할 리스트
    output_chunks = []

    for i in range(total_chunks):
        if i < total_chunks - 1:
            # 300초 단위로 오디오를 자름
            part_of_audio = audio[i * chunk_length_ms : (i + 1) * chunk_length_ms]
        else:
            # 마지막 부분은 나머지 전체를 자름
            part_of_audio = audio[i * chunk_length_ms :]

        buffer = io.BytesIO()
        part_of_audio.export(buffer, format="mp3")
        buffer.seek(0)
        output_chunks.append(buffer.getvalue())

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

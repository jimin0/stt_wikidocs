import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, firestore

# .env 파일에서 환경 변수 로드
load_dotenv()

sdk_path = os.environ.get('FIREBASE_ADMIN_SDK_PATH')
if not sdk_path:
    raise ValueError("FIREBASE_ADMIN_SDK_PATH 환경 변수가 설정되지 않았습니다.")

cred = credentials.Certificate(sdk_path)
app = initialize_app(cred)
db = firestore.client()
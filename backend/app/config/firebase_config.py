import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def initialize_firebase():
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    print(f"FIREBASE_CREDENTIALS_PATH: {os.getenv('FIREBASE_CREDENTIALS_PATH')}")
    if not cred_path:
        raise ValueError("파이어베이스 경로 다시 확인")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firebase()

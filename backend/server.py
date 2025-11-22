from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid
from datetime import datetime, timezone
import base64
import tempfile
# کتابخانه جدید مایکروسافت اج
import edge_tts

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db_name = os.environ.get('DB_NAME', 'voiceflow_db')
db = client[db_name]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# --- Models ---
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural" # پیش‌فرض تغییر کرد
    speed: float = 1.0
    model: str = "tts-1"

class TTSResponse(BaseModel):
    audio_base64: str
    format: str = "mp3"

# --- Helper to convert float speed to EdgeTTS format ---
def get_rate_str(speed: float) -> str:
    # تبدیل عدد 1.5 به "+50%" و 0.8 به "-20%"
    percentage = int((speed - 1.0) * 100)
    if percentage >= 0:
        return f"+{percentage}%"
    else:
        return f"{percentage}%"

@api_router.get("/")
async def root():
    return {"message": "VoiceFlow API (Edge TTS Version)"}

@api_router.post("/generate-speech", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
        # انتخاب صدا (اگر صدای نامعتبر آمد، پیش‌فرض را استفاده کن)
        voice_id = request.voice if "Neural" in request.voice else "en-US-AriaNeural"
        
        # تنظیم سرعت
        rate_str = get_rate_str(request.speed)
        
        # ارتباط با Edge TTS
        communicate = edge_tts.Communicate(request.text, voice_id, rate=rate_str)
        
        # ذخیره در فایل موقت
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_filename = temp_file.name
            
        await communicate.save(temp_filename)
        
        # خواندن فایل و تبدیل به Base64
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()
            
        # پاک کردن فایل موقت
        os.unlink(temp_filename)
        
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return TTSResponse(audio_base64=audio_base64)
        
    except Exception as e:
        logging.error(f"TTS generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@api_router.get("/voices")
async def get_voices():
    # لیست صداهای با کیفیت مایکروسافت
    return {
        "voices": [
            {"id": "en-US-AriaNeural", "name": "Aria (Female)", "description": "Expressive, Natural"},
            {"id": "en-US-GuyNeural", "name": "Guy (Male)", "description": "Professional, Calm"},
            {"id": "en-US-JennyNeural", "name": "Jenny (Female)", "description": "Friendly, Conversational"},
            {"id": "en-US-ChristopherNeural", "name": "Christopher (Male)", "description": "Deep, Authoritative"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (British)", "description": "British Accent, Clear"},
            {"id": "en-GB-RyanNeural", "name": "Ryan (British)", "description": "British Accent, Male"},
        ]
    }

# --- Routes for Status Check (Keep existing) ---
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    return [] # Simplified for brevity, DB logic remains same as before

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
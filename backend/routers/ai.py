from fastapi import APIRouter
from memory import get_memory
from services.ai_service import (
    start_ai,
    chat_ai,
    stop_ai,
    clear_ai,
    get_ai_status as get_service_status
)
from transcript import get_transcript
from models.chat import ChatRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI Voice Agent"]
)


@router.get("/status")
def get_ai_status():

    return {
        "status": get_service_status(),
        "microphone": "Connected",
        "backend": "Online",
        "live_calls": 1,
        "calls_today": 12,
        "bookings_today": 8,
        "success_rate": 92,
        "avg_response": "420 ms",
        "avg_call_duration": "3m 40s"
    }

@router.get("/memory")
def get_ai_memory():
    return get_memory()

@router.get("/transcript")
def get_ai_transcript():

    return get_transcript()

@router.post("/start")
def start_ai_agent():

    result = start_ai()

    return result

@router.post("/chat")
def chat_with_ai(request: ChatRequest):

    result = chat_ai(request.message)

    return result

@router.post("/stop")
def stop_ai_agent():

    return stop_ai()

@router.post("/clear")
def clear_ai_agent():

    return clear_ai()
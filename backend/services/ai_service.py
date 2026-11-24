from main import process_audio, process_text
from memory import clear_memory
from transcript import clear_transcript

ai_status = "Offline"


def start_ai():

    global ai_status

    ai_status = "Listening"

    result = process_audio()

    return result

def chat_ai(message: str):

    global ai_status

    ai_status = "Listening"

    result = process_text(message)

    return result


def stop_ai():

    global ai_status

    ai_status = "Offline"

    return {
        "message": "AI stopped successfully."
    }

def clear_ai():

    global ai_status

    clear_memory()

    clear_transcript()

    ai_status = "Offline"

    return {
        "message": "AI conversation cleared successfully."
    }


def get_ai_status():

    return ai_status
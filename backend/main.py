
from stt import transcribe_audio
from transcript import add_message
from intent import detect_intent
from entity import extract_entities
from memory import (
    save_memory,
    get_memory,
    clear_memory,
    set_confirmation_pending,
    clear_confirmation_pending,
    set_active_field
)
from handlers.cancel_handler import handle_cancel
from handlers.reschedule_handler import handle_reschedule
from handlers.view_handler import handle_view
from appointments_db import get_available_doctors_today
from conversation import get_missing_fields
from record_audio import record_audio
from appointments_db import save_booking
from appointments_db import get_available_slots


def process_text(text: str):

    add_message("patient", text)

    if not text.strip() or text.strip() == ".":

        return {
            "text": text,
            "intent": None,
            "entities": {},
            "memory": get_memory(),
            "missing": None,
            "response": "I couldn't understand your request. Could you please repeat it?",
            "follow_up": None,
        }

    memory = get_memory()

    print("\nCurrent Memory:", memory)

    print("Memory before intent detection:", memory)

    stored_intent = memory.get("intent")

    new_intent = detect_intent(text)

    if new_intent:
        intent = new_intent
        save_memory("intent", intent)

    elif stored_intent:
        intent = stored_intent

    else:
        intent = None

    mode = "all"

    if intent == "book_appointment" and memory.get("active_field"):
        mode = "single"

    entities = extract_entities(text, mode=mode)

    for key, value in entities.items():

        if value:
            save_memory(key, value)

    memory = get_memory()

    # ------------------------------------------
    # APPOINTMENT MANAGEMENT INTENTS
    # ------------------------------------------

    if intent == "cancel_appointment":

        result = handle_cancel(memory)

        response = result["reply"]

        add_message("ai", response)

        return {
            "text": text,
            "intent": intent,
            "entities": entities,
            "memory": get_memory(),
            "missing": None,
            "response": response,
            "follow_up": None
        }


    elif intent == "reschedule_appointment":

        result = handle_reschedule(memory, text)

        response = result["reply"]

        add_message("ai", response)

        return {
            "text": text,
            "intent": intent,
            "entities": entities,
            "memory": get_memory(),
            "missing": None,
            "response": response,
            "follow_up": None
        }


    elif intent == "view_appointments":

        result = handle_view(memory)

        response = result["reply"]

        add_message("ai", response)

        return {
            "text": text,
            "intent": intent,
            "entities": entities,
            "memory": get_memory(),
            "missing": None,
            "response": response,
            "follow_up": None
        }

    print("\nCurrent Memory:", memory)

    missing = get_missing_fields(memory)

    print("Intent:", intent)
    print("Missing:", missing)
    print("Missing Type:", type(missing))

    follow_up = None
    response = None
    booking = None
    memory_snapshot = memory

    questions = {
        "date": "What date would you like to book the appointment?",
        "time": "What time would you prefer?",
        "doctor": "Which doctor or specialization would the patient like to consult?",
        "patient_name": "What is the patient's name?",
        "phone": "What is the patient's contact number?"
    }

    print("Intent:", intent)
    print("Missing:", missing)

    if missing is None:

        if intent == "greeting":
            response = "Hello! How can I help you today?"

        elif intent == "available_doctors":

            available_doctors = get_available_doctors_today()

            if available_doctors:

                doctor_list = ""

                for doctor in available_doctors:

                    doctor_list += (
                        f"• Dr. {doctor['name']} - "
                        f"{doctor['specialization']}\n"
                    )

                response = (
                    "Doctors available today:\n\n"
                    f"{doctor_list}\n"
                    "Which doctor would you like to consult?"
                )

            else:

                response = (
                    "No doctors are available today."
                )

        elif intent == "exit":
            response = "Goodbye! Have a great day."

        else:
            response = "I'm here to help you with hospital appointments. How can I assist you today?"

    elif missing:

        set_active_field(missing[0])

        response = questions[missing[0]]

    else:
        if not memory.get("confirmation_pending"):

            set_confirmation_pending()

            response = (
                "Please confirm your appointment details.\n\n"
                f"Doctor: {memory['doctor']}\n"
                f"Date: {memory['date']}\n"
                f"Time: {memory['time']}\n"
                f"Patient: {memory['patient_name']}\n"
                f"Phone: {memory['phone']}\n\n"
                "Reply with 'Yes' to confirm or 'No' to cancel."
            )

        else:

            answer = text.strip().lower()

            if any(word in answer for word in [
                "yes",
                "confirm",
                "confirmed",
                "sure",
                "okay",
                "ok"
            ]):

                booking = save_booking(
                    memory["doctor"],
                    memory["date"],
                    memory["time"],
                    memory["patient_name"],
                    memory["phone"]
                )

            elif any(word in answer for word in [
                "no",
                "cancel",
                "stop"
            ]):

                clear_confirmation_pending()

                clear_memory()

                response = "Appointment booking has been cancelled."

            else:

                response = "Please reply with 'Yes' to confirm or 'No' to cancel."

            if booking:

                if booking["success"]:

                    clear_confirmation_pending()

                    response = (
                        f"Appointment booked successfully!\n"
                        f"Booking ID: {booking['data']['booking_id']}\n"
                        f"Patient: {booking['data']['name']}\n"
                        f"Doctor: {booking['data']['doctor']}\n"
                        f"Date: {booking['data']['date']}\n"
                        f"Time: {booking['data']['time']}"
                    )

                    memory_snapshot = memory.copy()

                    clear_memory()

                else:

                    if booking["message"] == "Selected appointment time is outside hospital working hours.":

                        save_memory("time", None)

                        set_active_field("time")

                        available_slots = get_available_slots(
                            memory["doctor"],
                            memory["date"]
                        )

                        slots_text = "\n".join(
                            f"• {slot}" for slot in available_slots
                        )

                        response = (
                            f"{booking['message']}\n\n"
                            "Available appointment times:\n\n"
                            f"{slots_text}\n\n"
                            "Please choose one of the available times."
                        )

                    else:

                        response = booking["message"]

    
    if response:
        add_message("ai", response)

    return {
        "text": text,
        "intent": intent,
        "entities": entities,
        "memory": memory_snapshot if booking and booking["success"] else memory,
        "missing": missing,
        "response": response,
        "follow_up": follow_up
    }

def process_audio():

    audio_file = record_audio()

    if not audio_file:
        return None

    text = transcribe_audio()

    if not text or not text.strip():
        print("\nNo speech recognized.")
        return None

    return process_text(text)


def run_cli():

    print("\n========================================")
    print("     AI VOICE APPOINTMENT ASSISTANT")
    print("========================================")
    print("Say 'exit' or 'goodbye' to end.")
    print("========================================")

    while True:

        try:

            result = process_audio()

            # ------------------------------------------
            # NO VALID AUDIO / TRANSCRIPTION
            # ------------------------------------------

            if result is None:
                print("\nNo valid speech detected.")
                print("Listening again...")
                continue

            # ------------------------------------------
            # DISPLAY RESULT
            # ------------------------------------------

            print("\n========== AI RESULT ==========")

            print("\nRecognized Text:")
            print(result["text"])

            print("\nDetected Intent:")
            print(result["intent"])

            print("\nEntities:")
            print(result["entities"])

            print("\nMemory:")
            print(result["memory"])

            print("\nMissing Fields:")
            print(result["missing"])

            if result["follow_up"]:
                print("\nFollow Up Question:")
                print(result["follow_up"])

            if result["response"]:
                print("\nAI Response:")
                print(result["response"])

            # ------------------------------------------
            # EXIT
            # ------------------------------------------

            if result["intent"] == "exit":

                print("\n========================================")
                print("Voice session ended.")
                print("========================================")

                break

            print("\n----------------------------------------")
            print("Listening for your next message...")
            print("----------------------------------------")

        except KeyboardInterrupt:

            print("\n\nVoice session stopped by user.")
            break

        except Exception as e:

            print("\nERROR:", e)
            print("Continuing voice session...\n")


if __name__ == "__main__":
    run_cli()
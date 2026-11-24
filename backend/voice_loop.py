from time_utils import extract_time
from memory import save_memory, get_memory, clear_memory
from intent import detect_intent
from entity import extract_entities
from record_audio import record_audio
from stt import transcribe_audio
from tts import speak
from llm import generate_response
from handlers.view_handler import handle_view
from conversation_engine import process_message
from handlers.slot_handler import (
    handle_slot
)
from handlers.confirmation_handler import (
    handle_confirmation
)
from handlers.reschedule_handler import (
    handle_reschedule
)
from handlers.cancel_handler import (
    handle_cancel
)
from handlers.booking_handler import (
    handle_booking
)
from appointments_db import (
    save_booking,
    cancel_booking,
    get_bookings_by_phone,
    update_booking,
    get_next_available_slots,
    update_completed_appointments
)
from patient_utils import (
    extract_phone,
    is_valid_phone
)


clear_memory()

update_completed_appointments()

speak("Hello! How can I help you today?")
while True:

    record_audio()

    user_input = transcribe_audio()

    print("\nYou:", user_input)

    command = user_input.lower().strip().replace(".", "")

    if command in ["exit", "quit", "stop"]:
        speak("Goodbye.")
        break

    if command == "reset":
        clear_memory()
        speak("Memory cleared.")
        continue

    process_message(user_input)

    memory = get_memory()

    text = user_input.lower()


    if (
        "cancel" in text
        or "delete" in text
    ):
        save_memory(
            "intent",
            "cancel_appointment"
        )

    elif (
        "change" in text
        or "reschedule" in text
    ):
        print(">>> RESCHEDULE INTENT DETECTED <<<")

        save_memory(
            "intent",
            "reschedule_appointment"
        )


    elif (
        "my appointment" in text
        or "my appointments" in text
        or "show appointment" in text
        or "show appointments" in text
        or "view appointment" in text
        or "view appointments" in text
    ):

        print(">>> VIEW INTENT DETECTED <<<")
        
        save_memory("intent", "view_appointments")

    

    elif (
        "appointment" in user_input.lower()
        and "cancel" not in user_input.lower()
        and "delete" not in user_input.lower()
        and not memory.get("waiting_for_cancel_selection")
    ):
        save_memory(
            "intent",
            "book_appointment"
        )


    doctors = [
        "cardiologist",
        "neurologist",
        "dentist",
        "physician"
    ]

    for doctor in doctors:
        if doctor in user_input.lower():
            save_memory("doctor", doctor)

    memory = get_memory()

    print("\nMemory:", memory)

    if memory.get("waiting_for_cancel_selection"):

        text = user_input.lower()

        selected_index = None

        if (
            "first" in text
            or text.strip() == "1"
            or "one" in text
        ):
            selected_index = 0

        elif (
            "second" in text
            or text.strip() == "2"
            or "two" in text
        ):
            selected_index = 1

        elif (
            "third" in text
            or text.strip() == "3"
            or "three" in text
        ):
            selected_index = 2

        if selected_index is not None:

            candidates = memory["cancel_candidates"]

            if selected_index < len(candidates):

                selected_booking = candidates[selected_index]

                cancelled = cancel_booking(
                    selected_booking["booking_id"]
                )

                if cancelled:

                    speak(
                        "Appointment cancelled successfully."
                    )

                else:

                    speak(
                        "Unable to cancel the appointment."
                    )

                clear_memory()

                break

            else:

                speak(
                    "Invalid appointment selection."
                )

        else:

            speak(
                "Please say first, second or third appointment."
            )

        continue

    if memory.get("intent") == "reschedule_appointment":

        completed = handle_reschedule(
            memory,
            speak
        )

        if completed:
            break

        continue

    if memory.get("intent") == "view_appointments":

        response = handle_view(
            memory
        )

        if response:

            speak(
                response["reply"]
            )

            if response.get("completed"):
                break

        continue

    if memory.get("intent") == "cancel_appointment":

        response = handle_cancel(
            memory
        )

        if response:

            speak(
                response["reply"]
            )

            if response.get("completed"):
                break

        continue
    
    if (
        "cancel" in user_input.lower()
        or "delete" in user_input.lower()
    ):

        words = user_input.split()

        for word in words:

            if word.startswith("APPT"):

                cancelled = cancel_booking(word)

                if cancelled:

                    speak(
                        f"Appointment {word} cancelled successfully."
                    )

                else:

                    speak(
                        f"Appointment {word} not found."
                    )

                break

        continue

    if memory.get("waiting_for_confirmation"):

        response = handle_confirmation(
            memory,
            user_input
        )

        if response:

            speak(response["reply"])

            if response["completed"]:
                break

        continue


    if memory.get("waiting_for_name"):

        name = user_input.strip().replace(".", "").strip()

        if not name:

            speak(
                "I didn't catch your name. Please tell me your name again."
            )

            continue

        save_memory(
            "name",
            name
        )

        save_memory(
            "waiting_for_name",
            False
        )

        speak(
            "Please provide your phone number."
        )

        save_memory(
            "waiting_for_phone",
            True
        )

        save_memory(
            "phone_request_for",
            None
        )

        continue

    if memory.get("waiting_for_phone"):

        phone = extract_phone(user_input)

        if not phone or not is_valid_phone(phone):

            speak(
                "Please provide a valid 10 digit phone number."
            )

            continue

        save_memory(
            "phone",
            phone
        )

        save_memory(
            "waiting_for_phone",
            False
        )

        memory = get_memory()

        memory = get_memory()

        if memory.get("phone_request_for") == "view":

            save_memory(
                "phone_request_for",
                None
            )

            response = handle_view(
                memory
            )

            if response:

                speak(
                    response["reply"]
                )

                if response.get("completed"):
                    break

            continue


        if memory.get("phone_request_for") == "cancel":

            save_memory(
                "phone_request_for",
                None
            )

            response = handle_cancel(
                memory
            )

            if response:

                speak(
                    response["reply"]
                )

                if response.get("completed"):
                    break

            continue


        if memory.get("intent") == "book_appointment":

            response = handle_booking(
                memory
            )

            if response:

                speak(
                    response["reply"]
                )

            continue
        

    if memory.get("waiting_for_slot"):

        response = handle_slot(
            memory,
            user_input
        )

        if response:

            speak(
                response["reply"]
            )

        continue
    

    if memory.get("intent") == "book_appointment":

        response = handle_booking(
            memory
        )


        if response:

            speak(
                response["reply"]
            )

        continue
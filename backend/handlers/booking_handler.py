from appointments_db import (
    is_doctor_available,
    get_next_available_slots
)
from response import success_reply

from memory import (
    save_memory
)


def handle_booking(
    memory
):

    if "date" not in memory:
        return success_reply(
            "What date would you like to book the appointment?"
        )


    elif "time" not in memory:

        return success_reply(
            "What time would you like?"
        )


    elif "doctor" not in memory:

        return success_reply(
            "Which doctor would you like to book an appointment with?"
        )


    available = is_doctor_available(
        memory["doctor"],
        memory["date"],
        memory["time"]
    )

    if available:

        if "name" not in memory:

            save_memory(
                "waiting_for_name",
                True
            )

            return success_reply(
                "Please provide your name."
            )


        elif "phone" not in memory:

            save_memory(
                "waiting_for_phone",
                True
            )

            return success_reply(
                "Please provide your phone number."
            )


        else:

            save_memory(
                "waiting_for_confirmation",
                True
            )

            return success_reply(
                f"Please review the appointment details. "
                f"Name {memory['name']}. "
                f"Phone {memory['phone']}. "
                f"Doctor {memory['doctor']}. "
                f"Date {memory['date']}. "
                f"Time {memory['time']}. "
                f"Would you like me to book this appointment with the above details?"
            )


    else:

        slots = get_next_available_slots(
            memory["doctor"],
            memory["date"]
        )

        slot_text = ", ".join(slots)

        save_memory(
            "waiting_for_slot",
            True
        )

        return success_reply(
            f"Sorry. {memory['doctor']} is not available at "
            f"{memory['time']}. "
            f"Available slots are {slot_text}. "
            f"Which slot would you like?"
        )

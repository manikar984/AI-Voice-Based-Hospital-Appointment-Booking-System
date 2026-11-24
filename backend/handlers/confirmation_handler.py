from memory import (
    save_memory,
    clear_memory
)
from response import success_reply
from appointments_db import (
    save_booking
)


def handle_confirmation(
    memory,
    user_input
):

    if any(
        word in user_input.lower()
        for word in [
            "yes",
            "ok",
            "okay",
            "confirm"
        ]
    ):

        booking = save_booking(
            memory["doctor"],
            memory["date"],
            memory["time"],
            memory["name"],
            memory["phone"]
        )

        if not booking["success"]:

            if booking["status"] == "working_hours":

                save_memory(
                    "waiting_for_confirmation",
                    False
                )

                save_memory(
                    "waiting_for_slot",
                    True
                )

                slot_text = ", ".join(
                    booking["available_slots"][:3]
                )

                return success_reply(
                    f"{booking['message']} "
                    f"Available slots are {slot_text}. "
                    f"Which time would you like me to book?"
                )


            elif booking["status"] == "doctor_unavailable":

                save_memory(
                    "waiting_for_confirmation",
                    False
                )

                save_memory(
                    "waiting_for_slot",
                    True
                )

                slot_text = ", ".join(
                    booking["available_slots"]
                )

                return success_reply(
                    f"{booking['message']} "
                    f"Available slots are {slot_text}. "
                    f"Which time would you like me to book?"
                )


            else:

                return success_reply(
                    booking["message"]
                )


        clear_memory()

        return success_reply(
            f"Great. Your appointment is confirmed. "
            f"Booking ID is {booking['data']['booking_id']}.",
            completed=True
        )

        


    elif any(
        word in user_input.lower()
        for word in [
            "no",
            "cancel"
        ]
    ):

        clear_memory()

        return success_reply(
            "Appointment booking cancelled.",
            completed=True
        )

        


    else:

        return success_reply(
            "Please say yes to confirm or no to cancel."
        )

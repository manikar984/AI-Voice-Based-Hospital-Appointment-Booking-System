from appointments_db import get_bookings_by_phone
from response import success_reply
from memory import (
    save_memory,
    clear_memory
)

def handle_view(memory):

    if "phone" not in memory:

        save_memory(
            "waiting_for_phone",
            True
        )

        save_memory(
            "phone_request_for",
            "view"
        )

        return success_reply(
            "Please provide your phone number."
        )

    bookings = get_bookings_by_phone(
        memory["phone"]
    )

    if bookings:

        reply = ""

        for booking in bookings:

            reply += (
                f"Booking ID {booking['booking_id']}. "
                f"Doctor {booking['doctor']}. "
                f"Date {booking['date']}. "
                f"Time {booking['time']}.\n\n"
            )

        clear_memory()

        return success_reply(
            reply.strip(),
            completed=True
        )

    clear_memory()

    return success_reply(
        "No appointments found for this phone number.",
        completed=True
    )
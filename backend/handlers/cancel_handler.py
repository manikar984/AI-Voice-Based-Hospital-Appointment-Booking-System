from appointments_db import (
    get_bookings_by_phone,
    cancel_booking
)
from response import success_reply
from memory import (
    save_memory,
    clear_memory
)


def handle_cancel(
    memory
):

    if "phone" not in memory:

        save_memory(
            "waiting_for_phone",
            True
        )

        save_memory(
            "phone_request_for",
            "cancel"
        )

        return success_reply(
            "Please provide your phone number."
        )

    bookings = get_bookings_by_phone(
        memory["phone"]
    )

    if len(bookings) == 1:

        booking = bookings[0]

        message = (
            f"I found one appointment. "
            f"Doctor {booking['doctor']}. "
            f"Date {booking['date']}. "
            f"Time {booking['time']}. "
            f"Cancelling your appointment. "
        )

        cancelled = cancel_booking(
            booking["booking_id"]
        )

        if cancelled:

            clear_memory()

            return success_reply(
                message + "Appointment cancelled successfully.",
                completed=True
            )

        else:

            clear_memory()

            return success_reply(
                "Unable to cancel the appointment.",
                completed=True
            )



    elif len(bookings) > 1:

        reply = "I found these appointments.\n\n"

        for index, booking in enumerate(
            bookings,
            start=1
        ):

            reply += (
                f"Appointment {index}. "
                f"Doctor {booking['doctor']}. "
                f"Date {booking['date']}. "
                f"Time {booking['time']}.\n\n"
            )

        save_memory(
            "cancel_candidates",
            bookings
        )

        save_memory(
            "waiting_for_cancel_selection",
            True
        )

        reply += "Which appointment would you like to cancel?"

        return success_reply(reply)

    else:

        clear_memory()

        return success_reply(
            "No appointments found.",
            completed=True
        )
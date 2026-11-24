from appointments_db import (
    get_bookings_by_phone,
    update_booking,
    is_doctor_available,
    get_available_slots
)

from response import success_reply

from memory import (
    save_memory,
    clear_memory
)


def handle_reschedule(memory, user_input):

    # -------------------------------------------------
    # STEP 1: Get patient's phone number
    # -------------------------------------------------

    if (
        not memory.get("waiting_for_reschedule_date")
        and not memory.get("waiting_for_reschedule_time")
    ):

        if "phone" not in memory:

            save_memory(
                "waiting_for_phone",
                True
            )

            save_memory(
                "phone_request_for",
                "reschedule"
            )

            return success_reply(
                "Please provide your phone number."
            )

        bookings = get_bookings_by_phone(
            memory["phone"]
        )

        if len(bookings) == 0:

            clear_memory()

            return success_reply(
                "No appointments found.",
                completed=True
            )

        elif len(bookings) == 1:

            booking = bookings[0]

            save_memory(
                "reschedule_booking",
                booking
            )

            save_memory(
                "waiting_for_reschedule_date",
                True
            )

            return success_reply(
                f"I found one appointment. "
                f"Doctor {booking['doctor']}. "
                f"Date {booking['date']}. "
                f"Time {booking['time']}. "
                f"What new date would you like?"
            )

        else:

            return success_reply(
                "You have multiple appointments. "
                "Please select which appointment you would like to reschedule."
            )


    # -------------------------------------------------
    # STEP 2: Get new date
    # -------------------------------------------------

    if memory.get("waiting_for_reschedule_date"):

        if "date" in memory:

            new_date = memory["date"]

            save_memory(
                "new_date",
                new_date
            )

            save_memory(
                "waiting_for_reschedule_date",
                False
            )

            save_memory(
                "waiting_for_reschedule_time",
                True
            )

            return success_reply(
                "What new time would you like?"
            )

        else:

            return success_reply(
                "Please tell me the new appointment date."
            )


    # -------------------------------------------------
    # STEP 3: Get new time
    # -------------------------------------------------

    if memory.get("waiting_for_reschedule_time"):

        booking = memory.get("reschedule_booking")

        if not booking:

            clear_memory()

            return success_reply(
                "I couldn't find the appointment to reschedule.",
                completed=True
            )

        # ---------------------------------------------
        # User says "same"
        # ---------------------------------------------

        lower_input = user_input.strip().lower()

        same_time_words = [
            "same",
            "same time",
            "keep same time",
            "keep the same time",
            "same as before",
            "unchanged"
        ]

        if lower_input in same_time_words:

            new_time = booking["time"]

        else:

            if "time" not in memory:

                return success_reply(
                    "Please tell me the new appointment time."
                )

            new_time = memory["time"]


        # ---------------------------------------------
        # New date
        # ---------------------------------------------

        new_date = memory.get("new_date")

        if not new_date:

            return success_reply(
                "Please tell me the new appointment date."
            )


        # ---------------------------------------------
        # Check availability for:
        #
        # doctor + NEW DATE + NEW TIME
        # ---------------------------------------------

        available = is_doctor_available(
            booking["doctor"],
            new_date,
            new_time
        )


        # ---------------------------------------------
        # If unavailable, show slots for NEW DATE
        # ---------------------------------------------

        if not available:

            slots = get_available_slots(
                booking["doctor"],
                new_date
            )

            if slots:

                return success_reply(
                    f"{new_time} is not available on {new_date}. "
                    f"Available slots are {', '.join(slots)}. "
                    f"Which time would you like?"
                )

            else:

                return success_reply(
                    f"{new_time} is not available on {new_date}. "
                    "There are no available slots for that date."
                )


        # ---------------------------------------------
        # Update appointment
        # ---------------------------------------------

        updated = update_booking(
            booking["booking_id"],
            new_date,
            new_time
        )


        if updated:

            clear_memory()

            return success_reply(
                f"Your appointment has been rescheduled successfully. "
                f"New date: {new_date}. "
                f"New time: {new_time}.",
                completed=True
            )

        else:

            clear_memory()

            return success_reply(
                "Unable to reschedule your appointment.",
                completed=True
            )


    return success_reply(
        "I couldn't process the reschedule request."
    )
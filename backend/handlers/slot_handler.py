from memory import (
    save_memory,
    get_memory
)

from appointments_db import (
    get_next_available_slots
)

from time_utils import (
    extract_time
)

from response import success_reply


def handle_slot(
    memory,
    user_input
):

    selected_time = extract_time(user_input)

    if selected_time:

        available_slots = get_next_available_slots(
            memory["doctor"],
            memory["date"]
        )

        if selected_time not in available_slots:

            slot_text = ", ".join(available_slots)

            return success_reply(
                f"{selected_time} is not available. "
                f"Please choose one of these: {slot_text}."
            )

        save_memory(
            "time",
            selected_time
        )

        save_memory(
            "waiting_for_slot",
            False
        )

        memory = get_memory()

        return success_reply(
            f"You selected {selected_time}."
        )

    else:

        return success_reply(
        "Please choose one of the available time slots."
    )
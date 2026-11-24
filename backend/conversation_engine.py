from memory import (
    save_memory,
    get_memory,
    clear_memory
)

from intent import detect_intent
from entity import extract_entities
from patient_utils import (
    extract_phone,
    is_valid_phone
)


def process_message(user_input: str):

    memory = get_memory()

    if memory.get("waiting_for_confirmation"):

        entities = {}

    elif memory.get("waiting_for_slot"):

        entities = extract_entities(
            user_input,
            mode="time"
        )

    else:

        entities = extract_entities(
            user_input
        )

    for key, value in entities.items():

        save_memory(key, value)

    phone = extract_phone(user_input)

    if is_valid_phone(phone):

        save_memory("phone", phone)

    intent = detect_intent(user_input)

    if intent:

        save_memory(
            "intent",
            intent
        )

    return get_memory()
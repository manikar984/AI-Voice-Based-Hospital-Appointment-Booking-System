def get_missing_fields(memory):

    intent = memory.get("intent")

    if intent != "book_appointment":
        return None

    missing = []

    required = [
    "date",
    "time",
    "doctor",
    "patient_name",
    "phone"
]

    for field in required:

        if not memory.get(field):
            missing.append(field)

    return missing
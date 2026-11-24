from memory import save_memory, get_memory

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    if "am" in user_input.lower() or "pm" in user_input.lower():
        save_memory("time", user_input)

    elif "tomorrow" in user_input.lower():
        save_memory("date", "tomorrow")

    doctors = [
        "cardiologist",
        "neurologist",
        "dentist",
        "physician"
    ]

    for doctor in doctors:
        if doctor in user_input.lower():
            save_memory("doctor", doctor)

    print("Memory:", get_memory())
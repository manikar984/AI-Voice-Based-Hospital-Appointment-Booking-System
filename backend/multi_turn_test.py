from memory import save_memory, get_memory

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    if "tomorrow" in user_input.lower():
        save_memory("date", "tomorrow")

    if "am" in user_input.lower() or "pm" in user_input.lower():
        save_memory("time", user_input)

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

    if "date" not in memory:
        print("AI: Which day would you like the appointment?")

    elif "time" not in memory:
       print("AI: What time would you like?")

    elif "doctor" not in memory:
       print("AI: Which doctor would you like to consult?")

    else:
       print("AI: Great. I have all the information.")
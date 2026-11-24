def handle_appointment(entities):

    doctor = entities.get("doctor", "doctor")
    date = entities.get("date", "unknown date")
    time = entities.get("time", "unknown time")

    return (
        f"I found an appointment request with a "
        f"{doctor} on {date} at {time}."
    )
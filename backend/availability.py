appointments = {
    "neurologist": [
        "10:00 AM",
        "11:00 AM",
        "03:00 PM"
    ],

    "dentist": [
        "09:00 AM",
        "01:00 PM"
    ],

    "cardiologist": [
        "10:00 AM",
        "02:00 PM"
    ]
}

def check_availability(doctor, time):

    if doctor not in appointments:
        return False

    return time in appointments[doctor]

def get_available_slots(doctor):

    return appointments.get(
        doctor,
        []
    )
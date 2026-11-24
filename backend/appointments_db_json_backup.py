import json

FILE_NAME = "bookings.json"


def save_booking(doctor,date,time,name,phone):

    bookings = get_bookings()

    booking_id = f"APPT{len(bookings) + 1:03d}"

    booking = {
        "booking_id": booking_id,
        "name": name,
        "phone": phone,
        "doctor": doctor,
        "date": date,
        "time": time
    }

    bookings.append(booking)

    with open(FILE_NAME, "w") as file:
        json.dump(
            bookings,
            file,
            indent=4
        )

    return booking


def get_bookings():

    try:

        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

def cancel_booking(booking_id):

    bookings = get_bookings()

    updated_bookings = []

    found = False

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            found = True

        else:

            updated_bookings.append(booking)

    if found:

        with open(FILE_NAME, "w") as file:

            json.dump(
                updated_bookings,
                file,
                indent=4
            )

    return found

def get_bookings_by_phone(phone):

    bookings = get_bookings()

    results = []

    for booking in bookings:

        if booking.get("phone") == phone:

            results.append(booking)

    return results

def get_bookings_by_phone(phone):

    bookings = get_bookings()

    results = []

    for booking in bookings:

        if booking.get("phone") == phone:

            results.append(booking)

    return results

def get_bookings_by_phone(phone):

    bookings = get_bookings()

    results = []

    for booking in bookings:

        if booking.get("phone") == phone:

            results.append(booking)

    return results

def update_booking(booking_id, new_date, new_time):

    bookings = get_bookings()

    updated = False

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            booking["date"] = new_date
            booking["time"] = new_time

            updated = True

            break

    if updated:

        with open(FILE_NAME, "w") as file:

            json.dump(
                bookings,
                file,
                indent=4
            )

    return updated
import json

from database import get_connection

FILE_NAME = "bookings.json"


def migrate():

    try:

        with open(FILE_NAME, "r") as file:

            bookings = json.load(file)

    except FileNotFoundError:

        print("bookings.json not found.")

        return

    connection = get_connection()

    cursor = connection.cursor()

    migrated = 0

    for booking in bookings:

        cursor.execute(
            """
            INSERT INTO appointments
            (name, phone, doctor, date, time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                booking.get("name", ""),
                booking.get("phone", ""),
                booking.get("doctor", ""),
                booking.get("date", ""),
                booking.get("time", "")
            )
        )

        migrated += 1

    connection.commit()

    connection.close()

    print(f"{migrated} appointments migrated successfully.")


if __name__ == "__main__":

    migrate()
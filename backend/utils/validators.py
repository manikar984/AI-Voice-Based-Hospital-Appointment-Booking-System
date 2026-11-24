import re
from datetime import datetime


def is_valid_phone(phone):

    return bool(
        re.fullmatch(
            r"\d{10}",
            phone
        )
    )


def is_valid_booking_id(booking_id):

    return bool(
        re.fullmatch(
            r"APPT\d+",
            booking_id.upper()
        )
    )


def is_valid_date(date):

    try:

        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

        return True

    except ValueError:

        return False


def is_valid_time(time):

    try:

        datetime.strptime(
            time,
            "%I:%M %p"
        )

        return True

    except ValueError:

        return False
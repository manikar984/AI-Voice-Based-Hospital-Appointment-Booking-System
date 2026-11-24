import re
import dateparser
from datetime import datetime, timedelta

def extract_date(text):

    text = text.lower()

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    for day in weekdays:

        if f"next {day}" in text:

            today = datetime.now()

            target_day = weekdays[day]

            days_ahead = target_day - today.weekday()

            if days_ahead <= 0:
                days_ahead += 7

            result = today + timedelta(days=days_ahead)

            return result.strftime("%Y-%m-%d")

    patterns = [
        "today",
        "tomorrow",
        "yesterday",
        "day after tomorrow"
    ]

    for pattern in patterns:

        if pattern in text:

            result = dateparser.parse(
                pattern,
                settings={"PREFER_DATES_FROM": "future"}
            )

            if result:
                return result.strftime("%Y-%m-%d")

    date_match = re.search(
        r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
        text
    )

    if date_match:

        result = dateparser.parse(date_match.group())

        if result:
            return result.strftime("%Y-%m-%d")

    time_only_pattern = re.fullmatch(
        r"(\d{1,2}([:.]\d{2})?\s*(am|pm)?)",
        text.strip()
    )

    if time_only_pattern:
        return None

    result = dateparser.parse(
        text,
        settings={"PREFER_DATES_FROM": "future"}
    )

    if text.strip().isdigit():
        return None

    if result:
        return result.strftime("%Y-%m-%d")

    return None
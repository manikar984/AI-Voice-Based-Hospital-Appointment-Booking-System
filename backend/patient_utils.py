import re


def extract_phone(text):

    match = re.search(
        r"\b\d{10}\b",
        text
    )

    if match:
        return match.group()

    return None

def is_valid_phone(phone):

    return (
        phone is not None
        and len(phone) == 10
        and phone.isdigit()
    )

def extract_name(text):

    words = text.strip().split()

    if (
        len(words) == 1
        and words[0].replace(".", "").isalpha()
    ):
        return words[0].replace(".", "").title()

    return None
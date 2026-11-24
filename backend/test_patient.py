from patient_utils import (
    extract_phone,
    is_valid_phone,
    extract_name
)

while True:

    text = input("Text: ")

    if text.lower() == "exit":
        break

    name = extract_name(text)

    phone = extract_phone(text)

    print("Name:", name)

    print("Phone:", phone)

    print(
        "Valid:",
        is_valid_phone(phone)
    )
import dateparser

while True:

    text = input("Date: ")

    if text == "exit":
        break

    result = dateparser.parse(
        text,
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    print(result)
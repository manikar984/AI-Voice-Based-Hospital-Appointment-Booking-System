from date_utils import extract_date

while True:

    text = input("Date: ")

    if text == "exit":
        break

    print(extract_date(text))
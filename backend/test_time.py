from time_utils import extract_time

while True:

    text = input("Time: ")

    if text == "exit":
        break

    print(extract_time(text))
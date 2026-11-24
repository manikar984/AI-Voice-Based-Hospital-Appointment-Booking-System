from entity import extract_entities

while True:

    text = input("Text: ")

    if text == "exit":
        break

    print(extract_entities(text))
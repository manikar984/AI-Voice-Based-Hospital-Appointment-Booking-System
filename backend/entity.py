import re
from date_utils import extract_date
from time_utils import extract_time
from database import get_all_doctors
from memory import get_active_field
from llm import extract_patient_name

def extract_entities(
    text,
    mode="all"
):

    entities = {}

    active_field = get_active_field()

    if mode == "all" or active_field == "date":

        date = extract_date(text)

        if date:
            entities["date"] = date

    if mode == "all" or active_field == "doctor":

        doctors = get_all_doctors()

        text_lower = text.lower()

        print("Doctors from DB:", doctors)
        print("Input Text:", text)
        print("Text Lower:", text_lower)

        for doctor in doctors:

            name = doctor["name"].lower()
            specialization = doctor["specialization"].lower()

            if re.search(rf"\b{re.escape(name)}\b", text_lower):
                entities["doctor"] = doctor["name"]
                break

            

            if re.search(rf"\b{re.escape(specialization)}\b", text_lower):
                entities["doctor"] = doctor["specialization"]
                break

            print(
                "Checking:",
                doctor["name"],
                "|",
                doctor["specialization"]
            )
        print("Entities after doctor extraction:", entities)


    if mode == "all" or active_field == "patient_name":

        patient_name = extract_patient_name(text)

        if patient_name:
            entities["patient_name"] = patient_name

    if mode == "all" or active_field == "phone":

        phone_match = re.search(r"[6-9][\d\s-]{9,12}", text)

        if phone_match:
            phone = re.sub(r"\D", "", phone_match.group())

            if len(phone) == 10:
                entities["phone"] = phone

    if mode == "all" or active_field == "time":

        time = extract_time(text)

        if time:
            entities["time"] = time
    return entities
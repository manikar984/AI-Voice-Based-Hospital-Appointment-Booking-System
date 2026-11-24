from database import get_all_doctors

doctors = get_all_doctors()

for doctor in doctors:
    print(dict(doctor))
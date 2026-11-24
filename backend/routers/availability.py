from fastapi import APIRouter

from appointments_db import get_available_slots

router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)




@router.get(
    "/{doctor}/{date}",
    summary="Check doctor availability",
    description="Returns the available appointment slots for a doctor on a given date."
)
def check_availability(
    doctor: str,
    date: str
):

    available_slots = get_available_slots(
        doctor,
        date
    )

    return {
        "doctor": doctor,
        "date": date,
        "available_slots": available_slots
    }
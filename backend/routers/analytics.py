from fastapi import APIRouter

from appointments_db import (
    get_status_analytics,
    get_doctor_analytics,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)




@router.get(
    "/status",
    summary="Appointment Status Analytics",
    description="Returns appointment counts grouped by status."
)
def appointment_status_analytics():

    return get_status_analytics()


@router.get(
    "/doctors",
    summary="Doctor Analytics",
    description="Returns appointment counts grouped by doctor."
)
def doctor_analytics():

    return get_doctor_analytics()
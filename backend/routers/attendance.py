from fastapi import APIRouter
from schemas import Attendance
from appointments_db import (
    mark_doctor_attendance,
    get_doctor_attendance,
    get_attendance_record
)
from datetime import datetime, time
from fastapi import HTTPException

router = APIRouter(
    prefix="/attendance",
    tags=["Doctor Attendance"]
)


@router.get("/{attendance_date}")
def get_attendance(
    attendance_date: str
):

    return get_doctor_attendance(
        attendance_date
    )


@router.post("")
def save_attendance(
    attendance: Attendance
):

    today = datetime.now().date()

    current_time = datetime.now().time()

    attendance_date = datetime.strptime(
        attendance.attendance_date,
        "%Y-%m-%d"
    ).date()

    if attendance_date != today:

        raise HTTPException(
            status_code=400,
            detail="Attendance can only be marked for today."
        )

    if not (
        time(1, 0) <= current_time < time(10, 0)
    ):

        raise HTTPException(
            status_code=400,
            detail="Attendance can only be updated between 1:00 AM and 10:00 AM."
        )

    existing_record = get_attendance_record(
        attendance.doctor_id,
        attendance.attendance_date
    )

    if existing_record:

        raise HTTPException(
            status_code=400,
            detail="Attendance has already been marked for today."
        )

    return mark_doctor_attendance(
        attendance.doctor_id,
        attendance.attendance_date,
        attendance.attendance_status,
        attendance.check_in_time,
        attendance.check_out_time
    )
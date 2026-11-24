from fastapi import APIRouter, HTTPException, status, Depends
import logging
from security import get_current_user, require_roles
from schemas import Appointment
from appointments_db import (
    get_bookings,
    get_bookings_by_phone,
    save_booking,
    update_booking_details,
    cancel_booking,
    update_completed_appointments,
    get_tomorrows_appointments

)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

logger = logging.getLogger(__name__)

@router.get(
    "",
    summary="Get all appointments",
    description="Returns a list of all appointments stored in the database."
)
def get_all_appointments(
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist",
            "doctor"
        )
    )
):
    return get_bookings()
@router.get(
    "/tomorrow",
    summary="Get tomorrow's appointments"
)
def tomorrow_appointments(
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist",
            "doctor"
        )
    )
):
    return get_tomorrows_appointments()


@router.get(
    "/{phone}",
    summary="Search appointments by phone number",
    description="Returns all appointments associated with the given phone number.",
    responses={
        200: {
            "description": "Appointments retrieved successfully"
        }
    }
)
def get_appointments_by_phone(
    phone: str,
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist",
            "doctor"
        )
    )
):

    return get_bookings_by_phone(phone)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new appointment",
    description="Creates a new appointment and stores it in the database.",
    responses={
        201: {
            "description": "Appointment created successfully"
        }
    }
)
def create_appointment(
    appointment: Appointment,
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist"
        )
    )
):

    booking = save_booking(
        appointment.doctor,
        appointment.date,
        appointment.time,
        appointment.name,
        appointment.phone
    )

    print(booking)

    if not booking.get("success"):

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=booking
        )

    logger.info(
        f"Appointment created: {booking['data']['booking_id']} "
        f"for {booking['data']['name']}"
    )

    return booking


@router.put(
    "/{booking_id}",
    summary="Update an appointment",
    description="Updates an existing appointment using its booking ID.",
    responses={
        404: {
            "description": "Appointment not found"
        }
    }
)
def update_appointment(
    booking_id: str,
    appointment: Appointment,
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist"
        )
    )
):

    updated = update_booking_details(
        booking_id,
        appointment.name,
        appointment.phone,
        appointment.doctor,
        appointment.date,
        appointment.time
    )

    if updated:

        logger.info(
            f"Appointment updated: {booking_id}"
        )

    if not updated:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found."
        )

    return {
        "message": "Appointment updated successfully."
    }


@router.delete(
    "/{booking_id}",
    summary="Delete an appointment",
    description="Deletes an appointment using its booking ID.",
    responses={
        404: {
            "description": "Appointment not found"
        }
    }
)
def delete_appointment(
    booking_id: str,
    current_user=Depends(
        require_roles(
            "admin"
        )
    )
):

    deleted = cancel_booking(
        booking_id
    )

    if deleted:

        logger.info(
            f"Appointment deleted: {booking_id}"
        )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found."
        )

    return {
        "message": "Appointment deleted successfully."
    }


@router.post(
    "/update-completed",
    summary="Update completed appointments"
)
def mark_completed_appointments(
    current_user=Depends(
        require_roles(
            "admin"
        )
    )
):

    updated = update_completed_appointments()

    return {
        "message": f"{updated} appointment(s) marked as completed."
    }

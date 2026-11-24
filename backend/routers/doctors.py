from fastapi import APIRouter, HTTPException, status

from schemas import Doctor

from appointments_db import (
    get_doctors,
    get_available_doctors_today,
    reactivate_doctor,
    save_doctor,
    update_doctor,
    delete_doctor,
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

@router.get(
    "",
    summary="Get all doctors",
    description="Returns all doctors."
)
def get_all_doctors():

    return get_doctors()

@router.get("/available/today")
def available_doctors_today():

    return get_available_doctors_today()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Add a doctor",
    description="Adds a new doctor to the database."
)
def create_doctor(
    doctor: Doctor
):
    try:

        return save_doctor(
            doctor.name,
            doctor.specialization,
            doctor.phone,
            doctor.email,
            doctor.experience,
            doctor.status
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the doctor."
        )


@router.put(
    "/{doctor_id}",
    summary="Update a doctor",
    description="Updates an existing doctor."
)
def edit_doctor(
    doctor_id: int,
    doctor: Doctor
):
    try:

        return update_doctor(
            doctor_id,
            doctor.name,
            doctor.specialization,
            doctor.phone,
            doctor.email,
            doctor.experience,
            doctor.status
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while updating the doctor."
        )


@router.delete(
    "/{doctor_id}",
    summary="Deactivate a doctor",
    description="Marks a doctor as Inactive instead of deleting."
)
def remove_doctor(
    doctor_id: int
):

    try:

        return delete_doctor(doctor_id)

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while deleting the doctor."
        )

@router.put("/reactivate/{doctor_id}")
def reactivate(doctor_id: int):

    reactivate_doctor(doctor_id)

    return {
        "message": "Doctor reactivated successfully"
    }
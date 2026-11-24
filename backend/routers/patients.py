from fastapi import APIRouter

from appointments_db import get_patients

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)





@router.get(
    "",
    summary="Get all patients",
    description="Returns a unique list of patients with appointment statistics."
)
def get_all_patients():

    return get_patients()
from fastapi import APIRouter
from appointments_db import get_doctor_analytics
from appointments_db import get_dashboard_summary

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/stats",
    summary="Dashboard Statistics",
    description="Returns summary statistics for the dashboard."
)
def dashboard_statistics():

    return get_dashboard_summary()

@router.get(
    "/analytics",
    summary="Analytics Statistics",
    description="Returns analytics statistics."
)
def analytics_statistics():

    return get_dashboard_summary()

@router.get("/doctor-analytics")
def doctor_analytics():
    return get_doctor_analytics()
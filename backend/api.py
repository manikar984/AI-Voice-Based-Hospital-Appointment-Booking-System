from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import HTTPException
from exception_handlers import http_exception_handler
from scheduler import start_scheduler
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers.auth import router as auth_router
from routers.appointments import router as appointments_router
from routers.ai import router as ai_router
from routers.doctors import router as doctors_router
from routers.patients import router as patients_router
from routers.dashboard import router as dashboard_router
from routers.analytics import router as analytics_router
from routers.availability import router as availability_router
from routers.attendance import router as attendance_router
logger = logging.getLogger(__name__)
from appointments_db import (
    update_completed_appointments,
    get_user_by_username,
    create_user
)

app = FastAPI(
    title="AI Clinical Appointment API",
    version="1.0.0",
    description="Backend API for AI Clinical Appointment Booking System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():

    if not get_user_by_username("admin"):

        create_user(
            username="admin",
            password="admin123",
            role="admin"
        )

        print("Default admin user created.")

    updated = update_completed_appointments()

    print(f"{updated} appointment(s) updated.")

    start_scheduler()

@app.get(
    "/",
    summary="API Home",
    description="Returns a welcome message indicating that the AI Clinical Appointment API is running."
)
def home():

    return {
        "message": "AI Clinical Appointment API is running"
    }




app.include_router(appointments_router)
app.include_router(doctors_router)
app.include_router(patients_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)
app.include_router(availability_router)
app.include_router(attendance_router)
app.include_router(auth_router)
app.include_router(ai_router)
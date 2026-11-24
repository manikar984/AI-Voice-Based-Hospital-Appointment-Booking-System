from typing import Literal
from datetime import date, time
from pydantic import BaseModel, Field, field_validator


class Appointment(BaseModel):

    name: str = Field(
    min_length=2,
    max_length=50,
    description="Patient's full name"
    )

    phone: str = Field(
    pattern=r"^\d{10}$",
    description="10-digit mobile number"
    )

    doctor: str = Field(
        min_length=2,
        max_length=50,
        description="Doctor specialization"
    )

    date: str
    
    time: str

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str):

        import datetime

        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Date must be in YYYY-MM-DD format."
            )

        return value

    @field_validator("time")
    @classmethod
    def validate_time(cls, value: str):

        import datetime

        try:
            datetime.datetime.strptime(value, "%I:%M %p")
        except ValueError:
            raise ValueError(
                "Time must be in HH:MM AM/PM format."
            )

        return value

class Doctor(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50,
        description="Doctor name"
    )

    specialization: str = Field(
        min_length=2,
        max_length=50,
        description="Doctor specialization"
    )

    phone: str = Field(
        pattern=r"^\d{10}$",
        description="10-digit mobile number"
    )

    email: str

    experience: int = Field(
        ge=0,
        le=60,
        description="Years of experience"
    )

    status: Literal[
        "Active",
        "Inactive"
    ] = "Active"

class Attendance(BaseModel):

    doctor_id: int

    attendance_date: str

    attendance_status: Literal[
        "Present",
        "Absent",
        "Leave"
    ]

    check_in_time: str | None = None

    check_out_time: str | None = None
    
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
from database import get_connection
from datetime import date
from datetime import datetime, timedelta
from hospital_config import WORKING_HOURS
from datetime import date
import sqlite3


def calculate_status(appointment_date: str):

    today = date.today().isoformat()

    if appointment_date < today:
        return "completed"

    return "scheduled"

def is_completed_booking(booking_id):

    booking_number = int(
        booking_id.replace("APPT", "")
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT status
        FROM appointments
        WHERE booking_id = ?
        """,
        (booking_number,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return False

    return row["status"] == "completed"

def save_booking(doctor, date, time, name, phone):

    connection = get_connection()

    cursor = connection.cursor()

    if time not in WORKING_HOURS:

        connection.close()

        return {
            "success": False,
            "status": "working_hours",
            "message": "Selected appointment time is outside hospital working hours.",
            "available_slots": WORKING_HOURS
        }

    if not is_doctor_available(
        doctor,
        date,
        time
    ):

        available_slots = get_next_available_slots(
            doctor,
            date
        )

        connection.close()

        return {
            "success": False,
            "status": "doctor_unavailable",
            "message": "Doctor is not available at the selected date and time.",
            "available_slots": available_slots
        }

    cursor.execute(
        """
        INSERT INTO appointments
        (name, phone, doctor, date, time, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            doctor,
            date,
            time,
            "scheduled"
        )
    )

    connection.commit()

    booking_id = cursor.lastrowid

    connection.close()

    return {
        "success": True,
        "status": "booked",
        "message": "Appointment booked successfully.",
        "data": {
            "booking_id": f"APPT{booking_id:03d}",
            "name": name,
            "phone": phone,
            "doctor": doctor,
            "date": date,
            "time": time,
            "status": "scheduled"
        }
    }

def get_bookings():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appointments
        ORDER BY booking_id
        """
    )

    rows = cursor.fetchall()

    cursor.execute("SELECT booking_id, status FROM appointments")

    for row in cursor.fetchall():
        print(row["booking_id"], row["status"])

    connection.close()

    bookings = []

    for row in rows:

        bookings.append(
            {
                "booking_id": f"APPT{row['booking_id']:03d}",
                "name": row["name"],
                "phone": row["phone"],
                "doctor": row["doctor"],
                "date": row["date"],
                "time": row["time"],
                "status": row["status"]
            }
        )

    return bookings

def get_dashboard_summary():

    bookings = get_bookings()
    doctors = get_doctors()
    patients = get_patients()
    todays_bookings = get_todays_bookings()

    total = len(bookings)

    scheduled = 0
    cancelled = 0
    completed = 0

    for booking in bookings:

        status = booking["status"].lower()

        if status == "scheduled":
            scheduled += 1

        elif status == "cancelled":
            cancelled += 1

        elif status == "completed":
            completed += 1

    return {
        "totalAppointments": total,
        "todayAppointments": len(todays_bookings),
        "scheduledAppointments": scheduled,
        "completedAppointments": completed,
        "cancelledAppointments": cancelled,
        "totalDoctors": len(doctors),
        "totalPatients": len(patients),
        "completionRate": round((completed / total) * 100, 2) if total > 0 else 0,

        "hospitalStatus": "Operational",
        "databaseStatus": "Connected",
        "aiAgentStatus": "Offline"
    }

def get_doctor_analytics():

    bookings = get_bookings()
    doctors = get_doctors()

    analytics = []

    for doctor in doctors:

        doctor_name = doctor["specialization"]

        total = 0
        completed = 0
        scheduled = 0
        cancelled = 0

        for booking in bookings:

            if booking["doctor"] == doctor_name:

                total += 1

                status = booking["status"].lower()

                if status == "completed":
                    completed += 1

                elif status == "scheduled":
                    scheduled += 1

                elif status == "cancelled":
                    cancelled += 1

        analytics.append({
            "doctor": doctor["name"],
            "total": total,
            "completed": completed,
            "scheduled": scheduled,
            "cancelled": cancelled,
        })

    return analytics

def get_status_analytics():

    summary = get_dashboard_summary()

    return {
        "scheduled": summary["scheduledAppointments"],
        "completed": summary["completedAppointments"],
        "cancelled": summary["cancelledAppointments"]
    }


def get_doctor_analytics():

    bookings = get_bookings()

    analytics = {}

    for booking in bookings:

        doctor = booking["doctor"].strip().title()

        if doctor not in analytics:

            analytics[doctor] = {
                "doctor": doctor,
                "total": 0,
                "completed": 0,
                "scheduled": 0,
                "cancelled": 0,
            }

        analytics[doctor]["total"] += 1

        status = booking["status"].lower()

        if status == "completed":
            analytics[doctor]["completed"] += 1

        elif status == "scheduled":
            analytics[doctor]["scheduled"] += 1

        elif status == "cancelled":
            analytics[doctor]["cancelled"] += 1

    return list(analytics.values())

def cancel_booking(booking_id):

    if is_completed_booking(booking_id):
        return False

    booking_number = int(booking_id.replace("APPT", ""))

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE appointments
        SET status = 'cancelled'
        WHERE booking_id = ?
        AND status = 'scheduled'
        """,
        (booking_number,)
    )

    connection.commit()

    cancelled = cursor.rowcount > 0

    connection.close()

    return cancelled

def get_bookings_by_phone(phone):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appointments
        WHERE phone = ?
        AND status = 'scheduled'
        ORDER BY booking_id
        """,
        (phone,)
    )

    rows = cursor.fetchall()

    connection.close()

    bookings = []

    for row in rows:

        bookings.append(
            {
                "booking_id": f"APPT{row['booking_id']:03d}",
                "name": row["name"],
                "phone": row["phone"],
                "doctor": row["doctor"],
                "date": row["date"],
                "time": row["time"],
                "status": row["status"]
            }
        )

    return bookings

def update_booking(booking_id, new_date, new_time):

    booking_number = int(booking_id.replace("APPT", ""))

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE appointments
        SET date = ?, time = ?
        WHERE booking_id = ?
        """,
        (
            new_date,
            new_time,
            booking_number
        )
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated

def get_bookings_by_doctor(doctor):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appointments
        WHERE LOWER(doctor) = LOWER(?)
        ORDER BY booking_id
        """,
        (doctor,)
    )

    rows = cursor.fetchall()

    connection.close()

    bookings = []

    for row in rows:

        bookings.append(
            {
                "booking_id": f"APPT{row['booking_id']:03d}",
                "name": row["name"],
                "phone": row["phone"],
                "doctor": row["doctor"],
                "date": row["date"],
                "time": row["time"],
                "status": row["status"]
            }
        )

    return bookings

def get_bookings_by_date(date):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appointments
        WHERE date = ?
        ORDER BY booking_id
        """,
        (date,)
    )

    rows = cursor.fetchall()

    connection.close()

    bookings = []

    for row in rows:

        bookings.append(
            {
                "booking_id": f"APPT{row['booking_id']:03d}",
                "name": row["name"],
                "phone": row["phone"],
                "doctor": row["doctor"],
                "date": row["date"],
                "time": row["time"],
                "status": row["status"]
            }
        )

    return bookings



def get_todays_bookings():

    today = date.today().strftime("%Y-%m-%d")

    return get_bookings_by_date(today)

def update_booking_details(
    booking_id,
    name,
    phone,
    doctor,
    date,
    time
):

    if is_completed_booking(booking_id):
        return False

    booking_number = int(booking_id.replace("APPT", ""))

    connection = get_connection()

    cursor = connection.cursor()

    status = calculate_status(date)

    cursor.execute(
        """
        UPDATE appointments
        SET
            name = ?,
            phone = ?,
            doctor = ?,
            date = ?,
            time = ?,
            status = ?
        WHERE booking_id = ?
        """,
        (
            name,
            phone,
            doctor,
            date,
            time,
            status,
            booking_number
        )
    )
    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated

def get_tomorrows_appointments():

    tomorrow = (
        datetime.now() +
        timedelta(days=1)
    ).strftime("%Y-%m-%d")

    print("Tomorrow =", tomorrow)

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM appointments
        WHERE
            date = ?
            AND status = 'scheduled'
        ORDER BY time
        """,
        (tomorrow,)
    )

    rows = cursor.fetchall()

    connection.close()

    appointments = []

    for row in rows:

        appointments.append(
            {
                "booking_id": f"APPT{row['booking_id']:03d}",
                "name": row["name"],
                "phone": row["phone"],
                "doctor": row["doctor"],
                "date": row["date"],
                "time": row["time"],
                "status": row["status"]
            }
        )

    return appointments

def is_doctor_available(
    doctor,
    date,
    time
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT booking_id
        FROM appointments
        WHERE
            doctor = ?
            AND date = ?
            AND time = ?
            AND status = 'scheduled'
        """,
        (
            doctor,
            date,
            time
        )
    )

    booking = cursor.fetchone()

    connection.close()

    return booking is None


# Paste the new function HERE ↓↓↓

def get_available_slots(
    doctor,
    date
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT time
        FROM appointments
        WHERE
            doctor = ?
            AND date = ?
            AND status = 'scheduled'
        """,
        (
            doctor,
            date
        )
    )

    booked_slots = []

    rows = cursor.fetchall()

    for row in rows:

        booked_slots.append(
            row["time"]
        )

    connection.close()

    available_slots = []

    for slot in WORKING_HOURS:

        if slot not in booked_slots:

            available_slots.append(slot)

    return available_slots

def get_next_available_slots(
    doctor,
    date,
    limit=3
):

    available_slots = get_available_slots(
        doctor,
        date
    )

    return available_slots[:limit]

def get_patients():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            name,
            phone,
            COUNT(*) AS appointments,
            SUM(CASE WHEN status = 'scheduled' THEN 1 ELSE 0 END) AS scheduled,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed
        FROM appointments
        GROUP BY phone, name
        ORDER BY name
        """
    )

    rows = cursor.fetchall()

    connection.close()

    patients = []

    for row in rows:

        patients.append(
            {
                "name": row["name"],
                "phone": row["phone"],
                "appointments": row["appointments"],
                "scheduled": row["scheduled"],
                "completed": row["completed"],
            }
        )

    return patients

def get_doctors():

    connection = get_connection()

    cursor = connection.cursor()

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT
            d.*,
            a.attendance_status
        FROM doctors d
        LEFT JOIN doctor_attendance a
        ON d.doctor_id = a.doctor_id
        AND a.attendance_date = ?
        ORDER BY
        CASE
            WHEN d.status = 'Active' THEN 0
            ELSE 1
        END,
        d.name
        """
    , (today,))

    rows = cursor.fetchall()

    connection.close()

    doctors = []

    for row in rows:

        doctors.append(
            {
                "doctor_id": row["doctor_id"],
                "name": row["name"],
                "specialization": row["specialization"],
                "phone": row["phone"],
                "email": row["email"],
                "experience": row["experience"],
                "status": row["status"],
                "attendance_status": row["attendance_status"]
            }
        )

    return doctors

from datetime import date

def get_available_doctors_today():

    conn = get_connection()
    cursor = conn.cursor()

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT
            d.doctor_id,
            d.name,
            d.specialization,
            d.phone,
            d.email,
            d.experience
        FROM doctors d
        INNER JOIN doctor_attendance a
            ON d.doctor_id = a.doctor_id
        WHERE
            d.status = 'Active'
            AND a.attendance_date = ?
            AND a.attendance_status = 'Present'
    """, (today,))

    doctors = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return doctors

def save_doctor(
    name,
    specialization,
    phone,
    email,
    experience,
    status="Active"
):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO doctors
            (
                name,
                specialization,
                phone,
                email,
                experience,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                specialization,
                phone,
                email,
                experience,
                status
            )
        )

        connection.commit()

        doctor_id = cursor.lastrowid

        return {
            "doctor_id": doctor_id,
            "name": name,
            "specialization": specialization,
            "phone": phone,
            "email": email,
            "experience": experience,
            "status": status
        }

    except sqlite3.IntegrityError as e:

        error = str(e)

        if "phone" in error:
            raise ValueError("Phone number already exists.")

        if "email" in error:
            raise ValueError("Email already exists.")

        raise ValueError("Doctor already exists.")

    finally:
        connection.close()

def update_doctor(
    doctor_id,
    name,
    specialization,
    phone,
    email,
    experience,
    status="Active"
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE doctors
            SET
                name = ?,
                specialization = ?,
                phone = ?,
                email = ?,
                experience = ?,
                status = ?
            WHERE doctor_id = ?
            """,
            (
                name,
                specialization,
                phone,
                email,
                experience,
                status,
                doctor_id
            )
        )

        connection.commit()

        return {
            "doctor_id": doctor_id,
            "name": name,
            "specialization": specialization,
            "phone": phone,
            "email": email,
            "experience": experience,
            "status": status
        }

    except sqlite3.IntegrityError as e:

        error = str(e)

        if "phone" in error:
            raise ValueError("Phone number already exists.")

        if "email" in error:
            raise ValueError("Email already exists.")

        raise ValueError("Doctor already exists.")

    finally:
        connection.close()

def delete_doctor(doctor_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE doctors
        SET status = 'Inactive'
        WHERE doctor_id = ?
        """,
        (doctor_id,)
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    if updated == 0:

        raise ValueError("Doctor not found.")

    return {
        "message": "Doctor deactivated successfully."
    }

from datetime import datetime

def update_completed_appointments():

    print("Completed appointments updated.")

    connection = get_connection()

    cursor = connection.cursor()

    now = datetime.now()

    cursor.execute(
        """
        SELECT booking_id, date, time
        FROM appointments
        WHERE status = 'scheduled'
        """
    )

    rows = cursor.fetchall()

    updated = 0

    for row in rows:

        try:
            appointment_datetime = datetime.strptime(
                f"{row['date']} {row['time']}",
                "%Y-%m-%d %I:%M %p"
            )

        except ValueError:

            appointment_datetime = datetime.strptime(
                f"{row['date']} {row['time']}",
                "%Y-%m-%d %I %p"
            )

        print(
            row["booking_id"],
            appointment_datetime,
            now,
            appointment_datetime < now
        )

        if appointment_datetime < now:

            cursor.execute(
                """
                UPDATE appointments
                SET status = 'completed'
                WHERE booking_id = ?
                """,
                (row["booking_id"],)
            )

            updated += 1

    connection.commit()

    connection.close()

    return updated

def get_user_by_username(username: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user

def create_user(
    username: str,
    password: str,
    role: str
):
    from security import hash_password

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            hash_password(password),
            role
        )
    )

    connection.commit()
    connection.close()

def get_available_doctors():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            name,
            specialization
        FROM doctors
        WHERE status = 'Active'
        ORDER BY specialization, name
    """)

    doctors = cursor.fetchall()

    connection.close()

    return doctors

def get_doctor_attendance(
    doctor_id,
    attendance_date,
    attendance_status,
    check_in_time,
    check_out_time
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT attendance_id
        FROM doctor_attendance
        WHERE doctor_id = ?
        AND attendance_date = ?
        """,
        (
            doctor_id,
            attendance_date
        )
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE doctor_attendance
            SET
                attendance_status = ?,
                check_in_time = ?,
                check_out_time = ?
            WHERE attendance_id = ?
            """,
            (
                attendance_status,
                check_in_time,
                check_out_time,
                existing["attendance_id"]
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO doctor_attendance
            (
                doctor_id,
                attendance_date,
                attendance_status,
                check_in_time,
                check_out_time
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                doctor_id,
                attendance_date,
                attendance_status,
                check_in_time,
                check_out_time
            )
        )

    connection.commit()

    connection.close()

    return {
        "message": "Attendance saved successfully."
    }

def get_attendance_record(
    doctor_id,
    attendance_date
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM doctor_attendance
        WHERE doctor_id = ?
        AND attendance_date = ?
        """,
        (
            doctor_id,
            attendance_date
        )
    )

    record = cursor.fetchone()

    connection.close()

    return record

def mark_doctor_attendance(
    
    doctor_id,
    attendance_date,
    attendance_status,
    check_in_time=None,
    check_out_time=None
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT attendance_id
        FROM doctor_attendance
        WHERE doctor_id = ?
        AND attendance_date = ?
        """,
        (
            doctor_id,
            attendance_date
        )
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE doctor_attendance
            SET
                attendance_status = ?,
                check_in_time = ?,
                check_out_time = ?
            WHERE attendance_id = ?
            """,
            (
                attendance_status,
                check_in_time,
                check_out_time,
                existing["attendance_id"]
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO doctor_attendance
            (
                doctor_id,
                attendance_date,
                attendance_status,
                check_in_time,
                check_out_time
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                doctor_id,
                attendance_date,
                attendance_status,
                check_in_time,
                check_out_time
            )
        )

    connection.commit()

    connection.close()

    return {
        "message": "Attendance saved successfully."
    }

def reactivate_doctor(doctor_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE doctors
        SET status = 'Active'
        WHERE doctor_id = ?
        """,
        (doctor_id,)
    )

    connection.commit()

    connection.close()
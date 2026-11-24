import sqlite3

DATABASE_NAME = "appointments.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments(

            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            phone TEXT,

            doctor TEXT,

            date TEXT,

            time TEXT

        )
        """
    )

    try:
        cursor.execute("""
            ALTER TABLE appointments
            ADD COLUMN status TEXT DEFAULT 'scheduled'
        """)
    except sqlite3.OperationalError:
        pass

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS doctors(

            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            specialization TEXT NOT NULL,

            phone TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            experience INTEGER,

            status TEXT DEFAULT 'Active'

        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS doctor_attendance(

            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,

            doctor_id INTEGER NOT NULL,

            attendance_date TEXT NOT NULL,

            attendance_status TEXT NOT NULL,

            check_in_time TEXT,

            check_out_time TEXT,

            FOREIGN KEY (doctor_id)
                REFERENCES doctors(doctor_id)

        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()

def get_all_doctors():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, specialization
        FROM doctors
        WHERE status = 'Active'
    """)

    doctors = cursor.fetchall()

    connection.close()

    return doctors


create_tables()
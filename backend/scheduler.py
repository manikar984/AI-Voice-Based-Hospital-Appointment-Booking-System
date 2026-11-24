from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from notification_service import send_sms_reminder
from appointments_db import (
    update_completed_appointments,
    get_tomorrows_appointments
)

scheduler = BackgroundScheduler(
    timezone=ZoneInfo("Asia/Kolkata")
)

def send_reminders():

    appointments = get_tomorrows_appointments()

    if not appointments:

        print("No reminders to send.")
        return

    for appointment in appointments:

        send_sms_reminder(appointment)


def start_scheduler():

    # Temporary test job
    scheduler.add_job(
        update_completed_appointments,
        trigger="cron",
        hour=1,
        minute=0
    )

    scheduler.add_job(
        send_reminders,
        trigger="cron",
        hour=9,
        minute=0
    )

    scheduler.start()

    print("Scheduler Started")
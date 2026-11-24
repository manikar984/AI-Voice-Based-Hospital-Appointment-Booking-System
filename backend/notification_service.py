from logger_config import logger


def send_sms_reminder(appointment):

    logger.info(
        f"SMS Reminder -> "
        f"{appointment['phone']} | "
        f"{appointment['name']} | "
        f"{appointment['doctor']} | "
        f"{appointment['date']} | "
        f"{appointment['time']}"
    )

    print(
        f"""
================ SMS REMINDER ================

To      : {appointment['phone']}

Hello {appointment['name']},

This is a reminder from AI Clinical Appointment System.

Doctor : {appointment['doctor']}
Date   : {appointment['date']}
Time   : {appointment['time']}

Please arrive 15 minutes before your appointment.

==============================================
"""
    )


def send_whatsapp_reminder(appointment):

    logger.info(
        f"WhatsApp Reminder -> {appointment['phone']}"
    )

    print(
        f"""
============== WHATSAPP REMINDER ==============

To : {appointment['phone']}

Hello {appointment['name']},

Your appointment is tomorrow.

Doctor : {appointment['doctor']}
Date   : {appointment['date']}
Time   : {appointment['time']}

===============================================
"""
    )


def send_voice_reminder(appointment):

    logger.info(
        f"Voice Reminder -> {appointment['phone']}"
    )

    print(
        f"""
=============== VOICE REMINDER ===============

Calling {appointment['phone']}

Hello {appointment['name']},

This is your appointment reminder.

Doctor : {appointment['doctor']}
Date   : {appointment['date']}
Time   : {appointment['time']}

==============================================
"""
    )
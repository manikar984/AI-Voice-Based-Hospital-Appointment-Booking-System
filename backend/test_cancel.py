from appointments_db import (
    cancel_booking,
    get_bookings
)

print("Before:")
print(get_bookings())

result = cancel_booking("APPT007")

print("Cancelled:", result)

print("After:")
print(get_bookings())
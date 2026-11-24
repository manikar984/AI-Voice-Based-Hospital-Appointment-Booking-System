from appointments_db import save_booking, get_bookings

save_booking(
    "neurologist",
    "2026-06-23",
    "11:00 AM",
    "Mani",
    "6300530178"
)

print(get_bookings())
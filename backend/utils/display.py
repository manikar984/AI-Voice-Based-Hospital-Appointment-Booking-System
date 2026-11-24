def print_separator():

    print("-" * 30)


def print_header(title):

    print()
    print("=" * 30)
    print(f" {title}")
    print("=" * 30)


def print_success(message):

    print(f"\n✅ {message}\n")


def print_error(message):

    print(f"\n❌ {message}\n")


def print_info(message):

    print(f"\nℹ️ {message}\n")


def print_booking(booking):

    print_separator()

    print(f"Booking ID : {booking['booking_id']}")
    print(f"Patient    : {booking.get('name') or 'Not Available'}")
    print(f"Phone      : {booking.get('phone') or 'Not Available'}")
    print(f"Doctor     : {booking.get('doctor')}")
    print(f"Date       : {booking.get('date')}")
    print(f"Time       : {booking.get('time')}")

    print_separator()
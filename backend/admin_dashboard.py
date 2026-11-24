from utils.validators import (
    is_valid_phone,
    is_valid_booking_id,
    is_valid_date,
    is_valid_time
)

from utils.display import (
    print_booking,
    print_success,
    print_error,
    print_info
)

from appointments_db import (
    get_bookings,
    get_dashboard_summary,
    get_todays_bookings,
    get_bookings_by_phone,
    get_bookings_by_doctor,
    get_bookings_by_date,
    update_booking,
    cancel_booking
)


def show_menu():

    print("\n==============================")
    print(" AI CLINIC ADMIN DASHBOARD")
    print("==============================")
    print("1. Dashboard Summary")
    print("2. View All Appointments")
    print("3. Search by Phone")
    print("4. Search by Doctor")
    print("5. Search by Date")
    print("6. Update Appointment")
    print("7. Delete Appointment")
    print("8. Exit")
    print("==============================")

def show_dashboard_summary():

    summary = get_dashboard_summary()

    print("\n====================================")
    print("      DASHBOARD SUMMARY")
    print("====================================")
    print(f"Total Appointments : {summary['total']}")
    print(f"Scheduled          : {summary['scheduled']}")
    print(f"Cancelled          : {summary['cancelled']}")
    print(f"Completed          : {summary['completed']}")
    print("====================================")

    todays_bookings = get_todays_bookings()

    print("\nToday's Appointments")
    print("------------------------------------")

    if not todays_bookings:

        print("No appointments scheduled today.")

    else:

        for booking in todays_bookings:

            print(
                f"{booking['time']:<10} "
                f"{booking['name']:<15} "
                f"{booking['doctor']}"
            )

    print("====================================\n")


while True:

    show_menu()

    choice = input("Enter your choice: ")

    if choice == "1":

        show_dashboard_summary()


    elif choice == "2":

        bookings = get_bookings()

        if not bookings:

            print("\nNo appointments found.\n")

        else:

            print()

            for booking in bookings:

                print_booking(booking)


    elif choice == "3":

        phone = input(
            "\nEnter phone number: "
        )

        if not is_valid_phone(phone):

            print_error(
                "Invalid phone number."
            )

            continue

        bookings = get_bookings_by_phone(
            phone
        )

        if not bookings:

            print_info(
                "No appointments found."
            )

        else:

            print()

            for booking in bookings:

                print_booking(booking)

    elif choice == "4":

        doctor = input(
            "\nEnter doctor name: "
        )

        bookings = get_bookings_by_doctor(
            doctor
        )

        if not bookings:

            print(
                "\nNo appointments found.\n"
            )

        else:

            print()

            for booking in bookings:

                print_booking(booking)


    elif choice == "5":

        date = input(
            "\nEnter appointment date (YYYY-MM-DD): "
        )

        if not is_valid_date(date):

            print("\nInvalid date format.\n")

            continue

        bookings = get_bookings_by_date(
            date
        )

        if not bookings:

            print(
                "\nNo appointments found.\n"
            )

        else:

            print()

            for booking in bookings:

                print_booking(booking)

    elif choice == "6":

        booking_id = input(
            "\nEnter Booking ID: "
        ).strip()

        if not is_valid_booking_id(booking_id):

            print("\nInvalid Booking ID.\n")

            continue

        new_date = input(
            "Enter New Date (YYYY-MM-DD): "
        ).strip()

        if not is_valid_date(new_date):

            print("\nInvalid date format.\n")

            continue

        new_time = input(
            "Enter New Time (HH:MM AM/PM): "
        ).strip()

        if not is_valid_time(new_time):

            print("\nInvalid time format.\n")

            continue

        updated = update_booking(
            booking_id,
            new_date,
            new_time
        )

        if updated:

            print_success(
                "Appointment updated successfully."
            )

        else:

            print(
                "\nBooking ID not found.\n"
            )

    elif choice == "7":

        booking_id = input(
            "\nEnter Booking ID to delete: "
        ).strip()

        if not is_valid_booking_id(booking_id):

            print("\nInvalid Booking ID.\n")

            continue

        deleted = cancel_booking(
            booking_id
        )

        if deleted:

            print_success(
                "Appointment deleted successfully."
            )

        else:

            print_error(
                "Booking ID not found."
            )

    elif choice == "8":

        print("\nGoodbye!\n")
        break

    else:

        print("\nFeature coming soon.\n")
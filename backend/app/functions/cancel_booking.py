from app.services.data_store import data_loader


def cancel_booking(pnr: str):

    bookings = data_loader.load_bookings()

    pnr = pnr.upper().strip()

    for booking in bookings:

        if booking["pnr"] == pnr:

            if booking["booking_status"] == "Cancelled":

                return {
                    "success": False,
                    "message": "Booking is already cancelled."
                }

            booking["booking_status"] = "Cancelled"

            return {
                "success": True,
                "message": "Booking cancelled successfully.",
                "booking": booking,
            }

    return {
        "success": False,
        "message": "Booking not found."
    }
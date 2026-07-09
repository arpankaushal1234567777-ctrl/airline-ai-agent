from app.services.data_store import data_loader


def check_flight_status(flight_number: str):

    flights = data_loader.load_emirates_flights()

    flight_number = flight_number.upper().strip()

    for flight in flights:

        if flight["flight_number"].upper() == flight_number:

            return {
                "success": True,
                "flight_number": flight["flight_number"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "departure": flight["departure"],
                "arrival": flight["arrival"],
                "aircraft": flight["aircraft"],
                "status": flight["status"],
                "available_seats": flight["available_seats"],
            }

    return {
        "success": False,
        "message": f"Flight '{flight_number}' not found.",
    }

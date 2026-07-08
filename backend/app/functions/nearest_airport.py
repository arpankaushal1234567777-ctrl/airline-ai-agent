from app.functions.airport_lookup import find_airport


def nearest_airport(city: str):

    airports = find_airport(city)

    if not airports:
        return {
            "success": False,
            "message": f"No airport found for {city}."
        }

    return {
        "success": True,
        "airport": airports[0]
    }
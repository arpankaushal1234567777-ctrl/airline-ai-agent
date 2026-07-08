from app.services.data_store import data_loader


def search_flights(origin: str, destination: str):

    flights = data_loader.load_emirates_flights()

    origin = origin.lower().strip()
    destination = destination.lower().strip()

    results = []

    for flight in flights:

        if (
            flight["origin"].lower() == origin
            and
            flight["destination"].lower() == destination
        ):

            results.append(flight)

    return results
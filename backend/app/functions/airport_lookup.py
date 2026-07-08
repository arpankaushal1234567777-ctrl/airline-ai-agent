from app.services.data_store import data_loader


def find_airport(city: str):

    airports = data_loader.load_airports()

    city = city.lower().strip()

    results = []

    for airport in airports:

        airport_name = airport[1]
        airport_city = airport[2]
        country = airport[3]
        iata = airport[4]
        icao = airport[5]

        if airport_city.lower() == city and iata != "\\N":

         results.append(
            {
            "airport_name": airport_name,
            "city": airport_city,
            "country": country,
            "iata": iata,
            "icao": icao,
            }
    )

    return results
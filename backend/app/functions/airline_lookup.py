from app.services.data_store import data_loader


def find_airline(query: str):

    airlines = data_loader.load_airlines()

    query = query.lower().strip()

    results = []

    for airline in airlines:

        name = airline[1]
        iata = airline[3]
        icao = airline[4]
        country = airline[6]

        if (
            query == name.lower()
            or query == iata.lower()
            or query == icao.lower()
        ):

            results.append(
                {
                    "name": name,
                    "iata": iata,
                    "icao": icao,
                    "country": country,
                }
            )

    return results
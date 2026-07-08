from app.services.data_store import data_loader


def find_aircraft(query: str):

    aircrafts = data_loader.load_planes()

    query = query.lower().strip()

    results = []

    for aircraft in aircrafts:

        name = aircraft[0]
        iata = aircraft[1]
        icao = aircraft[2]

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
                }
            )

    return results 
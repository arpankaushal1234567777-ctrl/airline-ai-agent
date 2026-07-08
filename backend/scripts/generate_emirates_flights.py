import json
import random
from pathlib import Path

from app.services.data_store import data_loader


# Emirates destinations (IATA Codes)
EMIRATES_DESTINATIONS = [
    "DXB",
    "DEL",
    "BOM",
    "BLR",
    "HYD",
    "MAA",
    "COK",
    "CCU",
    "LHR",
    "CDG",
    "FRA",
    "JFK",
    "SIN",
    "SYD",
    "BKK",
]

AIRCRAFT = [
    "Airbus A380-800",
    "Boeing 777-300ER",
    "Boeing 777-200LR",
]

TRAVEL_CLASSES = [
    "Economy",
    "Premium Economy",
    "Business",
    "First",
]


def generate_time():

    hour = random.randint(0, 23)
    minute = random.choice([0, 15, 30, 45])

    return f"{hour:02}:{minute:02}"


def load_airports():

    airports = data_loader.load_airports()

    airport_map = {}

    for airport in airports:

        iata = airport[4]

        if iata in EMIRATES_DESTINATIONS:

            airport_map[iata] = {
                "city": airport[2],
                "country": airport[3],
            }

    return airport_map


def main():

    airports = load_airports()

    flights = []

    flight_number = 200

    for origin in EMIRATES_DESTINATIONS:

        for destination in EMIRATES_DESTINATIONS:

            if origin == destination:
                continue

            if origin not in airports or destination not in airports:
                continue

            departure = generate_time()
            arrival = generate_time()

            flights.append(
                {
                    "flight_number": f"EK{flight_number}",
                    "origin": airports[origin]["city"],
                    "origin_iata": origin,
                    "destination": airports[destination]["city"],
                    "destination_iata": destination,
                    "departure": departure,
                    "arrival": arrival,
                    "aircraft": random.choice(AIRCRAFT),
                    "travel_classes": TRAVEL_CLASSES,
                    "available_seats": random.randint(40, 320),
                    "status": "Scheduled",
                }
            )

            flight_number += 1

    output_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "mock"
        / "emirates_flights.json"
    )

    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(flights, file, indent=4)

    print(f"Generated {len(flights)} Emirates flights.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
import json
import random
from pathlib import Path


PASSENGER_NAMES = [
    "Arpan Kaushal",
    "Rahul Sharma",
    "Priya Singh",
    "Amit Verma",
    "Neha Gupta",
    "Rohan Kapoor",
    "Ananya Mehta",
    "Vikram Patel",
    "Sneha Nair",
    "Karan Malhotra",
]

TRAVEL_CLASSES = [
    "Economy",
    "Premium Economy",
    "Business",
    "First",
]


def load_flights():

    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "mock"
        / "emirates_flights.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:

        return json.load(file)


def generate_pnr(existing):

    while True:

        pnr = f"EM{random.randint(100000,999999)}"

        if pnr not in existing:

            return pnr


def main():

    flights = load_flights()

    bookings = []

    used_pnr = set()

    for _ in range(100):

        flight = random.choice(flights)

        pnr = generate_pnr(used_pnr)

        used_pnr.add(pnr)

        bookings.append(
        {
            "pnr": pnr,
            "passenger_name": random.choice(PASSENGER_NAMES),
            "flight_number": flight["flight_number"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "travel_class": random.choice(TRAVEL_CLASSES),
            "seat_number": f"{random.randint(1,45)}{random.choice(['A','B','C','D','E','F'])}",
            "booking_date": "2026-07-07",
            "booking_status": "Confirmed",
        }
    )

    output_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "mock"
        / "bookings.json"
    )

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(bookings, file, indent=4)

    print(f"Generated {len(bookings)} bookings.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
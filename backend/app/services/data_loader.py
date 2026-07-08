from pathlib import Path
import csv
import json


class DataLoader:

    def __init__(self):

        self.dataset_path = (
            Path(__file__).resolve().parents[2] / "data" / "datasets"
        )

        self._cache = {}

    def _load_dataset(self, filename: str):

        if filename in self._cache:
            return self._cache[filename]

        data = []

        file_path = self.dataset_path / filename

        with open(file_path, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for row in reader:
                data.append(row)

        self._cache[filename] = data

        return data
    
    def _load_json(self, filename: str):

        if filename in self._cache:
            return self._cache[filename]

        file_path = (
        self.dataset_path.parent
        / "mock"
        / filename
        )

        with open(file_path, "r", encoding="utf-8") as file:

            data = json.load(file)

        self._cache[filename] = data

        return data

    def load_airports(self):
        return self._load_dataset("airports.dat")

    def load_airlines(self):
        return self._load_dataset("airlines.dat")

    def load_routes(self):
        return self._load_dataset("routes.dat")

    def load_planes(self):
        return self._load_dataset("planes.dat")

    def load_countries(self):
        return self._load_dataset("countries.dat")
    
    def load_emirates_flights(self):
        return self._load_json("emirates_flights.json")
    
    def load_bookings(self):
        return self._load_json("bookings.json")
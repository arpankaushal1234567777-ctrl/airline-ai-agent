from app.services.data_loader import DataLoader


loader = DataLoader()

airports = loader.load_airports()

print(f"Total Airports : {len(airports)}")

print()

print(airports[0])

print()

print(airports[1])
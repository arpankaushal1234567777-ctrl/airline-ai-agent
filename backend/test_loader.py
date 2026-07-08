from app.services.data_store import data_loader


bookings = data_loader.load_bookings()

print(f"Total Bookings : {len(bookings)}")

print()

print(bookings[0])
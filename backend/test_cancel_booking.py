from app.services.data_store import data_loader
from app.functions.cancel_booking import cancel_booking

bookings = data_loader.load_bookings()

pnr = bookings[0]["pnr"]

print("Testing PNR:", pnr)
print()

print(cancel_booking(pnr))
print()

print(cancel_booking(pnr))
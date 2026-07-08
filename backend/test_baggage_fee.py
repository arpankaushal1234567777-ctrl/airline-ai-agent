from app.functions.baggage_fee import calculate_baggage_fee


print(calculate_baggage_fee("Economy", 28))

print()

print(calculate_baggage_fee("Business", 35))

print()

print(calculate_baggage_fee("First", 55))

print()

print(calculate_baggage_fee("Premium Economy", 35))

print()

print(calculate_baggage_fee("VIP", 20))
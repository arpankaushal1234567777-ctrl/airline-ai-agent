from app.services.data_store import data_loader

planes = data_loader.load_planes()

print(len(planes))
print()
print(planes[0])
print()
print(planes[1])
print()
print(planes[2])
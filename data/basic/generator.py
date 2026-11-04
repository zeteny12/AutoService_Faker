from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker("hu_HU")
fake.add_provider(VehicleProvider)

def generate_hungarian_plate():
    plate_type = fake.random_element(["old", "new"])
    number = fake.random_int(min=1, max=999)
    number = f"{number:03d}"

    if plate_type == "old":
        return f'{fake.bothify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")}-{number}'
    else:
        vowels = "AEIOU"
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
        letters= fake.random_element([vowels, consonants])
        first_two = fake.lexify(text="??", letters=letters)

        while first_two in ("CS", "GY", "LY", "NY", "SZ", "TY", "ZS"):
            first_two = fake.lexify(text="??", letters=letters)

        return f'{first_two}-{fake.bothify(text="??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")}-{number}'
from faker import Faker
from faker_vehicle import VehicleProvider
from data.basic.model_dataclasses import Car, Service
from datetime import date, timedelta

fake = Faker("hu_HU")
fake.add_provider(VehicleProvider)

def generate_hungarian_plate()->str:
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
        forbidden_pairs = ["CS", "GY", "LY", "NY", "SZ", "TY", "ZS"]

        while first_two in forbidden_pairs:
            first_two = fake.lexify(text="??", letters=letters)

        return f'{first_two}-{fake.bothify(text="??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")}-{number}'

def generate_cars(n:int)->list[Car]:
    cars = []
    plates = set()
    for _ in range(n):
        plate = generate_hungarian_plate()
        while plate in plates:
            plate = generate_hungarian_plate()
        plates.add(plate)

        car = Car(
            plate = plate,
            type = fake.vehicle_make_model(),
            year = fake.random_int(min=1990, max=date.today().year),
            automatic = fake.boolean()
        )
        cars.append(car)

    return cars

def generate_services(cars: list[Car])->list[Service]:
    services = []
    next_id = 1

    service_types = [
        "Olajcsere",
        "Féktárcsacsere",
        "Futóműjavítás",
        "Kuplungcsere",
        "Gumicsere",
        "Vezérléscsere",
        "Akkumulátorcsere"
    ]

    for car in cars:
        service_count = fake.random_int(min=1, max=3)

        for _ in range(service_count):
            service_date = fake.date_between(
                start_date=max(
                    date(car.year, 1, 1),
                    date.today() - timedelta(days=5 * 365)
                ),
                end_date="today"
            ).isoformat()

            service = Service(
                id = next_id,
                car_plate = car.plate,
                date = service_date,
                description = fake.random_element(service_types),
                cost = fake.random_int(min=5_000, max=200_000)
            )
            next_id += 1
            services.append(service)


    return services

def generate_data(n:int)->tuple[list[Car], list[Service]]:
    cars = generate_cars(n)
    services = generate_services(cars)

    return cars, services
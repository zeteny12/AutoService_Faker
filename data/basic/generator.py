from faker import Faker
from faker_vehicle import VehicleProvider
from data.basic.model_dataclasses import Car, Service, Mechanic
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

def generate_cars(n:int, min_year: int = 1990, max_year: int | None = None)->list[Car]:
    cars = []
    plates = set()

    if max_year is None:
        max_year = date.today().year

    for _ in range(n):
        plate = generate_hungarian_plate()
        while plate in plates:
            plate = generate_hungarian_plate()
        plates.add(plate)

        car = Car(
            plate = plate,
            type = fake.vehicle_make_model(),
            year = fake.random_int(min=min_year, max=max_year),
            automatic = fake.boolean()
        )
        cars.append(car)

    return cars

def generate_services(cars: list[Car], mechanics: list[Mechanic], min_cost: int = 5_000, max_cost: int = 200_000)->list[Service]:
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
                cost = fake.random_int(min=min_cost, max=max_cost),
                mechanic_id = fake.random_element(mechanics).id
            )
            next_id += 1
            services.append(service)


    return services

def generate_mechanics(n: int, min_experience: int = 1, max_experience: int = 40)->list[Mechanic]:
    mechanics = []
    next_id = 1

    specializations = [
        "Motorszerelés",
        "Fékrendszer",
        "Futómű",
        "Autóelektronika",
        "Általános szerviz"
    ]

    for _ in range(n):
        mechanic = Mechanic(
            id = next_id,
            name = fake.name_male(),
            experience_years = fake.random_int(min=min_experience, max=max_experience),
            specialization = fake.random_element(specializations)
        )
        next_id += 1
        mechanics.append(mechanic)

    return mechanics

def generate_data(n:int)->tuple[list[Car], list[Service], list[Mechanic]]:
    cars = generate_cars(n)
    mechanics = generate_mechanics(n)
    services = generate_services(cars, mechanics)

    return cars, services, mechanics
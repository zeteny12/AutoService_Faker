from data.basic.model_dataclasses import Car, Service, Mechanic
from openpyxl import Workbook, load_workbook
import os


def write_data_xlsx(cars: list[Car], services: list[Service], mechanics: list[Mechanic], path: str, file_name: str = "autoservice", extension: str = ".xlsx") -> None:
    os.makedirs(path, exist_ok = True)

    workbook = Workbook()
    cars_sheet = workbook.active
    cars_sheet.title = "Cars"
    services_sheet = workbook.create_sheet("Services")
    mechanics_sheet = workbook.create_sheet("Mechanics")

    cars_sheet.append(["plate", "type", "year", "automatic"])
    services_sheet.append(["id", "car_plate", "date", "description", "cost", "mechanic_id"])
    mechanics_sheet.append(["id", "name", "experience_years", "specialization"])

    for car in cars:
        cars_sheet.append([
            car.plate,
            car.type,
            car.year,
            car.automatic
        ])

    for service in services:
        services_sheet.append([
            service.id,
            service.car_plate,
            service.date,
            service.description,
            service.cost,
            service.mechanic_id
        ])

    for mechanic in mechanics:
        mechanics_sheet.append([
            mechanic.id,
            mechanic.name,
            mechanic.experience_years,
            mechanic.specialization
        ])

    workbook.save(os.path.join(path, file_name + extension))

def read_data_xlsx(path: str) -> tuple[list[Car], list[Service], list[Mechanic]]:
    workbook = load_workbook(os.path.join(path, "autoservice.xlsx"))
    cars_sheet = workbook["Cars"]
    services_sheet = workbook["Services"]
    mechanics_sheet = workbook["Mechanics"]

    cars = []
    for row in cars_sheet.iter_rows(min_row=2, values_only=True):
        car = Car(
            plate = row[0],
            type = row[1],
            year = row[2],
            automatic = row[3]
        )
        cars.append(car)

    services = []
    for row in services_sheet.iter_rows(min_row=2, values_only=True):
        service = Service(
            id = row[0],
            car_plate = row[1],
            date = row[2],
            description = row[3],
            cost = row[4],
            mechanic_id = row[5]
        )
        services.append(service)

    mechanics = []
    for row in mechanics_sheet.iter_rows(min_row=2, values_only=True):
        mechanic = Mechanic(
            id = row[0],
            name = row[1],
            experience_years = row[2],
            specialization = row[3]
        )
        mechanics.append(mechanic)

    return cars, services, mechanics
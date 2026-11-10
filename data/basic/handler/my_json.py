import json
import os
from data.basic.model_dataclasses import Car, Service


def write_cars_json(cars: list[Car], path: str, file_name: str = "cars_writer_json", extension: str = ".json", pretty: bool = True) -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name + extension), "w", encoding="utf-8") as file:
        json.dump(
            [car.__dict__ for car in cars],
            file,
            indent=2 if pretty else None,
            ensure_ascii=False
        )

def read_cars_json(path: str) -> list[Car]:
    cars = []
    with open(os.path.join(path, "cars_writer_json.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
        for row in data:
            car = Car(
                plate = row["plate"],
                type = row["type"],
                year = row["year"],
                automatic = row["automatic"]
            )
            cars.append(car)
    return cars


def write_services_json(services: list[Service], path: str, file_name: str = "services_writer_json", extension: str = ".json", pretty: bool = True) -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name + extension), "w", encoding="utf-8") as file:
        json.dump(
            [service.__dict__ for service in services],
            file,
            indent=2 if pretty else None,
            ensure_ascii=False
        )

def read_services_json(path: str) -> list[Service]:
    services = []
    with open(os.path.join(path, "services_writer_json.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
        for row in data:
            service = Service(
                id = row["id"],
                car_plate = row["car_plate"],
                date = row["date"],
                description = row["description"],
                cost = row["cost"]
            )
            services.append(service)
    return services
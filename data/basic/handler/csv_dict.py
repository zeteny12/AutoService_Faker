import csv
import os
from data.basic.model_dataclasses import Car, Service


def write_cars_csv(cars: list[Car], path: str, file_name: str = "cars_writer_csv", extension: str = ".csv", heading: bool = True, delimiter: str = ";") -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name + extension), "w", newline="", encoding="utf-8") as file:
        car_writer = csv.DictWriter(file, fieldnames=["plate", "type", "year", "automatic"], delimiter=delimiter)
        if heading:
            car_writer.writeheader()
        for car in cars:
            car_writer.writerow(car.__dict__)

def read_cars_csv(path: str) -> list[Car]:
    cars = []
    with open(os.path.join(path, "cars_writer_csv.csv"), "r", encoding="utf-8", newline="") as file:
        car_reader = csv.DictReader(file, delimiter=";")
        for row in car_reader:
            car = Car(
                plate = row["plate"],
                type = row["type"],
                year = int(row["year"]),
                automatic = row["automatic"] == "True"
            )
            cars.append(car)
        return cars


def write_services_csv(services: list[Service], path: str, file_name: str = "services_writer_csv", extension: str = ".csv", heading: bool = True, delimiter: str = ";") -> None:
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file_name + extension), "w", newline="", encoding="utf-8") as file:
        services_writer = csv.DictWriter(file, fieldnames=["id", "car_plate", "date", "description", "cost"], delimiter=delimiter)
        if heading:
            services_writer.writeheader()
        for service in services:
            services_writer.writerow(service.__dict__)

def read_services_csv(path: str) -> list[Service]:
    services = []
    with open(os.path.join(path, "services_writer_csv.csv"), "r", encoding="utf-8", newline="") as file:
        service_reader = csv.DictReader(file, delimiter=";")
        for row in service_reader:
            service = Service(
                id = int(row["id"]),
                car_plate = row["car_plate"],
                date = row["date"],
                description = row["description"],
                cost = int(row["cost"])
            )
            services.append(service)
        return services
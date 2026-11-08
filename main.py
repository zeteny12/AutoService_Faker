from data.basic.model_dataclasses import Car, Service
from data.basic.generator import *

#print(generate_hungarian_plate())

cars = generate_cars(5)
"""for car in cars:
    print(car)"""

services = generate_services(cars)
for service in services:
    print(service)
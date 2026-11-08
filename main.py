from data.basic.model_dataclasses import Car, Service
from data.basic.generator import generate_hungarian_plate, generate_cars

#print(generate_hungarian_plate())

cars = generate_cars(1000)
for car in cars:
    print(car.plate)
print(len(cars))
print(len(set(car.plate for car in cars)))
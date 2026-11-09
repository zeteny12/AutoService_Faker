from data.basic.generator import generate_data
from data.basic.handler.csv_dict import write_cars, write_services, read_cars, read_services

cars, services = generate_data(5)


write_cars(cars, path = "./csv_files")
loaded_cars = read_cars("./csv_files")

for car in loaded_cars:
    print(car)
print(cars == loaded_cars)


write_services(services, path = "./csv_files")
loaded_services = read_services("./csv_files")

for service in loaded_services:
    print(service)
print(services == loaded_services)


plates = set(car.plate for car in loaded_cars)
print(all(service.car_plate in plates for service in loaded_services))
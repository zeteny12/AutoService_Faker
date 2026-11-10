from data.basic.generator import generate_data
from data.basic.handler.csv_dict import write_cars_csv, write_services_csv, read_cars_csv, read_services_csv
from data.basic.handler.my_json import write_cars_json, write_services_json, read_cars_json, read_services_json

cars, services = generate_data(5)


# write_cars_csv(cars, path = "./csv_files")
# loaded_cars = read_cars_csv("./csv_files")
# for car in loaded_cars:
#     print(car)
# print(cars == loaded_cars)
#
# write_services_csv(services, path = "./csv_files")
# loaded_services = read_services_csv("./csv_files")
# for service in loaded_services:
#     print(service)
# print(services == loaded_services)
#
# plates = set(car.plate for car in loaded_cars)
# print(all(service.car_plate in plates for service in loaded_services))


write_cars_json(cars, path = "./json_files")
write_services_json(services, path = "./json_files")

loaded_cars_json = read_cars_json("./json_files")
print(cars == loaded_cars_json)
for car in loaded_cars_json:
    print(car)

loaded_services_json = read_services_json("./json_files")
print(services == loaded_services_json)
for service in loaded_services_json:
    print(service)

plates = set(car.plate for car in loaded_cars_json)
print(all(service.car_plate in plates for service in loaded_services_json))
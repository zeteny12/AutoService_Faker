from data.basic.generator import generate_data, generate_cars, generate_mechanics, generate_services
from data.basic.handler.csv_dict import write_cars_csv, write_services_csv, read_cars_csv, read_services_csv, write_mechanics_csv, read_mechanics_csv
from data.basic.handler.my_json import write_cars_json, write_services_json, read_cars_json, read_services_json, write_mechanics_json, read_mechanics_json
from data.basic.handler.xlsx import write_data_xlsx, read_data_xlsx
from data.basic.handler.oracle_db import test_connection, create_car_table, create_mechanic_table, create_service_table, insert_data, check_table_counts

"""Data generator"""
cars, services, mechanics = generate_data(20)


"""Parameterized generator TESTS"""
test_mechanics = generate_mechanics(5, 30, 40)
# for i in test_mechanics:
#     print(i)
print("Mechanics experience (30 - 40):", all(30 <= i.experience_years <= 40 for i in test_mechanics))

test_cars = generate_cars(5, 2020, 2022)
# for i in test_cars:
#     print(i)
print("Cars manufacturing year (2020 - 2022):", all(2020 <= i.year <= 2022 for i in test_cars))

test_services = generate_services(cars, mechanics, 10_000, 20_000)
# for i in test_services:
#     print(i)
print("Service costs (10.000 - 20.000):", all(10_000 <= i.cost <= 20_000 for i in test_services))


"""CSV Read / Write TESTING"""
write_cars_csv(cars, "./csv_files")
loaded_cars = read_cars_csv("./csv_files")
# for car in loaded_cars:
#     print(car)
print("\nCSV Cars:", cars == loaded_cars)

write_services_csv(services, "./csv_files")
loaded_services = read_services_csv("./csv_files")
# for service in loaded_services:
#     print(service)
print("CSV Services:", services == loaded_services)

write_mechanics_csv(mechanics, "./csv_files")
loaded_mechanics = read_mechanics_csv("./csv_files")
# for i in loaded_mechanics:
#     print(i)
print("CSV Mechanics:", mechanics == loaded_mechanics)


"""JSON Read / Write TESTING"""
write_cars_json(cars,  "./json_files")
write_services_json(services,  "./json_files")
write_mechanics_json(mechanics, "./json_files")

loaded_cars_json = read_cars_json("./json_files")
print("\nJSON Cars:", cars == loaded_cars_json)
# for car in loaded_cars_json:
#     print(car)

loaded_services_json = read_services_json("./json_files")
print("JSON Services:", services == loaded_services_json)
# for service in loaded_services_json:
#     print(service)

loaded_mechanics_json = read_mechanics_json("./json_files")
print("JSON Mechanics:", mechanics == loaded_mechanics_json)
# for mechanic in loaded_mechanics_json:
#     print(mechanic)


"""XLSX Read / Write TESTING"""
write_data_xlsx(cars, services, mechanics,"xlsx_files")
loaded_cars_xlsx, loaded_services_xlsx, loaded_mechanics_xlsx = read_data_xlsx("xlsx_files")

print("\nXLSX Cars:", cars == loaded_cars_xlsx)
# for car in loaded_cars_xlsx:
#     print(car)

print("XLSX Services:", services == loaded_services_xlsx)
# for service in loaded_services_xlsx:
#     print(service)

print("XLSX Mechanics:", mechanics == loaded_mechanics_xlsx)
# for mechanic in loaded_mechanics_xlsx:
#     print(mechanic)


"""Relationships"""
plates = set(car.plate for car in cars)
print("\nCar-Service relationship:", all(service.car_plate in plates for service in services))

mechanic_ids = set(mechanic.id for mechanic in mechanics)
print("Mechanic-Service relationship:", all(service.mechanic_id in mechanic_ids for service in services))


"""Unique Primary Keys TESTS"""
print("\nUnique Car plates:", len(plates) == len(cars))

print("Unique Mechanic IDs:", len(mechanic_ids) == len(mechanics))

service_ids = set(service.id for service in services)
print("Unique Service IDs:", len(service_ids) == len(services))


"""ORACLE SQL TESTING"""
print("")

test_connection()

create_car_table()
create_mechanic_table()
create_service_table()

insert_data(cars, services, mechanics)
check_table_counts()
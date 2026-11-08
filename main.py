from data.basic.generator import generate_data

cars, services = generate_data(5)

for car in cars:
    print(car)

for service in services:
    print(service)
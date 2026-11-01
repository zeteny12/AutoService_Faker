from data.basic.model_dataclasses import Car, Service

car = Car(
    plate="JVF-145",
    type="Suzuki Swift",
    year=2005,
    automatic=False
)
print(car)

service = Service(
    id=1,
    car_plate="JVF-145",
    date="2026-11-04",
    description="Féktárcsa",
    cost=21000
)
print(service)
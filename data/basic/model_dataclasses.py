from dataclasses import dataclass

@dataclass
class Car:
    plate: str
    type: str
    year: int
    automatic: bool

@dataclass
class Service:
    id: int
    car_plate: str
    date: str
    description: str
    cost: int
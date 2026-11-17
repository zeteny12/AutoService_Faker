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
    mechanic_id: int

@dataclass
class Mechanic:
    id: int
    name: str
    experience_years: int
    specialization: str
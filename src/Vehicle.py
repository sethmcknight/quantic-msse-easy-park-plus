from typing import Literal

#Vehicle class for use with Parking Lot Manager
class Vehicle:
    color: str
    registrationNumber: str
    make: str
    model: str

    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        self.color = color
        self.registrationNumber = registrationNumber
        self.make = make
        self.model = model

    def getMake(self) -> str:
        return self.make

    def getModel(self) -> str:
        return self.model

    def getColor(self) -> str:
        return self.color

    def getRegistrationNumber(self) -> str:
        return self.registrationNumber

class Car(Vehicle):
    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        super().__init__(registrationNumber, make, model, color)

    def getType(self) -> Literal["Car"]:
        return "Car"

class Truck(Vehicle):
    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        super().__init__(registrationNumber, make, model, color)

    def getType(self) -> Literal["Truck"]:
        return "Truck"


class Motorcycle(Vehicle):
    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        super().__init__(registrationNumber, make, model, color)

    def getType(self) -> Literal["Motorcycle"]:
        return "Motorcycle"


class Bus(Vehicle):

    def __init__(self, registrationNumber: str, make: str, model: str, color: str):
        Vehicle.__init__(self, registrationNumber, make, model, color)

    def getType(self):
        return "Bus"




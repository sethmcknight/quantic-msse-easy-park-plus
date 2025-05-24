from typing import Literal

# TODO: Refactor or remove unused getType() methods and unnecessary ElectricVehicle hierarchy. See anti-patterns.md.
class ElectricVehicle:
    color: str
    registrationNumber: str
    make: str
    model: str
    charge: int

    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        self.color = color
        self.registrationNumber = registrationNumber
        self.make = make
        self.model = model
        self.charge = 0

    def getMake(self) -> str:
        return self.make

    def getModel(self) -> str:
        return self.model

    def getColor(self) -> str:
        return self.color

    def getRegistrationNumber(self) -> str:
        return self.registrationNumber

    def setCharge(self, charge: int) -> None:
        self.charge = charge

    def getCharge(self) -> int:
        return self.charge

class ElectricCar(ElectricVehicle):
    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        super().__init__(registrationNumber, make, model, color)

    def getType(self) -> Literal["Car"]:
        return "Car"

class ElectricBike(ElectricVehicle):
    def __init__(self, registrationNumber: str, make: str, model: str, color: str) -> None:
        super().__init__(registrationNumber, make, model, color)

    def getType(self) -> Literal["Motorcycle"]:
        return "Motorcycle"

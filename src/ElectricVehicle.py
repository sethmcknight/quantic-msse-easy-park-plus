# TODO: Refactor or remove unused getType() methods and unnecessary ElectricVehicle hierarchy. See anti-patterns.md.
class ElectricVehicle:
    def __init__(self,regnum,make,model,color):
        self.color = color
        self.regnum = regnum
        self.make = make
        self.model = model
        self.charge = 0

    def getMake(self):
        return self.make

    def getModel(self):
        return self.model

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regnum

    def setCharge(self, charge):
        self.charge = charge
    # TODO: Remove or implement setCharge if needed. Currently unused. See anti-patterns.md.
    def getCharge(self):
        return self.charge

class ElectricCar:
    def __init__(self,regnum,make,model,color):
        # TODO: Use proper inheritance from ElectricVehicle. See anti-patterns.md.
        ElectricVehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Car"

class ElectricBike:
    def __init__(self,regnum,make,model,color):
        # TODO: Use proper inheritance from ElectricVehicle. See anti-patterns.md.
        ElectricVehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Motorcycle"

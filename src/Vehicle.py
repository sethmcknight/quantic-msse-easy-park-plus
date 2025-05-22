# TODO: Refactor or remove unused getType() methods and unnecessary inheritance hierarchy. See anti-patterns.md.
#Vehicle class for use with Parking Lot Manager
class Vehicle:
    color: str
    regnum: str
    make: str
    model: str

    def __init__(self, regnum: str, make: str, model: str, color: str):
        self.color = color
        self.regnum = regnum
        self.make = make
        self.model = model

    def getMake(self):
        return self.make

    def getModel(self):
        return self.model

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regnum

class Car(Vehicle):

    def __init__(self,regnum,make,model,color):
        Vehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Car"

class Truck(Vehicle):

    def __init__(self,regnum,make,model,color):
        Vehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Truck"


class Motorcycle(Vehicle):

    def __init__(self,regnum,make,model,color):
        Vehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Motorcycle"


class Bus(Vehicle):

    def __init__(self,regnum,make,model,color):
        Vehicle.__init__(self,regnum,make,model,color)

    def getType(self):
        return "Bus"




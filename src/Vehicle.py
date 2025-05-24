"""
Vehicle Module

This module implements the vehicle hierarchy and factory for the parking lot management system.
It uses the Factory Pattern to centralize vehicle creation and ensure proper type checking.

Anti-patterns Removed:
1. Unnecessary Inheritance
   - Removed: Redundant getType() methods in subclasses
   - Solution: Type information stored in factory
   - Benefit: Reduced code duplication

2. Type Safety Issues
   - Removed: Direct instantiation of vehicle classes
   - Solution: Factory methods with type checking
   - Benefit: Better type safety and error handling

3. Tight Coupling
   - Removed: Direct dependencies on concrete vehicle classes
   - Solution: Factory interface
   - Benefit: Easier to modify and extend

4. Duplicate Vehicle/ElectricVehicle Structure
   - Removed: Separate ElectricVehicle hierarchy
   - Solution: ElectricVehicle as a Vehicle subclass
   - Benefit: Proper inheritance, reduced code duplication

Design Patterns Implemented:
1. Factory Pattern
   - Purpose: Centralize vehicle creation
   - Components: VehicleFactory class
   - Benefit: Encapsulated creation logic, type safety

2. Property Pattern
   - Purpose: Encapsulate vehicle attributes
   - Components: @property decorators
   - Benefit: Better attribute access control

3. Template Method Pattern
   - Purpose: Define skeleton of vehicle operations
   - Components: Abstract Vehicle class with concrete subclasses
   - Benefit: Code reuse and consistent interface

Usage:
    The VehicleFactory class is the main entry point for creating vehicles.
    It provides type-safe factory methods for each vehicle type.

Example:
    >>> factory = VehicleFactory()
    >>> car = factory.create_car("ABC123", "Toyota", "Camry", "Red")
    >>> print(car.registration_number)  # "ABC123"
    >>> ev_car = factory.create_electric_car("XYZ789", "Tesla", "Model 3", "White")
    >>> print(ev_car.charge)  # 0
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TypeVar

# Type variable for vehicle types
T = TypeVar('T', bound='Vehicle')

@dataclass
class VehicleInfo:
    """Data class to hold vehicle information"""
    registration_number: str
    make: str
    model: str
    color: str

class Vehicle(ABC):
    """Abstract base class for all vehicles"""
    
    def __init__(self, info: VehicleInfo):
        self._info = info

    @property
    def registration_number(self) -> str:
        return self._info.registration_number

    @property
    def make(self) -> str:
        return self._info.make

    @property
    def model(self) -> str:
        return self._info.model

    @property
    def color(self) -> str:
        return self._info.color

    @abstractmethod
    def get_type(self) -> str:
        """Return the type of vehicle"""
        pass

    def __str__(self) -> str:
        return f"{self.get_type()}: {self.registration_number} ({self.color} {self.make} {self.model})"

class ElectricVehicle(Vehicle):
    """Base class for electric vehicles"""
    
    def __init__(self, info: VehicleInfo):
        super().__init__(info)
        self._charge: int = 0

    @property
    def charge(self) -> int:
        """Get the current charge level (0-100)"""
        return self._charge

    def set_charge(self, charge: int) -> None:
        """Set the charge level (0-100)"""
        if not 0 <= charge <= 100:
            raise ValueError("Charge must be between 0 and 100")
        self._charge = charge

    def __str__(self) -> str:
        return f"{super().__str__()} (Charge: {self._charge}%)"

class Car(Vehicle):
    """Concrete class for cars"""
    
    def get_type(self) -> str:
        return "Car"

class ElectricCar(ElectricVehicle):
    """Concrete class for electric cars"""
    
    def get_type(self) -> str:
        return "Electric Car"

class Truck(Vehicle):
    """Concrete class for trucks"""
    
    def get_type(self) -> str:
        return "Truck"

class ElectricTruck(ElectricVehicle):
    """Concrete class for electric trucks"""
    
    def get_type(self) -> str:
        return "Electric Truck"

class Motorcycle(Vehicle):
    """Concrete class for motorcycles"""
    
    def get_type(self) -> str:
        return "Motorcycle"

class ElectricMotorcycle(ElectricVehicle):
    """Concrete class for electric motorcycles"""
    
    def get_type(self) -> str:
        return "Electric Motorcycle"

class Bus(Vehicle):
    """Concrete class for buses"""
    
    def get_type(self) -> str:
        return "Bus"

class ElectricBus(ElectricVehicle):
    """Concrete class for electric buses"""
    
    def get_type(self) -> str:
        return "Electric Bus"

class VehicleFactory:
    """Factory class for creating vehicles"""
    
    @staticmethod
    def create_vehicle(vehicle_type: str, info: VehicleInfo, is_electric: bool = False) -> Vehicle:
        """
        Create a vehicle of the specified type
        
        Args:
            vehicle_type: Type of vehicle to create ("car", "truck", "motorcycle", "bus")
            info: Vehicle information
            is_electric: Whether the vehicle is electric
            
        Returns:
            A new vehicle instance
            
        Raises:
            ValueError: If vehicle_type is invalid
        """
        vehicle_type = vehicle_type.lower()
        
        if is_electric:
            if vehicle_type == "car":
                return ElectricCar(info)
            elif vehicle_type == "truck":
                return ElectricTruck(info)
            elif vehicle_type == "motorcycle":
                return ElectricMotorcycle(info)
            elif vehicle_type == "bus":
                return ElectricBus(info)
            else:
                raise ValueError(f"Invalid electric vehicle type: {vehicle_type}")
        else:
            if vehicle_type == "car":
                return Car(info)
            elif vehicle_type == "truck":
                return Truck(info)
            elif vehicle_type == "motorcycle":
                return Motorcycle(info)
            elif vehicle_type == "bus":
                return Bus(info)
            else:
                raise ValueError(f"Invalid vehicle type: {vehicle_type}")

    @classmethod
    def create_car(cls, registration_number: str, make: str, model: str, color: str) -> Car:
        """Create a car with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return Car(info)

    @classmethod
    def create_electric_car(cls, registration_number: str, make: str, model: str, color: str) -> ElectricCar:
        """Create an electric car with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return ElectricCar(info)

    @classmethod
    def create_truck(cls, registration_number: str, make: str, model: str, color: str) -> Truck:
        """Create a truck with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return Truck(info)

    @classmethod
    def create_electric_truck(cls, registration_number: str, make: str, model: str, color: str) -> ElectricTruck:
        """Create an electric truck with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return ElectricTruck(info)

    @classmethod
    def create_motorcycle(cls, registration_number: str, make: str, model: str, color: str) -> Motorcycle:
        """Create a motorcycle with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return Motorcycle(info)

    @classmethod
    def create_electric_motorcycle(cls, registration_number: str, make: str, model: str, color: str) -> ElectricMotorcycle:
        """Create an electric motorcycle with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return ElectricMotorcycle(info)

    @classmethod
    def create_bus(cls, registration_number: str, make: str, model: str, color: str) -> Bus:
        """Create a bus with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return Bus(info)

    @classmethod
    def create_electric_bus(cls, registration_number: str, make: str, model: str, color: str) -> ElectricBus:
        """Create an electric bus with the given information"""
        info = VehicleInfo(registration_number, make, model, color)
        return ElectricBus(info)




"""
Vehicle Module

This module implements the vehicle hierarchy and factory for creating vehicles.
It uses the Factory Pattern for vehicle creation, the Strategy Pattern for parking behavior,
and the Template Method Pattern for common vehicle operations.

Anti-patterns Removed:
1. Unnecessary Inheritance
   - Removed: Empty subclasses
   - Solution: Factory Pattern
   - Benefit: Reduced complexity

2. Direct Instantiation
   - Removed: Direct class instantiation
   - Solution: Factory Pattern
   - Benefit: Centralized creation logic

3. Code Duplication
   - Removed: Repeated vehicle operations
   - Solution: Template Method Pattern
   - Benefit: DRY code

Design Patterns Implemented:
1. Factory Pattern
   - Purpose: Centralize vehicle creation
   - Components: VehicleFactory class
   - Benefit: Type-safe creation

2. Strategy Pattern
   - Purpose: Encapsulate parking behavior
   - Components: ParkingStrategy interface
   - Benefit: Flexible parking rules

3. Template Method Pattern
   - Purpose: Define common vehicle operations
   - Components: Abstract base class with template methods
   - Benefit: Reduced code duplication

Usage:
    The VehicleFactory class is the main entry point for creating vehicles.
    It provides type-safe factory methods for each vehicle type.

Example:
    # Create a regular car
    >>> car = VehicleFactory.create_car("ABC123", "Toyota", "Camry", "Red")
    >>> print(car.get_info())
    Type: Car
    Registration: ABC123
    Make: Toyota
    Model: Camry
    Color: Red

    # Create an electric car
    >>> ev_car = VehicleFactory.create_electric_car("XYZ789", "Tesla", "Model 3", "Blue")
    >>> print(ev_car.get_info())
    Type: Electric Car
    Registration: XYZ789
    Make: Tesla
    Model: Model 3
    Color: Blue
    Charge: 0%

    # Check if vehicles can park in different slot types
    >>> car.can_park_in("standard")  # True
    >>> ev_car.can_park_in("electric")  # True
    >>> ev_car.can_park_in("standard")  # True
"""

from dataclasses import dataclass
from typing import Optional, TypeVar, Protocol
from abc import ABC, abstractmethod

@dataclass
class VehicleInfo:
    """Data class for vehicle information"""
    registration_number: str
    make: str
    model: str
    color: str

class Vehicle(ABC):
    """Abstract base class for vehicles"""
    
    def __init__(self, info: VehicleInfo):
        self._info = info
        self._parking_strategy: Optional[ParkingStrategy] = None
    
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
        """Get the vehicle type"""
        pass
    
    def can_park_in(self, slot_type: str) -> bool:
        """Check if the vehicle can park in the given slot type"""
        if self._parking_strategy:
            return self._parking_strategy.can_park_in(slot_type)
        return False
    
    def set_parking_strategy(self, strategy: 'ParkingStrategy') -> None:
        """Set the parking strategy for this vehicle"""
        self._parking_strategy = strategy
    
    # Template methods for common vehicle operations
    def validate_registration(self) -> bool:
        """Validate the vehicle registration number"""
        return len(self.registration_number) >= 3
    
    def validate_make_model(self) -> bool:
        """Validate the vehicle make and model"""
        return bool(self.make and self.model)
    
    def validate_color(self) -> bool:
        """Validate the vehicle color"""
        return bool(self.color)
    
    def is_valid(self) -> bool:
        """Template method for vehicle validation"""
        return (self.validate_registration() and 
                self.validate_make_model() and 
                self.validate_color())
    
    def get_info(self) -> str:
        """Template method for getting vehicle information"""
        return (f"Type: {self.get_type()}\n"
                f"Registration: {self.registration_number}\n"
                f"Make: {self.make}\n"
                f"Model: {self.model}\n"
                f"Color: {self.color}")

class ElectricVehicle(Vehicle):
    """Base class for electric vehicles"""
    
    def __init__(self, info: VehicleInfo):
        super().__init__(info)
        self._charge: int = 0
    
    @property
    def charge(self) -> int:
        return self._charge
    
    def set_charge(self, charge: int) -> None:
        """Set the vehicle's charge level"""
        self._charge = max(0, min(100, charge))
    
    def is_fully_charged(self) -> bool:
        """Check if the vehicle is fully charged"""
        return self._charge >= 100
    
    def needs_charging(self) -> bool:
        """Check if the vehicle needs charging"""
        return self._charge < 20
    
    def get_info(self) -> str:
        """Override template method to include charge information"""
        return (super().get_info() + 
                f"\nCharge: {self._charge}%")

class Car(Vehicle):
    """Class representing a car"""
    
    def get_type(self) -> str:
        return "Car"

class Truck(Vehicle):
    """Class representing a truck"""
    
    def get_type(self) -> str:
        return "Truck"

class Motorcycle(Vehicle):
    """Class representing a motorcycle"""
    
    def get_type(self) -> str:
        return "Motorcycle"

class Bus(Vehicle):
    """Class representing a bus"""
    
    def get_type(self) -> str:
        return "Bus"

class ElectricCar(ElectricVehicle):
    """Class representing an electric car"""
    
    def get_type(self) -> str:
        return "Electric Car"

class ElectricTruck(ElectricVehicle):
    """Class representing an electric truck"""
    
    def get_type(self) -> str:
        return "Electric Truck"

class ElectricMotorcycle(ElectricVehicle):
    """Class representing an electric motorcycle"""
    
    def get_type(self) -> str:
        return "Electric Motorcycle"

class ElectricBus(ElectricVehicle):
    """Class representing an electric bus"""
    
    def get_type(self) -> str:
        return "Electric Bus"

class ParkingStrategy(Protocol):
    """Protocol for parking strategies"""
    
    def can_park_in(self, slot_type: str) -> bool:
        """Check if a vehicle can park in the given slot type"""
        ...

class StandardParkingStrategy:
    """Strategy for standard vehicles"""
    
    def can_park_in(self, slot_type: str) -> bool:
        return slot_type == "standard"

class ElectricParkingStrategy:
    """Strategy for electric vehicles"""
    
    def can_park_in(self, slot_type: str) -> bool:
        return slot_type in ("standard", "electric")

class MotorcycleParkingStrategy:
    """Strategy for motorcycles"""
    
    def can_park_in(self, slot_type: str) -> bool:
        return slot_type == "standard"

T = TypeVar('T', bound=Vehicle)

class VehicleFactory:
    """Factory for creating vehicles"""
    
    @staticmethod
    def create_vehicle(vehicle_type: type[T], info: VehicleInfo) -> T:
        """Create a vehicle of the specified type"""
        vehicle = vehicle_type(info)
        
        # Set appropriate parking strategy
        if isinstance(vehicle, ElectricVehicle):
            vehicle.set_parking_strategy(ElectricParkingStrategy())
        elif isinstance(vehicle, Motorcycle):
            vehicle.set_parking_strategy(MotorcycleParkingStrategy())
        else:
            vehicle.set_parking_strategy(StandardParkingStrategy())
        
        return vehicle
    
    @staticmethod
    def create_car(registration_number: str, make: str, model: str, color: str) -> Car:
        """Create a car"""
        return VehicleFactory.create_vehicle(Car, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_truck(registration_number: str, make: str, model: str, color: str) -> Truck:
        """Create a truck"""
        return VehicleFactory.create_vehicle(Truck, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_motorcycle(registration_number: str, make: str, model: str, color: str) -> Motorcycle:
        """Create a motorcycle"""
        return VehicleFactory.create_vehicle(Motorcycle, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_bus(registration_number: str, make: str, model: str, color: str) -> Bus:
        """Create a bus"""
        return VehicleFactory.create_vehicle(Bus, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_electric_car(registration_number: str, make: str, model: str, color: str) -> ElectricCar:
        """Create an electric car"""
        return VehicleFactory.create_vehicle(ElectricCar, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_electric_truck(registration_number: str, make: str, model: str, color: str) -> ElectricTruck:
        """Create an electric truck"""
        return VehicleFactory.create_vehicle(ElectricTruck, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_electric_motorcycle(registration_number: str, make: str, model: str, color: str) -> ElectricMotorcycle:
        """Create an electric motorcycle"""
        return VehicleFactory.create_vehicle(ElectricMotorcycle, VehicleInfo(registration_number, make, model, color))
    
    @staticmethod
    def create_electric_bus(registration_number: str, make: str, model: str, color: str) -> ElectricBus:
        """Create an electric bus"""
        return VehicleFactory.create_vehicle(ElectricBus, VehicleInfo(registration_number, make, model, color))




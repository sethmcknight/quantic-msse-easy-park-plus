"""
Vehicle classes for the parking system.

This module defines the vehicle classes used in the parking system.
"""

from dataclasses import dataclass
from typing import Optional, TypeVar, Protocol, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Vehicle:
    """Base class for all vehicles"""
    registration_number: str
    manufacturer: str
    model: str
    color: str
    is_electric: bool
    is_motorcycle: bool
    vehicle_type: VehicleType
    
    def __post_init__(self):
        """Validate vehicle data"""
        if not self.registration_number:
            raise ValueError("Registration number is required")
        if not self.manufacturer:
            raise ValueError("Manufacturer is required")
        if not self.model:
            raise ValueError("Model is required")
        if not self.color:
            raise ValueError("Color is required")
    
    def get_vehicle_type(self) -> VehicleType:
        """Get the vehicle type"""
        return self.vehicle_type
    
    def get_status(self) -> str:
        """Get the vehicle status"""
        return (f"Registration: {self.registration_number}\n"
                f"Manufacturer: {self.manufacturer}\n"
                f"Model: {self.model}\n"
                f"Color: {self.color}\n"
                f"Type: {self.vehicle_type.name}")

@dataclass
class ElectricVehicle(Vehicle):
    """Class for electric vehicles"""
    charge_level: float = 0.0
    
    def __post_init__(self):
        """Validate electric vehicle data"""
        super().__post_init__()
        if not self.is_electric:
            raise ValueError("Electric vehicle must have is_electric=True")
        if self.charge_level < 0 or self.charge_level > 100:
            raise ValueError("Charge level must be between 0 and 100")
    
    def set_charge(self, charge: float) -> None:
        """Set the charge level
        
        Args:
            charge: The new charge level (0-100)
        """
        if charge < 0 or charge > 100:
            raise ValueError("Charge level must be between 0 and 100")
        self.charge_level = charge
    
    def get_charge(self) -> float:
        """Get the current charge level
        
        Returns:
            float: The current charge level (0-100)
        """
        return self.charge_level
    
    def get_status(self) -> str:
        """Get the vehicle status"""
        return (super().get_status() + "\n"
                f"Charge Level: {self.charge_level}%")

@dataclass
class Car(Vehicle):
    """Class representing a car"""
    
    def __init__(self, info: VehicleInfo) -> None:
        super().__init__(info)

    def get_type(self) -> Literal["Car"]:
        """Return the type of this vehicle"""
        return "Car"

class Truck(Vehicle):
    """Class representing a truck"""
    
    def __init__(self, info: VehicleInfo) -> None:
        super().__init__(info)
    
    def get_type(self) -> str:
        return "Truck"

class Motorcycle(Vehicle):
    """Class representing a motorcycle"""
    
    def __init__(self, info: VehicleInfo) -> None:
        super().__init__(info)
    
    def get_type(self) -> str:
        return "Motorcycle"

class Bus(Vehicle):
    """Class representing a bus"""
    
    def __init__(self, info: VehicleInfo) -> None:
        super().__init__(info)
    
    def get_type(self) -> str:
        return "Bus"

class ElectricCar(ElectricVehicle):
    """Class for electric cars"""
    def __post_init__(self):
        """Validate electric car data"""
        super().__post_init__()
        if self.is_motorcycle:
            raise ValueError("Electric car cannot be a motorcycle")
        self.vehicle_type = VehicleType.ELECTRIC_CAR

@dataclass
class Motorcycle(Vehicle):
    """Class for motorcycles"""
    def __post_init__(self):
        """Validate motorcycle data"""
        super().__post_init__()
        if not self.is_motorcycle:
            raise ValueError("Motorcycle must have is_motorcycle=True")
        if self.is_electric:
            raise ValueError("Motorcycle cannot be electric")
        self.vehicle_type = VehicleType.MOTORCYCLE

@dataclass
class ElectricMotorcycle(ElectricVehicle):
    """Class for electric motorcycles"""
    def __post_init__(self):
        """Validate electric motorcycle data"""
        super().__post_init__()
        if not self.is_motorcycle:
            raise ValueError("Electric motorcycle must have is_motorcycle=True")
        self.vehicle_type = VehicleType.ELECTRIC_MOTORCYCLE

@dataclass
class Truck(Vehicle):
    """Class for trucks"""
    def __post_init__(self):
        """Validate truck data"""
        super().__post_init__()
        if self.is_motorcycle:
            raise ValueError("Truck cannot be a motorcycle")
        if self.is_electric:
            raise ValueError("Truck cannot be electric")
        self.vehicle_type = VehicleType.TRUCK

@dataclass
class Bus(Vehicle):
    """Class for buses"""
    def __post_init__(self):
        """Validate bus data"""
        super().__post_init__()
        if self.is_motorcycle:
            raise ValueError("Bus cannot be a motorcycle")
        if self.is_electric:
            raise ValueError("Bus cannot be electric")
        self.vehicle_type = VehicleType.BUS




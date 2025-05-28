"""
Vehicle Module

This module defines the vehicle classes for the parking system.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto

class VehicleType(Enum):
    """Enum for vehicle types"""
    CAR = auto()
    TRUCK = auto()
    MOTORCYCLE = auto()
    BUS = auto()

    @classmethod
    def from_string(cls, type_str: str) -> 'VehicleType':
        """Convert string to VehicleType enum"""
        try:
            return cls[type_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid vehicle type: {type_str}")

@dataclass
class Vehicle:
    """Base class for all vehicles"""
    registration_number: str
    manufacturer: str
    model: str
    color: str
    vehicle_type: VehicleType
    is_electric: bool = False
    current_battery_charge: Optional[float] = None

    def __post_init__(self):
        """Initialize vehicle after creation"""
        if self.is_electric and self.current_battery_charge is None:
            self.current_battery_charge = 0.0

    def get_type(self) -> str:
        """Get vehicle type as string"""
        type_str = self.vehicle_type.name.lower()
        return f"electric_{type_str}" if self.is_electric else type_str

    def get_manufacturer(self) -> str:
        """Get vehicle manufacturer"""
        return self.manufacturer

    def get_model(self) -> str:
        """Get vehicle model"""
        return self.model

    def get_color(self) -> str:
        """Get vehicle color"""
        return self.color

    def get_registration_number(self) -> str:
        """Get vehicle registration number"""
        return self.registration_number

    def get_battery_charge(self) -> Optional[float]:
        """Get current battery charge if electric vehicle"""
        return self.current_battery_charge if self.is_electric else None

    def set_battery_charge(self, charge: float) -> None:
        """Set battery charge for electric vehicles"""
        if self.is_electric:
            self.current_battery_charge = max(0.0, min(100.0, charge))
        else:
            raise ValueError("Cannot set battery charge for non-electric vehicle")

    def __str__(self) -> str:
        """String representation of vehicle"""
        base_info = f"{self.manufacturer} {self.model} ({self.color}) - {self.registration_number}"
        if self.is_electric and self.current_battery_charge is not None:
            return f"{base_info} - Battery: {self.current_battery_charge}%"
        return base_info

def create_vehicle(
    registration_number: str,
    manufacturer: str,
    model: str,
    color: str,
    vehicle_type: VehicleType,
    is_electric: bool = False,
    current_battery_charge: Optional[float] = None
) -> Vehicle:
    """Factory function to create vehicles"""
    return Vehicle(
        registration_number=registration_number,
        manufacturer=manufacturer,
        model=model,
        color=color,
        vehicle_type=vehicle_type,
        is_electric=is_electric,
        current_battery_charge=current_battery_charge
    )




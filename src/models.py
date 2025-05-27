"""
Data models for the parking system.

This module defines the data structures used throughout the parking system.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto

class SlotType(Enum):
    """Types of parking slots"""
    REGULAR = auto()
    ELECTRIC = auto()

class VehicleType(Enum):
    """Types of vehicles"""
    CAR = auto()
    TRUCK = auto()
    BUS = auto()
    MOTORCYCLE = auto()
    ELECTRIC_CAR = auto()
    ELECTRIC_MOTORCYCLE = auto()

@dataclass
class VehicleData:
    """Data transfer object for vehicle information"""
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

@dataclass
class ParkingLevelData:
    """Data transfer object for parking level information"""
    level_number: int
    regular_slots: int
    electric_slots: int
    
    def __post_init__(self):
        """Validate level data"""
        if self.level_number < 1:
            raise ValueError("Level number must be positive")
        if self.regular_slots < 0:
            raise ValueError("Number of regular slots cannot be negative")
        if self.electric_slots < 0:
            raise ValueError("Number of electric slots cannot be negative")

@dataclass
class ParkingLotData:
    """Data transfer object for parking lot information"""
    name: str
    levels: List[ParkingLevelData]
    
    def __post_init__(self):
        """Validate lot data"""
        if not self.name:
            raise ValueError("Lot name is required")
        if not self.levels:
            raise ValueError("At least one level is required")

@dataclass
class SearchCriteria:
    """Search criteria for finding vehicles"""
    registration_number: Optional[str] = None
    color: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    is_electric: Optional[bool] = None
    is_motorcycle: Optional[bool] = None
    
    def is_empty(self) -> bool:
        """Check if search criteria is empty"""
        return all(value is None for value in self.__dict__.values())

@dataclass
class ParkingStatus:
    """Status information for a parking lot"""
    lot_name: str
    level: int
    slot: int
    vehicle: Optional[VehicleData]
    slot_type: SlotType
    is_occupied: bool
    is_charging: bool = False
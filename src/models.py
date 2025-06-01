"""
Data Models Module

This module defines the data models used in the parking system.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto
from Vehicle import VehicleType

class SlotType(Enum):
    """Enum for slot types"""
    REGULAR = auto()
    ELECTRIC = auto()

@dataclass
class VehicleData:
    """Data transfer object for vehicle information"""
    registration_number: str  # Unique identifier for the vehicle
    manufacturer: str  # Manufacturer of the vehicle (e.g., Toyota, Tesla)
    model: str  # Model of the vehicle (e.g., Camry, Model 3)
    color: str  # Color of the vehicle
    is_electric: bool  # Flag indicating if the vehicle is electric
    is_motorcycle: bool # Flag indicating if the vehicle is a motorcycle
    vehicle_type: VehicleType  # Type of the vehicle (e.g., CAR, TRUCK)
    current_battery_charge: Optional[float] = None  # Current battery charge percentage for electric vehicles

@dataclass
class ParkingSlotData:
    """Data transfer object for parking slot information"""
    slot_number: int  # Unique identifier for the slot within its level
    is_occupied: bool  # Flag indicating if the slot is currently occupied
    vehicle: Optional[VehicleData] = None  # VehicleData object if a vehicle is parked, else None
    slot_type: SlotType = SlotType.REGULAR  # Type of the parking slot (e.g., REGULAR, ELECTRIC)
    level: int = 0  # The level number where this slot is located
    lot_name: str = ""  # The name of the parking lot this slot belongs to

@dataclass
class ParkingLevelData:
    """
    Data transfer object for parking level information.
    Represents a single level within a parking lot, containing multiple parking slots.
    """
    level: int  # The identifier for this parking level (e.g., 1, 2, G)
    slots: List[ParkingSlotData]  # A list of ParkingSlotData objects representing all slots on this level
    lot_name: str = ""  # The name of the parking lot this level belongs to

@dataclass
class ParkingLotData:
    """
    Data transfer object for parking lot information.
    Represents an entire parking lot, which can have multiple levels.
    """
    name: str  # The unique name of the parking lot
    levels: List[ParkingLevelData]  # A list of ParkingLevelData objects representing all levels in this lot

@dataclass
class SearchCriteria:
    """
    Data transfer object for search criteria.
    Used to specify parameters when searching for vehicles within the parking system.
    All fields are optional; only provided fields will be used in the search.
    """
    registration_number: Optional[str] = None  # Vehicle registration number to search for
    color: Optional[str] = None  # Vehicle color to search for
    manufacturer: Optional[str] = None  # Vehicle manufacturer to search for
    model: Optional[str] = None  # Vehicle model to search for
    is_electric: Optional[bool] = None  # Whether to search for electric vehicles
    is_motorcycle: Optional[bool] = None # Whether to search for motorcycles
    vehicle_type: Optional[VehicleType] = None  # Specific vehicle type to search for

@dataclass
class SearchResult:
    """
    Data transfer object for search results.
    Represents a single vehicle found that matches the search criteria,
    including its location within the parking system.
    """
    lot_name: str  # Name of the parking lot where the vehicle is found
    level: int  # Level number where the vehicle is parked
    slot: int  # Slot number where the vehicle is parked
    vehicle: VehicleData  # Detailed information about the found vehicle
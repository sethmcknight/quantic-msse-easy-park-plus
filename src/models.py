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
    registration_number: str
    manufacturer: str
    model: str
    color: str
    is_electric: bool
    is_motorcycle: bool
    vehicle_type: VehicleType

@dataclass
class ParkingSlotData:
    """Data transfer object for parking slot information"""
    slot_number: int
    is_occupied: bool
    vehicle: Optional[VehicleData] = None
    slot_type: SlotType = SlotType.REGULAR
    level: int = 0
    lot_name: str = ""

@dataclass
class ParkingLevelData:
    """Data transfer object for parking level information"""
    level: int
    slots: List[ParkingSlotData]
    lot_name: str = ""

@dataclass
class ParkingLotData:
    """Data transfer object for parking lot information"""
    name: str
    levels: List[ParkingLevelData]

@dataclass
class SearchCriteria:
    """Data transfer object for search criteria"""
    registration_number: Optional[str] = None
    color: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    is_electric: Optional[bool] = None
    is_motorcycle: Optional[bool] = None
    vehicle_type: Optional[VehicleType] = None

@dataclass
class SearchResult:
    """Data transfer object for search results"""
    lot_name: str
    level: int
    slot: int
    vehicle: VehicleData
"""
Models Module

This module contains data classes used throughout the parking lot system.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class VehicleData:
    """Data class for vehicle information in the UI"""
    registration_number: str  # Replaced registration with registration_number
    manufacturer: str  # Updated from make
    model: str
    color: str
    is_electric: bool
    is_motorcycle: bool

@dataclass
class SearchCriteria:
    """Data class for search criteria"""
    registration: Optional[str] = None
    color: Optional[str] = None
    manufacturer: Optional[str] = None  # Updated from make
    model: Optional[str] = None
    search_type: str = "registration"

@dataclass
class ParkingLotData:
    """Data class for parking lot information"""
    name: str
    level: int
    regular_slots: int
    electric_vehicle_slots: int
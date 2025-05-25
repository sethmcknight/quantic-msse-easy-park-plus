"""
Models Module

This module contains data classes used throughout the parking lot system.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class VehicleData:
    """Data class for vehicle information in the UI"""
    registration: str
    make: str
    model: str
    color: str
    is_electric: bool
    is_motorcycle: bool

@dataclass
class SearchCriteria:
    """Data class for search criteria"""
    registration: Optional[str] = None
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    search_type: str = "registration"

@dataclass
class ParkingLotData:
    """Data class for parking lot information"""
    name: str
    level: int
    regular_slots: int
    ev_slots: int 
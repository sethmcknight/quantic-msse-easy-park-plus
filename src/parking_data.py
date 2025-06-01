"""
Data classes for parking management system.

This module contains data transfer objects (DTOs) used throughout the parking
management system for transferring data between components and representing
the state of various parking-related entities.
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class VehicleInfo:
    """
    Information about a parked vehicle.
    
    This dataclass represents complete information about a vehicle
    that is currently parked in the parking lot, including its
    location and identification details.
    """
    slot: int  # The slot number where the vehicle is parked
    floor: int  # The floor/level number where the vehicle is located
    reg_no: str  # The vehicle's registration number/license plate
    color: str  # The color of the vehicle
    make: str  # The vehicle's manufacturer/brand
    model: str  # The vehicle's model name

@dataclass
class EVChargeInfo:
    """
    Electric vehicle charging information.
    
    This dataclass represents information about an electric vehicle
    that is currently charging at a charging station.
    """
    slot: int  # The charging slot number where the vehicle is connected
    floor: int  # The floor/level number where the charging station is located
    reg_no: str  # The vehicle's registration number/license plate
    charge: str  # The current charge level or charging status as a string

@dataclass
class ParkingStatus:
    """
    Overall parking status container.
    
    This dataclass aggregates information about both regular and
    electric vehicles currently parked in the parking lot.
    """
    regular_vehicles: List[VehicleInfo]  # List of information about regular vehicles
    ev_vehicles: List[VehicleInfo]  # List of information about electric vehicles

@dataclass
class ChargeStatus:
    """
    Electric vehicle charging status container.
    
    This dataclass contains information about all electric vehicles
    that are currently charging in the parking lot.
    """
    vehicles: List[EVChargeInfo]  # List of electric vehicle charging information

@dataclass
class SearchResult:
    """
    Search operation result container.
    
    This dataclass represents the result of a search operation
    within the parking management system.
    """
    result_type: str  # Type of search result ('slot' or 'registration')
    items: List[str]  # List of items found in the search
    is_ev: bool  # Boolean indicating if the search relates to electric vehicles
    error: Optional[str] = None  # Optional error message if the search failed

@dataclass
class ParkingResult:
    """
    Parking operation result container.
    
    This dataclass represents the result of a parking operation
    such as parking or removing a vehicle.
    """
    success: bool  # Boolean indicating if the operation was successful
    slot_number: Optional[int] = None  # Optional slot number assigned (for parking operations)
    message: str = ""  # Descriptive message about the operation result

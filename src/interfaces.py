"""
Interfaces Module

This module contains the protocol definitions for the parking lot system.
"""

from typing import List, Dict, Optional, Any, Protocol
from models import VehicleData, SearchCriteria, ParkingLotData
from Vehicle import Vehicle

class ParkingLotInterface(Protocol):
    """Protocol defining the interface for parking lot operations"""
    def park_vehicle(self, vehicle_data: VehicleData) -> Optional[int]:
        """Park a vehicle and return the slot number"""
        ...

    def remove_vehicle(self, registration: str) -> bool:
        """Remove a vehicle by registration number"""
        ...

    def search_vehicles(self, criteria: SearchCriteria) -> List[Dict[str, Any]]:
        """Search for vehicles based on criteria"""
        ...

    def create_parking_lot(self, data: ParkingLotData) -> bool:
        """Create a new parking lot"""
        ...

    def register_observer(self, observer: 'ParkingLotObserver') -> None:
        """Register an observer for parking lot updates"""
        ...

    def get_lot_names(self) -> List[str]:
        """Get all parking lot names"""
        ...

    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get levels for a lot"""
        ...

    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific lot and level"""
        ...

    def get_slot_by_registration(self, reg: str) -> Optional[int]:
        """Get slot number by registration number"""
        ...

    def get_vehicle(self, slot_number: int) -> Optional[Vehicle]:
        """Get vehicle by slot number"""
        ...

    def get_status(self) -> str:
        """Get parking lot status"""
        ...

    def park(self, reg: str, manufacturer: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle"""
        ...

    def leave(self, slot_number: int) -> bool:
        """Remove a vehicle from a slot"""
        ...

    def get_slots_by_color(self, color: str) -> List[int]:
        """Get slot numbers by vehicle color"""
        ...

    def get_slots_by_manufacturer(self, manufacturer: str) -> List[int]:
        """Get slot numbers by vehicle manufacturer"""
        ...

    def get_slots_by_model(self, model: str) -> List[int]:
        """Get slot numbers by vehicle model"""
        ...

class ParkingLotObserver(Protocol):
    """Protocol for parking lot observers"""
    def update(self, message: str) -> None:
        """Update the observer with a message"""
        ...

class Command(Protocol):
    """Protocol for command objects"""
    def execute(self) -> bool:
        """Execute the command"""
        ...

    def undo(self) -> bool:
        """Undo the command"""
        ...
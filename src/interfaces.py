"""
Interfaces for the parking system.

This module defines the interfaces used throughout the parking system.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Protocol
from models import VehicleData, SearchCriteria, ParkingLotData, ParkingStatus
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
    """Observer interface for parking lot updates"""
    
    def update(self, message: str) -> None:
        """Handle updates from the parking lot
        
        Args:
            message: The update message
        """
        ...

class Command(Protocol):
    """Protocol for command objects"""
    def execute(self) -> bool:
        """Execute the command"""
        ...

    def undo(self) -> bool:
        """Undo the command"""
        ...

class ParkingLotManager(ABC):
    """Interface for parking lot management"""
    
    @abstractmethod
    def create_lot(self, lot_data: ParkingLotData) -> bool:
        """Create a new parking lot
        
        Args:
            lot_data: The parking lot data
            
        Returns:
            bool: True if the lot was created successfully
        """
        ...
    
    @abstractmethod
    def park_vehicle(self, lot_name: str, level: int, vehicle: VehicleData) -> Optional[int]:
        """Park a vehicle in the specified lot and level
        
        Args:
            lot_name: The name of the parking lot
            level: The parking level
            vehicle: The vehicle to park
            
        Returns:
            Optional[int]: The slot number if successful, None otherwise
        """
        ...
    
    @abstractmethod
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[VehicleData]:
        """Remove a vehicle from the specified lot, level, and slot
        
        Args:
            lot_name: The name of the parking lot
            level: The parking level
            slot: The parking slot
            
        Returns:
            Optional[VehicleData]: The removed vehicle if successful, None otherwise
        """
        ...
    
    @abstractmethod
    def search_vehicles(self, lot_name: str, criteria: SearchCriteria) -> List[ParkingStatus]:
        """Search for vehicles matching the criteria
        
        Args:
            lot_name: The name of the parking lot
            criteria: The search criteria
            
        Returns:
            List[ParkingStatus]: List of matching vehicles and their status
        """
        ...
    
    @abstractmethod
    def get_lot_status(self, lot_name: str) -> List[ParkingStatus]:
        """Get the status of all slots in a lot
        
        Args:
            lot_name: The name of the parking lot
            
        Returns:
            List[ParkingStatus]: List of all slots and their status
        """
        ...
    
    @abstractmethod
    def get_lot_names(self) -> List[str]:
        """Get the names of all parking lots
        
        Returns:
            List[str]: List of parking lot names
        """
        ...
    
    @abstractmethod
    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get the levels in a parking lot
        
        Args:
            lot_name: The name of the parking lot
            
        Returns:
            List[int]: List of level numbers
        """
        ...
    
    @abstractmethod
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer for parking lot updates
        
        Args:
            observer: The observer to register
        """
        ...
    
    @abstractmethod
    def unregister_observer(self, observer: ParkingLotObserver) -> None:
        """Unregister an observer
        
        Args:
            observer: The observer to unregister
        """
        ...
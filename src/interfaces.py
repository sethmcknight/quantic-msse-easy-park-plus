"""
Interfaces Module

This module defines the interfaces used in the parking system.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from models import (
    VehicleData,
    ParkingLotData,
    ParkingLevelData,
    SearchCriteria,
    SearchResult
)
from Vehicle import Vehicle

class ParkingSystemError(Exception):
    """Base exception for all parking system errors"""
    pass

class ParkingLotError(ParkingSystemError):
    """Base exception for parking lot operations"""
    pass

class ValidationError(ParkingSystemError):
    """Exception for validation errors"""
    pass

class OperationError(ParkingSystemError):
    """Exception for operation errors"""
    pass

class ParkingLotObserver(ABC):
    """Interface for parking lot observers"""
    
    @abstractmethod
    def update(self, message: str) -> None:
        """Update the observer with a message
        
        Args:
            message: The message to send to the observer
        """
        pass

class ParkingLotInterface(ABC):
    """Interface for parking lot operations"""
    
    @abstractmethod
    def park_vehicle(self, level: int, vehicle: Vehicle) -> Optional[int]:
        """Park a vehicle in the lot
        
        Args:
            level: The level to park in
            vehicle: The vehicle to park
            
        Returns:
            The slot number where the vehicle was parked, or None if parking failed
        """
        pass
    
    @abstractmethod
    def remove_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Remove a vehicle from the lot
        
        Args:
            level: The level to remove from
            slot: The slot to remove from
            
        Returns:
            The removed vehicle, or None if no vehicle was found
        """
        pass
    
    @abstractmethod
    def get_status(self) -> List[ParkingLevelData]:
        """Get the status of all levels in the lot
        
        Returns:
            List of level data
        """
        pass
    
    @abstractmethod
    def get_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Get a vehicle from the lot
        
        Args:
            level: The level to get from
            slot: The slot to get from
            
        Returns:
            The vehicle in the slot, or None if no vehicle is present
        """
        pass

    @abstractmethod
    def get_vehicles_in_lot(self, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific level
        
        Args:
            level: The level to get vehicles from
            
        Returns:
            Dictionary mapping slot numbers to vehicles
        """
        pass

class ParkingLotManager(ABC):
    """Interface for parking lot management"""
    
    @abstractmethod
    def create_lot(self, data: ParkingLotData) -> bool:
        """Create a new parking lot
        
        Args:
            data: The parking lot data
            
        Returns:
            True if the lot was created successfully
        """
        pass
    
    @abstractmethod
    def park_vehicle(self, lot_name: str, level: int, data: VehicleData) -> Optional[int]:
        """Park a vehicle in a lot
        
        Args:
            lot_name: The name of the lot
            level: The level to park in
            data: The vehicle data
            
        Returns:
            The slot number where the vehicle was parked, or None if parking failed
        """
        pass
    
    @abstractmethod
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[Vehicle]:
        """Remove a vehicle from a lot
        
        Args:
            lot_name: The name of the lot
            level: The level to remove from
            slot: The slot to remove from
            
        Returns:
            The removed vehicle, or None if no vehicle was found
        """
        pass
    
    @abstractmethod
    def search_vehicles(self, lot_name: str, criteria: SearchCriteria) -> List[SearchResult]:
        """Search for vehicles matching criteria in a specific lot
        
        Args:
            lot_name: The name of the lot to search in
            criteria: The search criteria
            
        Returns:
            List of search results
        """
        pass
    
    @abstractmethod
    def get_lot_status(self, lot_name: str) -> List[ParkingLevelData]:
        """Get the status of a lot
        
        Args:
            lot_name: The name of the lot
            
        Returns:
            List of level data
        """
        pass
    
    @abstractmethod
    def get_lot_names(self) -> List[str]:
        """Get the names of all lots
        
        Returns:
            List of lot names
        """
        pass
    
    @abstractmethod
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer
        
        Args:
            observer: The observer to register
        """
        pass
    
    @abstractmethod
    def remove_observer(self, observer: ParkingLotObserver) -> None:
        """Remove an observer
        
        Args:
            observer: The observer to remove
        """
        pass

    @abstractmethod
    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific lot and level
        
        Args:
            lot_name: The name of the lot
            level: The level to get vehicles from
            
        Returns:
            Dictionary mapping slot numbers to vehicles
        """
        pass
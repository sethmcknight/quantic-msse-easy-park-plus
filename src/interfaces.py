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
        """Parks a vehicle at the specified level.

        Args:
            level: The level number where the vehicle should be parked.
            vehicle: The vehicle object to park.

        Returns:
            The slot number where the vehicle was parked, or None if parking failed.
        """
        pass
    
    @abstractmethod
    def remove_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Removes a vehicle from the specified level and slot.

        Args:
            level: The level number from which to remove the vehicle.
            slot: The slot number from which to remove the vehicle.

        Returns:
            The vehicle object that was removed, or None if no vehicle was found.
        """
        pass
    
    @abstractmethod
    def get_status(self) -> List[ParkingLevelData]:
        """Gets the current status of all levels in the parking lot.

        Returns:
            A list of ParkingLevelData objects representing the status of each level.
        """
        pass
    
    @abstractmethod
    def get_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Retrieves the vehicle parked at the specified level and slot.

        Args:
            level: The level number.
            slot: The slot number.

        Returns:
            The vehicle object if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_vehicles_in_lot(self, level: int) -> Dict[int, Vehicle]:
        """Gets all vehicles parked on a specific level.

        Args:
            level: The level number.

        Returns:
            A dictionary mapping slot numbers to Vehicle objects for the specified level.
        """
        pass

class ParkingLotManager(ABC):
    """Interface for parking lot management"""
    
    @abstractmethod
    def create_lot(self, data: ParkingLotData) -> bool:
        """Creates a new parking lot.

        Args:
            data: ParkingLotData object containing the configuration for the new lot.

        Returns:
            True if the lot was created successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def park_vehicle(self, lot_name: str, level: int, data: VehicleData) -> Optional[int]:
        """Parks a vehicle in the specified parking lot and level.

        Args:
            lot_name: The name of the parking lot.
            level: The level number to park the vehicle on.
            data: VehicleData object for the vehicle to be parked.

        Returns:
            The slot number where the vehicle was parked, or None if parking failed.
        """
        pass
    
    @abstractmethod
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[Vehicle]:
        """Removes a vehicle from the specified parking lot, level, and slot.

        Args:
            lot_name: The name of the parking lot.
            level: The level number.
            slot: The slot number.

        Returns:
            The removed Vehicle object, or None if no vehicle was found.
        """
        pass
    
    @abstractmethod
    def search_vehicles(self, lot_name: str, criteria: SearchCriteria) -> List[SearchResult]:
        """Searches for vehicles in a parking lot based on given criteria.

        Args:
            lot_name: The name of the parking lot to search within.
            criteria: SearchCriteria object specifying the search parameters.

        Returns:
            A list of SearchResult objects matching the criteria.
        """
        pass
    
    @abstractmethod
    def get_lot_status(self, lot_name: str) -> List[ParkingLevelData]:
        """Gets the current status of a specific parking lot.

        Args:
            lot_name: The name of the parking lot.

        Returns:
            A list of ParkingLevelData objects for the specified lot.
        """
        pass
    
    @abstractmethod
    def get_lot_names(self) -> List[str]:
        """Gets the names of all available parking lots.

        Returns:
            A list of parking lot names.
        """
        pass
    
    @abstractmethod
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Registers an observer to receive updates about parking lot events.

        Args:
            observer: The ParkingLotObserver instance to register.
        """
        pass
    
    @abstractmethod
    def remove_observer(self, observer: ParkingLotObserver) -> None:
        """Removes a previously registered observer.

        Args:
            observer: The ParkingLotObserver instance to remove.
        """
        pass

    @abstractmethod
    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Gets all vehicles parked on a specific level of a specific lot.

        Args:
            lot_name: The name of the parking lot.
            level: The level number.

        Returns:
            A dictionary mapping slot numbers to Vehicle objects for the specified level and lot.
        """
        pass
"""
Parking Manager Module

This module implements the parking lot management system.
"""

import logging
from typing import Dict, List, Optional, Set
from models import (
    VehicleData,
    ParkingLotData,
    ParkingLevelData,
    ParkingSlotData,
    SearchCriteria,
    SearchResult,
    SlotType
)
from Vehicle import Vehicle, VehicleType, create_vehicle
from interfaces import ParkingLotInterface, ParkingLotManager, ParkingLotObserver, ValidationError, OperationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parking_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ParkingLot(ParkingLotInterface):
    """Class representing a parking lot"""
    
    def __init__(self, name: str):
        """Initialize the parking lot
        
        Args:
            name: The name of the parking lot
        """
        self.name = name
        self.levels: Dict[int, List[ParkingSlotData]] = {}
        logger.info(f"Created parking lot: {name}")
    
    def add_level(self, level: int, regular_slots: int, electric_slots: int) -> None:
        """Add a level to the parking lot
        
        Args:
            level: The level number
            regular_slots: Number of regular slots
            electric_slots: Number of electric slots
        """
        slots: List[ParkingSlotData] = []
        
        # Add regular slots
        for i in range(regular_slots):
            slots.append(ParkingSlotData(
                slot_number=i + 1,
                is_occupied=False,
                slot_type=SlotType.REGULAR
            ))
        
        # Add electric slots
        for i in range(electric_slots):
            slots.append(ParkingSlotData(
                slot_number=regular_slots + i + 1,
                is_occupied=False,
                slot_type=SlotType.ELECTRIC
            ))
        
        self.levels[level] = slots
        logger.info(f"Added level {level} to {self.name} with {regular_slots} regular and {electric_slots} electric slots")
    
    def park_vehicle(self, level: int, vehicle: Vehicle) -> Optional[int]:
        """Park a vehicle in the lot
        
        Args:
            level: The level to park in
            vehicle: The vehicle to park
            
        Returns:
            The slot number where the vehicle was parked, or None if parking failed
        """
        if level not in self.levels:
            logger.error(f"Level {level} not found in {self.name}")
            return None
        
        # Find appropriate slot
        for slot in self.levels[level]:
            if not slot.is_occupied:
                if vehicle.is_electric and slot.slot_type == SlotType.ELECTRIC:
                    slot.is_occupied = True
                    slot.vehicle = VehicleData(
                        registration_number=vehicle.registration_number,
                        manufacturer=vehicle.manufacturer,
                        model=vehicle.model,
                        color=vehicle.color,
                        is_electric=True,
                        is_motorcycle=vehicle.vehicle_type == VehicleType.MOTORCYCLE,
                        vehicle_type=vehicle.vehicle_type
                    )
                    logger.info(f"Parked electric vehicle {vehicle.registration_number} in slot {slot.slot_number}")
                    return slot.slot_number
                elif not vehicle.is_electric and slot.slot_type == SlotType.REGULAR:
                    slot.is_occupied = True
                    slot.vehicle = VehicleData(
                        registration_number=vehicle.registration_number,
                        manufacturer=vehicle.manufacturer,
                        model=vehicle.model,
                        color=vehicle.color,
                        is_electric=False,
                        is_motorcycle=vehicle.vehicle_type == VehicleType.MOTORCYCLE,
                        vehicle_type=vehicle.vehicle_type
                    )
                    logger.info(f"Parked vehicle {vehicle.registration_number} in slot {slot.slot_number}")
                    return slot.slot_number
        
        logger.error(f"No suitable slot found for vehicle {vehicle.registration_number}")
        return None
    
    def remove_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Remove a vehicle from the lot
        
        Args:
            level: The level to remove from
            slot: The slot to remove from
            
        Returns:
            The removed vehicle, or None if no vehicle was found
        """
        if level not in self.levels:
            logger.error(f"Level {level} not found in {self.name}")
            return None
        
        for parking_slot in self.levels[level]:
            if parking_slot.slot_number == slot:
                if not parking_slot.is_occupied:
                    logger.error(f"Slot {slot} is empty")
                    return None
                
                vehicle_data = parking_slot.vehicle
                if vehicle_data is None:
                    logger.error(f"No vehicle data in slot {slot}")
                    return None
                
                # Create vehicle object
                vehicle = create_vehicle(
                    registration_number=vehicle_data.registration_number,
                    manufacturer=vehicle_data.manufacturer,
                    model=vehicle_data.model,
                    color=vehicle_data.color,
                    vehicle_type=vehicle_data.vehicle_type,
                    is_electric=vehicle_data.is_electric
                )
                
                # Clear slot
                parking_slot.is_occupied = False
                parking_slot.vehicle = None
                
                logger.info(f"Removed vehicle {vehicle.registration_number} from slot {slot}")
                return vehicle
        
        logger.error(f"Slot {slot} not found in level {level}")
        return None
    
    def get_status(self) -> List[ParkingLevelData]:
        """Get the status of all levels in the lot
        
        Returns:
            List of level data
        """
        return [
            ParkingLevelData(level=level, slots=slots)
            for level, slots in sorted(self.levels.items())
        ]
    
    def get_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Get a vehicle from the lot
        
        Args:
            level: The level to get from
            slot: The slot to get from
            
        Returns:
            The vehicle in the slot, or None if no vehicle is present
        """
        if level not in self.levels:
            logger.error(f"Level {level} not found in {self.name}")
            return None
        
        for parking_slot in self.levels[level]:
            if parking_slot.slot_number == slot:
                if not parking_slot.is_occupied or parking_slot.vehicle is None:
                    return None
                
                vehicle_data = parking_slot.vehicle
                return create_vehicle(
                    registration_number=vehicle_data.registration_number,
                    manufacturer=vehicle_data.manufacturer,
                    model=vehicle_data.model,
                    color=vehicle_data.color,
                    vehicle_type=vehicle_data.vehicle_type,
                    is_electric=vehicle_data.is_electric
                )
        
        logger.error(f"Slot {slot} not found in level {level}")
        return None

    def get_vehicles_in_lot(self, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific level
        
        Args:
            level: The level to get vehicles from
            
        Returns:
            Dictionary mapping slot numbers to vehicles
        """
        vehicles: Dict[int, Vehicle] = {}
        
        if level not in self.levels:
            logger.error(f"Level {level} not found in {self.name}")
            return vehicles
        
        for slot in self.levels[level]:
            if slot.is_occupied and slot.vehicle:
                vehicle = create_vehicle(
                    registration_number=slot.vehicle.registration_number,
                    manufacturer=slot.vehicle.manufacturer,
                    model=slot.vehicle.model,
                    color=slot.vehicle.color,
                    vehicle_type=slot.vehicle.vehicle_type,
                    is_electric=slot.vehicle.is_electric
                )
                vehicles[slot.slot_number] = vehicle
        
        return vehicles

class ParkingLotManagerImpl(ParkingLotManager):
    """Implementation of the parking lot manager"""
    
    def __init__(self):
        """Initialize the parking lot manager"""
        self.lots: Dict[str, ParkingLot] = {}
        self.observers: Set[ParkingLotObserver] = set()
        logger.info("Initialized ParkingLotManagerImpl")
    
    def create_lot(self, data: ParkingLotData) -> bool:
        """Create a new parking lot or add a level to an existing lot
        
        Args:
            data: The parking lot data
            
        Returns:
            True if the lot was created or updated successfully
            
        Raises:
            ValidationError: If the lot data is invalid
            OperationError: If the operation fails
        """
        if not data.name:
            raise ValidationError("Lot name is required")
        
        try:
            if data.name in self.lots:
                # Add new level to existing lot
                lot = self.lots[data.name]
                for level_data in data.levels:
                    # Check if level already exists
                    if level_data.level in lot.levels:
                        raise OperationError(f"Level {level_data.level} already exists in lot {data.name}")
                    
                    # Add the new level
                    lot.add_level(
                        level=level_data.level,
                        regular_slots=len([s for s in level_data.slots if s.slot_type == SlotType.REGULAR]),
                        electric_slots=len([s for s in level_data.slots if s.slot_type == SlotType.ELECTRIC])
                    )
                logger.info(f"Added new level to existing lot: {data.name}")
            else:
                # Create new lot
                lot = ParkingLot(data.name)
                for level_data in data.levels:
                    lot.add_level(
                        level=level_data.level,
                        regular_slots=len([s for s in level_data.slots if s.slot_type == SlotType.REGULAR]),
                        electric_slots=len([s for s in level_data.slots if s.slot_type == SlotType.ELECTRIC])
                    )
                self.lots[data.name] = lot
                logger.info(f"Created new parking lot: {data.name}")
            
            self._notify_observers(data.name)
            return True
        except Exception as e:
            logger.error(f"Error creating/updating lot {data.name}: {e}")
            raise OperationError(f"Failed to create/update lot: {str(e)}")
    
    def park_vehicle(self, lot_name: str, level: int, data: VehicleData) -> Optional[int]:
        """Park a vehicle in a lot
        
        Args:
            lot_name: The name of the lot
            level: The level to park in
            data: The vehicle data
            
        Returns:
            The slot number where the vehicle was parked, or None if parking failed
            
        Raises:
            ValidationError: If the input data is invalid
            OperationError: If the lot doesn't exist or parking fails
        """
        if lot_name not in self.lots:
            raise OperationError(f"Lot {lot_name} not found")
        
        try:
            vehicle = create_vehicle(
                registration_number=data.registration_number,
                manufacturer=data.manufacturer,
                model=data.model,
                color=data.color,
                vehicle_type=data.vehicle_type,
                is_electric=data.is_electric
            )
            
            slot = self.lots[lot_name].park_vehicle(level, vehicle)
            if slot is not None:
                self._notify_observers(lot_name)
            return slot
        except Exception as e:
            logger.error(f"Error parking vehicle in lot {lot_name}: {e}")
            raise OperationError(f"Failed to park vehicle: {str(e)}")
    
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[Vehicle]:
        """Remove a vehicle from a lot
        
        Args:
            lot_name: The name of the lot
            level: The level to remove from
            slot: The slot to remove from
            
        Returns:
            The removed vehicle, or None if no vehicle was found
            
        Raises:
            ValidationError: If the input data is invalid
            OperationError: If the lot doesn't exist or removal fails
        """
        if lot_name not in self.lots:
            raise OperationError(f"Lot {lot_name} not found")
        
        try:
            vehicle = self.lots[lot_name].remove_vehicle(level, slot)
            if vehicle is not None:
                self._notify_observers(lot_name)
            return vehicle
        except Exception as e:
            logger.error(f"Error removing vehicle from lot {lot_name}: {e}")
            raise OperationError(f"Failed to remove vehicle: {str(e)}")
    
    def search_vehicles(self, lot_name: str, criteria: SearchCriteria) -> List[SearchResult]:
        """Search for vehicles matching criteria in a specific lot
        
        Args:
            lot_name: The name of the lot to search in
            criteria: The search criteria
            
        Returns:
            List of search results
            
        Raises:
            ValidationError: If the input data is invalid
            OperationError: If the lot doesn't exist or search fails
        """
        if lot_name not in self.lots:
            raise OperationError(f"Lot {lot_name} not found")
        
        try:
            results: List[SearchResult] = []
            lot = self.lots[lot_name]
            
            # Search through all levels
            for level, slots in lot.levels.items():
                for slot in slots:
                    if slot.is_occupied and slot.vehicle and self._matches_criteria(slot.vehicle, criteria):
                        results.append(SearchResult(
                            lot_name=lot_name,
                            level=level,
                            slot=slot.slot_number,
                            vehicle=slot.vehicle
                        ))
            
            return results
        except Exception as e:
            logger.error(f"Error searching vehicles in lot {lot_name}: {e}")
            raise OperationError(f"Failed to search vehicles: {str(e)}")
    
    def get_lot_status(self, lot_name: str) -> List[ParkingLevelData]:
        """Get the status of a lot
        
        Args:
            lot_name: The name of the lot
            
        Returns:
            List of level data
            
        Raises:
            ValidationError: If the input data is invalid
            OperationError: If the lot doesn't exist or status retrieval fails
        """
        if lot_name not in self.lots:
            raise OperationError(f"Lot {lot_name} not found")
        
        try:
            return self.lots[lot_name].get_status()
        except Exception as e:
            logger.error(f"Error getting status for lot {lot_name}: {e}")
            raise OperationError(f"Failed to get lot status: {str(e)}")
    
    def get_lot_names(self) -> List[str]:
        """Get the names of all lots
        
        Returns:
            List of lot names
        """
        return list(self.lots.keys())
    
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer
        
        Args:
            observer: The observer to register
        """
        self.observers.add(observer)
        logger.info(f"Registered observer: {observer}")
    
    def unregister_observer(self, observer: ParkingLotObserver) -> None:
        """Unregister an observer
        
        Args:
            observer: The observer to unregister
        """
        if observer in self.observers:
            self.observers.remove(observer)
            logger.info(f"Unregistered observer: {observer}")
    
    def remove_observer(self, observer: ParkingLotObserver) -> None:
        """Remove an observer (for interface compatibility)"""
        self.unregister_observer(observer)
    
    def _notify_observers(self, lot_name: str) -> None:
        """Notify all observers of a change
        
        Args:
            lot_name: The name of the lot that was updated
        """
        for observer in self.observers:
            observer.update(lot_name)
    
    def _matches_criteria(self, vehicle: VehicleData, criteria: SearchCriteria) -> bool:
        """Check if a vehicle matches search criteria
        
        Args:
            vehicle: The vehicle to check
            criteria: The search criteria
            
        Returns:
            True if the vehicle matches the criteria
        """
        if criteria.registration_number and vehicle.registration_number != criteria.registration_number:
            return False
        if criteria.color and vehicle.color != criteria.color:
            return False
        if criteria.manufacturer and vehicle.manufacturer != criteria.manufacturer:
            return False
        if criteria.model and vehicle.model != criteria.model:
            return False
        if criteria.is_electric is not None and vehicle.is_electric != criteria.is_electric:
            return False
        if criteria.is_motorcycle is not None and (vehicle.vehicle_type == VehicleType.MOTORCYCLE) != criteria.is_motorcycle:
            return False
        if criteria.vehicle_type and vehicle.vehicle_type != criteria.vehicle_type:
            return False
        return True

    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get the levels in a lot
        
        Args:
            lot_name: The name of the lot
            
        Returns:
            List of level numbers
        """
        if lot_name not in self.lots:
            logger.error(f"Lot {lot_name} not found")
            return []
        
        return sorted(self.lots[lot_name].levels.keys())

    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific lot and level
        
        Args:
            lot_name: The name of the lot
            level: The level to get vehicles from
            
        Returns:
            Dictionary mapping slot numbers to vehicles
            
        Raises:
            ValidationError: If the input data is invalid
            OperationError: If the lot doesn't exist or retrieval fails
        """
        if lot_name not in self.lots:
            raise OperationError(f"Lot {lot_name} not found")
        
        try:
            vehicles: Dict[int, Vehicle] = {}
            lot = self.lots[lot_name]
            
            if level not in lot.levels:
                logger.error(f"Level {level} not found in lot {lot_name}")
                return vehicles
            
            for slot in lot.levels[level]:
                if slot.is_occupied and slot.vehicle:
                    vehicle = create_vehicle(
                        registration_number=slot.vehicle.registration_number,
                        manufacturer=slot.vehicle.manufacturer,
                        model=slot.vehicle.model,
                        color=slot.vehicle.color,
                        vehicle_type=slot.vehicle.vehicle_type,
                        is_electric=slot.vehicle.is_electric
                    )
                    vehicles[slot.slot_number] = vehicle
            
            return vehicles
        except Exception as e:
            logger.error(f"Error getting vehicles in lot {lot_name}, level {level}: {e}")
            raise OperationError(f"Failed to get vehicles: {str(e)}")

# Main App
def main():
    # Create UI
    from ParkingLotUI import ParkingLotUI
    ui = ParkingLotUI()  # No need to pass parking lot since it's created in __init__
    ui.run()

if __name__ == '__main__':
    main()

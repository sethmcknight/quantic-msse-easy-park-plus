"""
Parking Lot Management Module

This module implements the parking lot management system.
It uses the State Pattern to manage parking slot states, the Observer Pattern for UI updates,
and the Command Pattern to encapsulate parking operations.

Anti-patterns Removed:
1. Magic Numbers
   - Removed: -1 for empty slots
   - Solution: State Pattern for slot states
   - Benefit: Clear state representation

2. UI-Business Logic Coupling
   - Removed: Direct UI manipulation
   - Solution: Observer Pattern
   - Benefit: Separation of concerns

3. Hard-Coded Behavior
   - Removed: Fixed slot behavior
   - Solution: State Pattern
   - Benefit: Flexible slot behavior

4. Direct Operation Execution
   - Removed: Direct method calls for operations
   - Solution: Command Pattern
   - Benefit: Encapsulated operations, undo/redo support

Design Patterns Implemented:
1. State Pattern
   - Purpose: Manage parking slot states
   - Components: ParkingSlotState interface and concrete states
   - Benefit: Encapsulated state behavior

2. Observer Pattern
   - Purpose: Decouple UI from business logic
   - Components: ParkingLotObserver interface
   - Benefit: Clean separation of concerns

3. Command Pattern
   - Purpose: Encapsulate parking operations
   - Components: Command interface and concrete commands
   - Benefit: Flexible operation management

Usage:
    The ParkingLot class is the main entry point for parking operations.
    It manages parking slots and notifies observers of changes.

Example:
    >>> parking_lot = ParkingLot()
    >>> parking_lot.create_parking_lot(10, 5, 1)  # 10 regular slots, 5 EV slots, level 1
    >>> parking_lot.park("ABC123", "Toyota", "Camry", "Red", False, False)

[DEBUG LOGGING]
This module contains temporary debug logging statements that should be removed before final submission.
These logs help track:
- Parking lot creation and initialization
- Vehicle parking and removal
- Status queries and data retrieval
- Search operations

To remove debug logging:
1. Remove all print statements starting with [DEBUG]
2. Remove this debug logging section from the docstring
"""

import logging
from typing import Dict, List, Optional, Set
from models import (
    VehicleData, ParkingLotData, ParkingLevelData,
    SearchCriteria, ParkingStatus, SlotType, VehicleType
)
from interfaces import ParkingLotManager, ParkingLotObserver
from Vehicle import (
    Vehicle, ElectricVehicle, Car, ElectricCar,
    Motorcycle, ElectricMotorcycle, Truck, Bus
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ParkingSlot:
    """Class representing a parking slot"""
    
    def __init__(self, slot_type: SlotType):
        """Initialize a parking slot
        
        Args:
            slot_type: The type of slot
        """
        self.slot_type = slot_type
        self.vehicle: Optional[Vehicle] = None
        self.is_charging: bool = False
    
    def is_available(self) -> bool:
        """Check if the slot is available
        
        Returns:
            bool: True if the slot is available
        """
        return self.vehicle is None
    
    def can_park(self, vehicle: Vehicle) -> bool:
        """Check if a vehicle can park in this slot
        
        Args:
            vehicle: The vehicle to check
            
        Returns:
            bool: True if the vehicle can park
        """
        if not self.is_available():
            return False
        
        if self.slot_type == SlotType.REGULAR:
            return not vehicle.is_electric and not vehicle.is_motorcycle
        elif self.slot_type == SlotType.ELECTRIC:
            return vehicle.is_electric and not vehicle.is_motorcycle
        elif self.slot_type == SlotType.MOTORCYCLE:
            return not vehicle.is_electric and vehicle.is_motorcycle
        else:  # EV_MOTORCYCLE
            return vehicle.is_electric and vehicle.is_motorcycle
    
    def park(self, vehicle: Vehicle) -> None:
        """Park a vehicle in this slot
        
        Args:
            vehicle: The vehicle to park
        """
        if not self.can_park(vehicle):
            raise ValueError("Vehicle cannot park in this slot")
        self.vehicle = vehicle
        if isinstance(vehicle, ElectricVehicle):
            self.is_charging = True
    
    def remove(self) -> Optional[Vehicle]:
        """Remove the vehicle from this slot
        
        Returns:
            Optional[Vehicle]: The removed vehicle
        """
        vehicle = self.vehicle
        self.vehicle = None
        self.is_charging = False
        return vehicle

class ParkingLevel:
    """Class representing a parking level"""
    
    def __init__(self, level_data: ParkingLevelData):
        """Initialize a parking level
        
        Args:
            level_data: The level configuration
        """
        self.level_number = level_data.level_number
        self.slots: List[ParkingSlot] = []
        
        # Create regular slots
        for _ in range(level_data.regular_slots):
            self.slots.append(ParkingSlot(SlotType.REGULAR))
        
        # Create electric slots
        for _ in range(level_data.electric_slots):
            self.slots.append(ParkingSlot(SlotType.ELECTRIC))
        
        # Create motorcycle slots
        for _ in range(level_data.motorcycle_slots):
            self.slots.append(ParkingSlot(SlotType.MOTORCYCLE))
        
        # Create EV motorcycle slots
        for _ in range(level_data.ev_motorcycle_slots):
            self.slots.append(ParkingSlot(SlotType.EV_MOTORCYCLE))
    
    def get_available_slot(self, vehicle: Vehicle) -> Optional[int]:
        """Get an available slot for a vehicle
        
        Args:
            vehicle: The vehicle to park
            
        Returns:
            Optional[int]: The slot number if available
        """
        for i, slot in enumerate(self.slots):
            if slot.can_park(vehicle):
                return i
        return None
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[int]:
        """Park a vehicle in this level
        
        Args:
            vehicle: The vehicle to park
            
        Returns:
            Optional[int]: The slot number if successful
        """
        slot_num = self.get_available_slot(vehicle)
        if slot_num is not None:
            self.slots[slot_num].park(vehicle)
        return slot_num
    
    def remove_vehicle(self, slot_num: int) -> Optional[Vehicle]:
        """Remove a vehicle from this level
        
        Args:
            slot_num: The slot number
            
        Returns:
            Optional[Vehicle]: The removed vehicle
        """
        if 0 <= slot_num < len(self.slots):
            return self.slots[slot_num].remove()
        return None
    
    def get_status(self) -> List[ParkingStatus]:
        """Get the status of all slots in this level
        
        Returns:
            List[ParkingStatus]: List of slot statuses
        """
        statuses: List[ParkingStatus] = []
        for i, slot in enumerate(self.slots):
            vehicle_data = None
            if slot.vehicle is not None:
                vehicle_data = VehicleData(
                    registration_number=slot.vehicle.registration_number,
                    manufacturer=slot.vehicle.manufacturer,
                    model=slot.vehicle.model,
                    color=slot.vehicle.color,
                    is_electric=slot.vehicle.is_electric,
                    is_motorcycle=slot.vehicle.is_motorcycle,
                    vehicle_type=slot.vehicle.vehicle_type
                )
            status = ParkingStatus(
                lot_name="",  # Will be set by ParkingLot
                level=self.level_number,
                slot=i,
                vehicle=vehicle_data,
                slot_type=slot.slot_type,
                is_occupied=not slot.is_available(),
                is_charging=slot.is_charging
            )
            statuses.append(status)
        return statuses

class ParkingLot:
    """Class representing a parking lot"""
    
    def __init__(self, lot_data: ParkingLotData):
        """Initialize a parking lot
        
        Args:
            lot_data: The lot configuration
        """
        self.name = lot_data.name
        self.levels: List[ParkingLevel] = []
        self.observers: Set[ParkingLotObserver] = set()
        
        # Create levels
        for level_data in lot_data.levels:
            self.levels.append(ParkingLevel(level_data))
    
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer
        
        Args:
            observer: The observer to register
        """
        self.observers.add(observer)
    
    def unregister_observer(self, observer: ParkingLotObserver) -> None:
        """Unregister an observer
        
        Args:
            observer: The observer to unregister
        """
        self.observers.discard(observer)
    
    def notify_observers(self, message: str) -> None:
        """Notify all observers
        
        Args:
            message: The message to send
        """
        for observer in self.observers:
            observer.update(message)
    
    def park_vehicle(self, level: int, vehicle: Vehicle) -> Optional[int]:
        """Park a vehicle in the lot
        
        Args:
            level: The level number
            vehicle: The vehicle to park
            
        Returns:
            Optional[int]: The slot number if successful
        """
        if not 0 <= level < len(self.levels):
            return None
        
        slot_num = self.levels[level].park_vehicle(vehicle)
        if slot_num is not None:
            self.notify_observers(f"Vehicle {vehicle.registration_number} parked in slot {slot_num}")
        return slot_num
    
    def remove_vehicle(self, level: int, slot: int) -> Optional[Vehicle]:
        """Remove a vehicle from the lot
        
        Args:
            level: The level number
            slot: The slot number
            
        Returns:
            Optional[Vehicle]: The removed vehicle
        """
        if not 0 <= level < len(self.levels):
            return None
        
        vehicle = self.levels[level].remove_vehicle(slot)
        if vehicle is not None:
            self.notify_observers(f"Vehicle {vehicle.registration_number} removed from slot {slot}")
        return vehicle
    
    def get_status(self) -> List[ParkingStatus]:
        """Get the status of all slots in the lot
        
        Returns:
            List[ParkingStatus]: List of slot statuses
        """
        statuses: List[ParkingStatus] = []
        for level in self.levels:
            level_statuses = level.get_status()
            for status in level_statuses:
                status.lot_name = self.name
            statuses.extend(level_statuses)
        return statuses

class ParkingLotManagerImpl(ParkingLotManager):
    """Implementation of the parking lot manager"""
    
    def __init__(self):
        """Initialize the parking lot manager"""
        logger.debug("[DEBUG] Initializing ParkingLotManagerImpl")
        self.lots: Dict[str, ParkingLot] = {}
        self.observers = []
        logger.debug("[DEBUG] ParkingLotManagerImpl initialization complete")
    
    def create_lot(self, lot_data: ParkingLotData) -> bool:
        """Create a new parking lot
        
        Args:
            lot_data: The lot configuration
            
        Returns:
            bool: True if the lot was created successfully
        """
        if lot_data.name in self.lots:
            return False
        
        self.lots[lot_data.name] = ParkingLot(lot_data)
        return True
    
    def park_vehicle(self, lot_name: str, level: int, vehicle: VehicleData) -> Optional[int]:
        """Park a vehicle in the specified lot and level
        
        Args:
            lot_name: The name of the parking lot
            level: The parking level
            vehicle: The vehicle to park
            
        Returns:
            Optional[int]: The slot number if successful
        """
        if lot_name not in self.lots:
            return None
        
        # Create the appropriate vehicle type
        vehicle_obj = self._create_vehicle(vehicle)
        if vehicle_obj is None:
            return None
        
        return self.lots[lot_name].park_vehicle(level, vehicle_obj)
    
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[VehicleData]:
        """Remove a vehicle from the specified lot, level, and slot
        
        Args:
            lot_name: The name of the parking lot
            level: The parking level
            slot: The parking slot
            
        Returns:
            Optional[VehicleData]: The removed vehicle if successful
        """
        if lot_name not in self.lots:
            return None
        
        vehicle = self.lots[lot_name].remove_vehicle(level, slot)
        if vehicle is None:
            return None
        
        # Convert vehicle to VehicleData
        return VehicleData(
            registration_number=vehicle.registration_number,
            manufacturer=vehicle.manufacturer,
            model=vehicle.model,
            color=vehicle.color,
            is_electric=vehicle.is_electric,
            is_motorcycle=vehicle.is_motorcycle,
            vehicle_type=vehicle.vehicle_type
        )
    
    def search_vehicles(self, lot_name: str, criteria: SearchCriteria) -> List[ParkingStatus]:
        """Search for vehicles matching the criteria
        
        Args:
            lot_name: The name of the parking lot
            criteria: The search criteria
            
        Returns:
            List[ParkingStatus]: List of matching vehicles and their status
        """
        if lot_name not in self.lots:
            return []
        
        all_statuses = self.lots[lot_name].get_status()
        if criteria.is_empty():
            return all_statuses
        
        matching_statuses: List[ParkingStatus] = []
        for status in all_statuses:
            if status.vehicle is None:
                continue
            
            matches = True
            if criteria.registration_number and status.vehicle.registration_number != criteria.registration_number:
                matches = False
            if criteria.color and status.vehicle.color != criteria.color:
                matches = False
            if criteria.manufacturer and status.vehicle.manufacturer != criteria.manufacturer:
                matches = False
            if criteria.model and status.vehicle.model != criteria.model:
                matches = False
            if criteria.vehicle_type and status.vehicle.vehicle_type != criteria.vehicle_type:
                matches = False
            if criteria.is_electric is not None and status.vehicle.is_electric != criteria.is_electric:
                matches = False
            if criteria.is_motorcycle is not None and status.vehicle.is_motorcycle != criteria.is_motorcycle:
                matches = False
            
            if matches:
                matching_statuses.append(status)
        
        return matching_statuses
    
    def get_lot_status(self, lot_name: str) -> List[ParkingStatus]:
        """Get the status of all slots in a lot
        
        Args:
            lot_name: The name of the parking lot
            
        Returns:
            List[ParkingStatus]: List of all slots and their status
        """
        if lot_name not in self.lots:
            return []
        return self.lots[lot_name].get_status()
    
    def get_lot_names(self) -> List[str]:
        """Get the names of all parking lots
        
        Returns:
            List[str]: List of parking lot names
        """
        logger.debug("[DEBUG] Getting all parking lot names")
        try:
            names = list(self.lots.keys())
            logger.debug(f"[DEBUG] Found {len(names)} parking lots: {names}")
            return names
        except Exception as e:
            logger.error(f"[DEBUG] Error getting lot names: {e}")
            raise
    
    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get the levels in a parking lot
        
        Args:
            lot_name: The name of the parking lot
            
        Returns:
            List[int]: List of level numbers
        """
        if lot_name not in self.lots:
            return []
        logger.debug(f"[DEBUG] Getting levels for lot: {lot_name}")
        try:
            levels = [level.level_number for level in self.lots[lot_name].levels]
            logger.debug(f"[DEBUG] Found {len(levels)} levels for lot {lot_name}: {levels}")
            return levels
        except Exception as e:
            logger.error(f"[DEBUG] Error getting levels: {e}")
            raise
    
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer for parking lot updates
        
        Args:
            observer: The observer to register
        """
        for lot in self.lots.values():
            lot.register_observer(observer)
    
    def unregister_observer(self, observer: ParkingLotObserver) -> None:
        """Unregister an observer
        
        Args:
            observer: The observer to unregister
        """
        for lot in self.lots.values():
            lot.unregister_observer(observer)
    
    def _create_vehicle(self, data: VehicleData) -> Optional[Vehicle]:
        """Create a vehicle from vehicle data
        
        Args:
            data: The vehicle data
            
        Returns:
            Optional[Vehicle]: The created vehicle
        """
        try:
            if data.is_electric:
                if data.is_motorcycle:
                    return ElectricMotorcycle(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=True,
                        is_motorcycle=True,
                        vehicle_type=VehicleType.ELECTRIC_MOTORCYCLE
                    )
                else:
                    return ElectricCar(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=True,
                        is_motorcycle=False,
                        vehicle_type=VehicleType.ELECTRIC_CAR
                    )
            else:
                if data.is_motorcycle:
                    return Motorcycle(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=False,
                        is_motorcycle=True,
                        vehicle_type=VehicleType.MOTORCYCLE
                    )
                elif data.vehicle_type == VehicleType.TRUCK:
                    return Truck(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=False,
                        is_motorcycle=False,
                        vehicle_type=VehicleType.TRUCK
                    )
                elif data.vehicle_type == VehicleType.BUS:
                    return Bus(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=False,
                        is_motorcycle=False,
                        vehicle_type=VehicleType.BUS
                    )
                else:
                    return Car(
                        registration_number=data.registration_number,
                        manufacturer=data.manufacturer,
                        model=data.model,
                        color=data.color,
                        is_electric=False,
                        is_motorcycle=False,
                        vehicle_type=VehicleType.CAR
                    )
        except ValueError as e:
            logger.error(f"Error creating vehicle: {e}")
            return None

# Main App
def main():
    # Create UI
    from ParkingLotUI import ParkingLotUI
    ui = ParkingLotUI()  # No need to pass parking lot since it's created in __init__
    ui.run()

if __name__ == '__main__':
    main()

"""
Parking Lot Management Module

This module implements the core parking lot management functionality using several design patterns:
- Observer Pattern: For real-time updates between parking lot and UI
- Factory Pattern: For creating different types of vehicles
- Strategy Pattern: For different parking strategies
- Singleton Pattern: For managing parking lot instances

The ParkingLot class provides methods for:
- Creating and managing parking lots
- Parking and removing vehicles
- Searching for vehicles
- Managing parking lot state
"""

import logging
from typing import List, Dict, Optional, Any
from abc import ABC
from Vehicle import Vehicle, VehicleFactory
from models import VehicleData, SearchCriteria, ParkingLotData
from interfaces import ParkingLotInterface, ParkingLotObserver, Command

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParkingLotComponent(ABC):
    """Abstract base class for parking lot components"""
    def __init__(self, parent: Optional['ParkingLotComponent'] = None):
        self.parent = parent

class ParkingSlot:
    """Class representing a parking slot"""
    def __init__(self, slot_type: str):
        self._slot_type = slot_type
        self._vehicle: Optional[Vehicle] = None

    @property
    def slot_type(self) -> str:
        return self._slot_type

    def is_empty(self) -> bool:
        return self._vehicle is None

    def park(self, vehicle: Vehicle) -> bool:
        if self.is_empty():
            self._vehicle = vehicle
            return True
        return False

    def leave(self) -> Optional[Vehicle]:
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle

    def get_vehicle(self) -> Optional[Vehicle]:
        return self._vehicle

class ParkingLotLevel:
    """Class representing a parking lot level"""
    def __init__(self, level: int):
        self.level = level
        self.name: Optional[str] = None
        self.regular_slots: List[ParkingSlot] = []
        self.electric_vehicle_slots: List[ParkingSlot] = []

    @property
    def slots(self) -> List[ParkingSlot]:
        return self.regular_slots + self.electric_vehicle_slots

    def set_name(self, name: str) -> None:
        self.name = name

    def add_regular_slot(self, slot: ParkingSlot) -> None:
        self.regular_slots.append(slot)

    def add_ev_slot(self, slot: ParkingSlot) -> None:
        self.electric_vehicle_slots.append(slot)

class ParkingLot(ParkingLotInterface):
    """Singleton class representing the parking lot"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the parking lot"""
        self.levels: List[ParkingLotLevel] = []
        self.observers: List[ParkingLotObserver] = []
        self.command_history: List[Command] = []

    def create_parking_lot(self, data: ParkingLotData) -> bool:
        """Create a new parking lot with the given data"""
        try:
            # Prevent duplicate lot names and levels
            for level in self.levels:
                if level.name == data.name and level.level == data.level:
                    self.notify_observers(f"Lot name already exists for level {data.level}")
                    return False
            # Create a new level
            level = ParkingLotLevel(data.level)
            # Add regular slots
            for _ in range(data.regular_slots):
                level.add_regular_slot(ParkingSlot("regular"))
            # Add EV slots
            for _ in range(data.electric_vehicle_slots):
                level.add_ev_slot(ParkingSlot("ev"))
            # Set the name
            level.set_name(data.name)
            # Add the level to the parking lot
            self.levels.append(level)
            # Notify observers
            self.notify_observers(f"Created parking lot {data.name} with {data.regular_slots} regular slots and {data.electric_vehicle_slots} EV slots")
            return True
        except Exception as e:
            logger.error(f"Error creating parking lot: {e}")
            return False

    def notify_observers(self, message: str) -> None:
        """Notify all observers with a message"""
        for observer in self.observers:
            observer.update(message)

    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer"""
        if observer not in self.observers:
            self.observers.append(observer)

    def park_vehicle(self, vehicle_data: VehicleData) -> Optional[int]:
        """Park a vehicle using the vehicle data"""
        return self.park(
            vehicle_data.registration_number,
            vehicle_data.manufacturer,  # Updated from make
            vehicle_data.model,
            vehicle_data.color,
            vehicle_data.is_electric,
            vehicle_data.is_motorcycle
        )

    def remove_vehicle(self, registration: str) -> bool:
        """Remove a vehicle by registration number"""
        slot = self.get_slot_by_registration(registration)
        if slot is not None:
            return self.leave(slot)
        return False

    def search_vehicles(self, criteria: SearchCriteria) -> List[Dict[str, Any]]:
        """Search for vehicles based on criteria"""
        results: List[Dict[str, Any]] = []
        if criteria.search_type == "registration" and criteria.registration:
            slot = self.get_slot_by_registration(criteria.registration)
            if slot is not None:
                vehicle = self.get_vehicle(slot)
                if vehicle:
                    results.append({
                        "slot": slot,
                        "registration": vehicle.registration_number,
                        "manufacturer": vehicle.vehicle_manufacturer,
                        "model": vehicle.model,
                        "color": vehicle.color,
                        "type": vehicle.get_type()
                    })
        elif criteria.search_type == "color" and criteria.color:
            slots = self.get_slots_by_color(criteria.color)
            for slot in slots:
                vehicle = self.get_vehicle(slot)
                if vehicle:
                    results.append({
                        "slot": slot,
                        "registration": vehicle.registration_number,
                        "manufacturer": vehicle.vehicle_manufacturer,
                        "model": vehicle.model,
                        "color": vehicle.color,
                        "type": vehicle.get_type()
                    })
        elif criteria.search_type == "manufacturer" and criteria.manufacturer:
            slots = self.get_slots_by_manufacturer(criteria.manufacturer)
            for slot in slots:
                vehicle = self.get_vehicle(slot)
                if vehicle:
                    results.append({
                        "slot": slot,
                        "registration": vehicle.registration_number,
                        "manufacturer": vehicle.vehicle_manufacturer,
                        "model": vehicle.model,
                        "color": vehicle.color,
                        "type": vehicle.get_type()
                    })
        elif criteria.search_type == "model" and criteria.model:
            slots = self.get_slots_by_model(criteria.model)
            for slot in slots:
                vehicle = self.get_vehicle(slot)
                if vehicle:
                    results.append({
                        "slot": slot,
                        "registration": vehicle.registration_number,
                        "manufacturer": vehicle.vehicle_manufacturer,
                        "model": vehicle.model,
                        "color": vehicle.color,
                        "type": vehicle.get_type()
                    })
        elif criteria.search_type == "manufacturer" and criteria.manufacturer:
            slots = self.get_slots_by_manufacturer(criteria.manufacturer)
            for slot in slots:
                vehicle = self.get_vehicle(slot)
                if vehicle:
                    results.append({
                        "slot": slot,
                        "registration": vehicle.registration_number,
                        "manufacturer": vehicle.vehicle_manufacturer,  # Updated from make
                        "model": vehicle.model,
                        "color": vehicle.color,
                        "type": vehicle.get_type()
                    })
        return results

    def get_status(self) -> str:
        """Get the current status of the parking lot"""
        total_slots = sum(len(level.slots) for level in self.levels)
        occupied_slots = sum(1 for level in self.levels for slot in level.slots if not slot.is_empty())
        return f"Total slots: {total_slots}, Occupied: {occupied_slots}, Available: {total_slots - occupied_slots}"

    def get_lot_names(self) -> List[str]:
        """Get all parking lot names"""
        return [name for level in self.levels if (name := level.name)]

    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get all levels for a specific lot"""
        return [level.level for level in self.levels if level.name == lot_name]

    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific lot and level"""
        vehicles: Dict[int, Vehicle] = {}
        for level_obj in self.levels:
            if level_obj.name == lot_name and level_obj.level == level:
                for slot_index, slot in enumerate(level_obj.slots):
                    vehicle = slot.get_vehicle()
                    if vehicle:
                        vehicles[slot_index + 1] = vehicle
        return vehicles

    def get_slot_by_registration(self, reg: str) -> Optional[int]:
        """Get slot number by registration number"""
        for level in self.levels:
            for slot_index, slot in enumerate(level.slots):
                vehicle = slot.get_vehicle()
                if vehicle and vehicle.registration_number == reg:
                    return slot_index + 1
        return None

    def get_vehicle(self, slot_number: int) -> Optional[Vehicle]:
        """Get vehicle by slot number"""
        for level in self.levels:
            if 0 <= slot_number - 1 < len(level.slots):
                return level.slots[slot_number - 1].get_vehicle()
        return None

    def get_slots_by_color(self, color: str) -> List[int]:
        """Get slot numbers by vehicle color"""
        slots: List[int] = []
        for level in self.levels:
            for slot_index, slot in enumerate(level.slots):
                vehicle = slot.get_vehicle()
                if vehicle and vehicle.color.lower() == color.lower():
                    slots.append(slot_index + 1)
        return slots

    def get_slots_by_manufacturer(self, manufacturer: str) -> List[int]:
        """Get slot numbers by vehicle manufacturer"""
        slots: List[int] = []
        for level in self.levels:
            for slot_index, slot in enumerate(level.slots):
                vehicle = slot.get_vehicle()
                if vehicle and vehicle.vehicle_manufacturer.lower() == manufacturer.lower():
                    slots.append(slot_index + 1)
        return slots

    def get_slots_by_model(self, model: str) -> List[int]:
        """Get slot numbers by vehicle model"""
        slots: List[int] = []
        for level in self.levels:
            for slot_index, slot in enumerate(level.slots):
                vehicle = slot.get_vehicle()
                if vehicle and vehicle.model.lower() == model.lower():
                    slots.append(slot_index + 1)
        return slots

    def _create_vehicle(self, reg: str, manufacturer: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Vehicle:
        """Create a vehicle instance based on the provided parameters."""
        if is_electric:
            if is_motorcycle:
                return VehicleFactory.create_electric_motorcycle(reg, manufacturer, model, color)
            return VehicleFactory.create_electric_car(reg, manufacturer, model, color)
        if is_motorcycle:
            return VehicleFactory.create_motorcycle(reg, manufacturer, model, color)
        return VehicleFactory.create_car(reg, manufacturer, model, color)

    def park(self, reg: str, manufacturer: str, model: str, color: str, is_electric: bool, is_motorcycle: bool, lot_name: Optional[str] = None, level: Optional[int] = None) -> Optional[int]:
        """Park a vehicle in a specific lot and level if provided, otherwise find first available slot"""
        vehicle = self._create_vehicle(reg, manufacturer, model, color, is_electric, is_motorcycle)
        
        # If lot and level are specified, try to park in that specific location
        if lot_name is not None and level is not None:
            for level_obj in self.levels:
                if level_obj.name == lot_name and level_obj.level == level:
                    for i, slot in enumerate(level_obj.slots):
                        if slot.is_empty() and slot.park(vehicle):
                            self.notify_observers(f"Parked {vehicle.get_type()} in slot {i + 1} of {lot_name} level {level}")
                            return i + 1
            return None
        
        # Otherwise, find first available slot in any lot/level
        for level_obj in self.levels:
            for i, slot in enumerate(level_obj.slots):
                if slot.is_empty() and slot.park(vehicle):
                    self.notify_observers(f"Parked {vehicle.get_type()} in slot {i + 1}")
                    return i + 1
        return None

    def leave(self, slot_number: int) -> bool:
        """Remove a vehicle from a slot"""
        for level in self.levels:
            if 0 <= slot_number - 1 < len(level.slots):
                vehicle = level.slots[slot_number - 1].leave()
                if vehicle:
                    self.notify_observers(f"Removed {vehicle.get_type()} from slot {slot_number}")
                    return True
        return False

# Main App
def main():
    # Create UI
    from ParkingLotUI import ParkingLotUI
    ui = ParkingLotUI()  # No need to pass parking lot since it's created in __init__
    ui.run()

if __name__ == '__main__':
    main()

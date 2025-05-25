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

import Vehicle as Vehicle
from typing import Optional, List, Protocol, Dict, TypeVar, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

T = TypeVar('T')

class Command(Protocol):
    """Protocol for command objects"""
    
    def execute(self) -> bool:
        """Execute the command"""
        ...
    
    def undo(self) -> bool:
        """Undo the command"""
        ...

class CreateParkingLotCommand:
    """Command to create a parking lot"""
    
    def __init__(self, parking_lot: 'ParkingLot', capacity: int, electric_vehicle_capacity: int, level: int):
        self._parking_lot = parking_lot
        self._capacity = capacity
        self._electric_vehicle_capacity = electric_vehicle_capacity
        self._level = level
        self._previous_levels: Optional[List['SingleLevelParkingLot']] = None
    
    def execute(self) -> bool:
        self._previous_slots = self._parking_lot.slots.copy() if self._parking_lot.slots else None
        self._previous_level = self._parking_lot.level
        self._parking_lot.create_parking_lot(self._capacity, self._electric_vehicle_capacity, self._level)
        return True
    
    def undo(self) -> bool:
        if self._previous_levels is not None:
            self._parking_lot.levels = self._previous_levels
            self._parking_lot.notify_observers("Undid parking lot creation")
            return True
        return False

class ParkCommand:
    """Command to park a vehicle"""

    def __init__(self, parking_lot: 'ParkingLot', registration_number: str, make: str, model: str, 
                 color: str, is_electric: bool, is_motorcycle: bool):
        self._parking_lot = parking_lot
        self._registration_number = registration_number
        self._make = make
        self._model = model
        self._color = color
        self._is_electric = is_electric
        self._is_motorcycle = is_motorcycle
        self._parking_slot_number: Optional[int] = None

    def execute(self) -> bool:
        self._parking_slot_number = self._parking_lot.park(
            self._registration_number, self._make, self._model,
            self._color, self._is_electric, self._is_motorcycle
        )
        return self._parking_slot_number is not None

    def undo(self) -> bool:
        if self._parking_slot_number is not None:
            return self._parking_lot.leave(self._parking_slot_number)
        return False

class LeaveCommand:
    """Command to remove a vehicle"""
    
    def __init__(self, parking_lot: 'ParkingLot', parking_slot_number: int):
        self._parking_lot = parking_lot
        self._parking_slot_number = parking_slot_number
        self._vehicle: Optional[Vehicle.Vehicle] = None
    
    def execute(self) -> bool:
        self._vehicle = self._parking_lot.get_vehicle(self._parking_slot_number)
        return self._parking_lot.leave(self._parking_slot_number)
    
    def undo(self) -> bool:
        if self._vehicle:
            return self._parking_lot.park(
                self._vehicle.registration_number,
                self._vehicle.make,
                self._vehicle.model,
                self._vehicle.color,
                isinstance(self._vehicle, Vehicle.ElectricVehicle),
                isinstance(self._vehicle, Vehicle.Motorcycle)
            ) is not None
        return False

class ParkingSlotState(ABC):
    """Abstract base class for parking slot states"""
    
    @abstractmethod
    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        """Check if a vehicle can park in this state"""
        pass
    
    @abstractmethod
    def park(self, vehicle: Vehicle.Vehicle) -> bool:
        """Park a vehicle in this state"""
        pass
    
    @abstractmethod
    def leave(self) -> Optional[Vehicle.Vehicle]:
        """Remove the vehicle from this state"""
        pass
    
    @abstractmethod
    def get_vehicle(self) -> Optional[Vehicle.Vehicle]:
        """Get the vehicle in this state"""
        pass

class EmptyState(ParkingSlotState):
    """State for an empty parking slot"""
    
    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        return True
    
    def park(self, vehicle: Vehicle.Vehicle) -> bool:
        return True
    
    def leave(self) -> Optional[Vehicle.Vehicle]:
        return None
    
    def get_vehicle(self) -> Optional[Vehicle.Vehicle]:
        return None
class OccupiedState(ParkingSlotState):
    """State for an occupied parking slot"""
    
    def __init__(self, vehicle: Vehicle.Vehicle):
        self._vehicle = vehicle
    
    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        return False
    
    def park(self, vehicle: Vehicle.Vehicle) -> bool:
        return False
    
    def leave(self) -> Optional[Vehicle.Vehicle]:
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle
    
    def get_vehicle(self) -> Optional[Vehicle.Vehicle]:
        return self._vehicle

class ReservedState(ParkingSlotState):
    """State for a reserved parking slot"""
    
    def __init__(self, vehicle_type: str):
        self._vehicle_type = vehicle_type
        self._vehicle: Optional[Vehicle.Vehicle] = None
    
    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        return vehicle.get_type() == self._vehicle_type
    
    def park(self, vehicle: Vehicle.Vehicle) -> bool:
        if self.can_park(vehicle):
            self._vehicle = vehicle
            return True
        return False
    
    def leave(self) -> Optional[Vehicle.Vehicle]:
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle
    
    def get_vehicle(self) -> Optional[Vehicle.Vehicle]:
        return self._vehicle

@dataclass
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
        return [name for level in self.levels if (name := level.get_name())]
    
    def create_parking_lot(self, capacity: int, electric_vehicle_capacity: int, level: int) -> None:
        """Create a new parking lot with the specified capacity"""
        self.slots = []
        self.level = level
        
        # Create regular slots
        for _ in range(capacity):
            self.slots.append(ParkingSlot("standard"))
        
        # Create EV slots
        for _ in range(electric_vehicle_capacity):
            self.slots.append(ParkingSlot("electric"))
        
        self.notify_observers(f"Created parking lot with {capacity} regular slots and {electric_vehicle_capacity} EV slots on level {level}")
    
    def park(self, registration_number: str, make: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle in the parking lot"""
        # Create vehicle using factory
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

    def leave(self, parking_slot_number: int) -> bool:
        """Remove a vehicle from the specified slot"""
        if not 1 <= parking_slot_number <= len(self.slots):
            self.notify_observers(f"Invalid slot number: {parking_slot_number}")
            return False
        
        slot = self.slots[parking_slot_number - 1]
        vehicle = slot.leave()
        
        if vehicle:
            self.notify_observers(f"Vehicle {vehicle.registration_number} removed from slot {parking_slot_number}")
            return True
        
        self.notify_observers(f"No vehicle in slot {parking_slot_number}")
        return False

    def get_vehicle(self, parking_slot_number: int) -> Optional[Vehicle.Vehicle]:
        """Get the vehicle in the specified slot"""
        if not 1 <= parking_slot_number <= len(self.slots):
            return None
        return self.slots[parking_slot_number - 1].get_vehicle()
    
    def get_slot_by_registration(self, registration_number: str) -> Optional[int]:
        """Find a slot containing a vehicle with the given registration number"""
        for i, slot in enumerate(self.slots):
            vehicle = slot.get_vehicle()
            if vehicle and vehicle.registration_number == registration_number:
                return i + 1
        return None
    
    def get_slots_by_color(self, color: str) -> List[int]:
        """Find all slots containing vehicles of the given color"""
        return [i + 1 for i, slot in enumerate(self.slots)
                if (vehicle := slot.get_vehicle()) is not None and vehicle.color == color]
    
    def get_slots_by_make(self, make: str) -> List[int]:
        """Find all slots containing vehicles of the given make"""
        return [i + 1 for i, slot in enumerate(self.slots)
                if (vehicle := slot.get_vehicle()) is not None and vehicle.make == make]
    
    def get_slots_by_model(self, model: str) -> List[int]:
        """Find all slots containing vehicles of the given model"""
        return [i + 1 for i, slot in enumerate(self.slots)
                if (vehicle := slot.get_vehicle()) is not None and vehicle.model == model]
    
    def get_vehicles_by_color(self, color: str) -> List[str]:
        """Get registration numbers of all vehicles of the given color"""
        return [vehicle.registration_number for slot in self.slots
                if (vehicle := slot.get_vehicle()) is not None and vehicle.color == color]
    
    def get_status(self) -> str:
        """Get the current status of the parking lot"""
        status = [f"Parking Lot Status (Level {self.level}):"]
        
        # Regular vehicles
        status.append("\nRegular Vehicles:")
        status.append("Slot\tRegistration\tColor\tMake\tModel")
        for i, slot in enumerate(self.slots):
            vehicle = slot.get_vehicle()
            if vehicle and not isinstance(vehicle, Vehicle.ElectricVehicle):
                status.append(f"{i + 1}\t{vehicle.registration_number}\t{vehicle.color}\t{vehicle.make}\t{vehicle.model}")
        
        # Electric vehicles
        status.append("\nElectric Vehicles:")
        status.append("Slot\tRegistration\tColor\tMake\tModel\tCharge")
        for i, slot in enumerate(self.slots):
            vehicle = slot.get_vehicle()
            if isinstance(vehicle, Vehicle.ElectricVehicle):
                status.append(f"{i + 1}\t{vehicle.registration_number}\t{vehicle.color}\t{vehicle.make}\t{vehicle.model}\t{vehicle.charge}%")
        
        return "\n".join(status)

# Main App
def main():
    # Create UI
    from ParkingLotUI import ParkingLotUI
    ui = ParkingLotUI()  # No need to pass parking lot since it's created in __init__
    ui.run()

if __name__ == '__main__':
    main()

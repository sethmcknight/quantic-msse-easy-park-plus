"""
Parking Manager Module

This module implements the parking lot management system.
It uses the State Pattern to manage parking slot states, the Observer Pattern for UI updates,
the Command Pattern to encapsulate parking operations, the Singleton Pattern to ensure
a single instance of the parking lot, the Adapter Pattern for legacy code compatibility,
and the Composite Pattern for multi-level parking lots.

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

5. Multiple Parking Lot Instances
   - Removed: Multiple parking lot instances
   - Solution: Singleton Pattern
   - Benefit: Single source of truth

6. Legacy Code Incompatibility
   - Removed: Direct use of old method names
   - Solution: Adapter Pattern
   - Benefit: Backward compatibility

7. Complex Level Management
   - Removed: Direct level handling
   - Solution: Composite Pattern
   - Benefit: Uniform level operations

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

4. Singleton Pattern
   - Purpose: Ensure single parking lot instance
   - Components: Private constructor and instance method
   - Benefit: Consistent state management

5. Adapter Pattern
   - Purpose: Handle legacy code compatibility
   - Components: LegacyParkingLotAdapter
   - Benefit: Backward compatibility

6. Composite Pattern
   - Purpose: Handle multi-level parking lots
   - Components: ParkingLotComponent interface
   - Benefit: Uniform level operations

Usage:
    The ParkingLot class is the main entry point for parking operations.
    It manages parking slots and notifies observers of changes.

Example:
    >>> parking_lot = ParkingLot.get_instance()
    >>> parking_lot.create_parking_lot(10, 5, 1)  # 10 regular slots, 5 EV slots, level 1
    >>> parking_lot.park("ABC123", "Toyota", "Camry", "Red", False, False)
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
        self._state: ParkingSlotState = EmptyState()
    
    @property
    def slot_type(self) -> str:
        return self._slot_type
    
    def can_park(self, vehicle: Vehicle.Vehicle) -> bool:
        return self._state.can_park(vehicle)
    
    def park(self, vehicle: Vehicle.Vehicle) -> bool:
        if self._state.can_park(vehicle):
            self._state = OccupiedState(vehicle)
            return True
        return False
    
    def leave(self) -> Optional[Vehicle.Vehicle]:
        vehicle = self._state.leave()
        self._state = EmptyState()
        return vehicle
    
    def get_vehicle(self) -> Optional[Vehicle.Vehicle]:
        return self._state.get_vehicle()
    
    def reserve(self, vehicle_type: str) -> None:
        self._state = ReservedState(vehicle_type)

class ParkingLotObserver(ABC):
    """Abstract base class for parking lot observers"""
    
    @abstractmethod
    def update(self, message: str) -> None:
        """Handle updates from the parking lot"""
        pass

class ParkingLotComponent(ABC):
    """Abstract base class for parking lot components"""
    
    @abstractmethod
    def get_level(self) -> int:
        """Get the level number"""
        pass
    
    @abstractmethod
    def get_slots(self) -> List[ParkingSlot]:
        """Get all slots in this component"""
        pass
    
    @abstractmethod
    def get_available_slots(self) -> List[ParkingSlot]:
        """Get available slots in this component"""
        pass
    
    @abstractmethod
    def get_occupied_slots(self) -> List[ParkingSlot]:
        """Get occupied slots in this component"""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get the status of this component"""
        pass

class MultiLevelParkingLot(ParkingLotComponent):
    """Class representing a multi-level parking lot"""
    
    def __init__(self):
        self.levels: List['SingleLevelParkingLot'] = []
        self.name: str = "Downtown Parking"  # Default name
    
    def get_level(self) -> int:
        return len(self.levels)
    
    def get_slots(self) -> List[ParkingSlot]:
        return [slot for level in self.levels for slot in level.get_slots()]
    
    def get_available_slots(self) -> List[ParkingSlot]:
        return [slot for level in self.levels for slot in level.get_available_slots()]
    
    def get_occupied_slots(self) -> List[ParkingSlot]:
        return [slot for level in self.levels for slot in level.get_occupied_slots()]
    
    def get_status(self) -> str:
        return "\n\n".join(level.get_status() for level in self.levels)
    
    def add_level(self, level: 'SingleLevelParkingLot') -> None:
        """Add a level to the parking lot"""
        self.levels.append(level)
        level.set_parent(self)
    
    def get_level_by_number(self, level_number: int) -> Optional['SingleLevelParkingLot']:
        """Get a level by its number"""
        for level in self.levels:
            if level.get_level() == level_number:
                return level
        return None
    
    def set_name(self, name: str) -> None:
        """Set the name of the parking lot"""
        self.name = name

class SingleLevelParkingLot(ParkingLotComponent):
    """Class representing a single level of a parking lot"""
    
    def __init__(self, level: int):
        """Initialize the parking lot level"""
        self.level = level
        self.regular_slots: List[ParkingSlot] = []
        self.ev_slots: List[ParkingSlot] = []
        self.parent: Optional[MultiLevelParkingLot] = None
        self.name: Optional[str] = None
    
    def get_level(self) -> int:
        """Get the level number"""
        return self.level
    
    def get_name(self) -> Optional[str]:
        """Get the lot name"""
        return self.name
    
    def set_name(self, name: str) -> None:
        """Set the lot name"""
        self.name = name
    
    def get_regular_slots(self) -> List[ParkingSlot]:
        """Get all regular slots"""
        return self.regular_slots
    
    def get_ev_slots(self) -> List[ParkingSlot]:
        """Get all EV slots"""
        return self.ev_slots
    
    def get_slots(self) -> List[ParkingSlot]:
        return self.regular_slots + self.ev_slots
    
    def get_available_slots(self) -> List[ParkingSlot]:
        return [slot for slot in self.get_slots() if slot.get_vehicle() is None]
    
    def get_occupied_slots(self) -> List[ParkingSlot]:
        return [slot for slot in self.get_slots() if slot.get_vehicle() is not None]
    
    def get_status(self) -> str:
        """Get the status of this component"""
        status: List[str] = [f"Parking Lot: {self.parent.name if self.parent else 'Downtown Parking'}", f"Level {self.level} Status:"]
        # Regular slots
        for i, slot in enumerate(self.regular_slots):
            vehicle = slot.get_vehicle()
            if vehicle:
                status.append(f"Slot {i + 1}: {vehicle.get_info()}")
            else:
                status.append(f"Slot {i + 1}: Empty Regular")
        # EV slots
        for i, slot in enumerate(self.ev_slots):
            vehicle = slot.get_vehicle()
            if vehicle:
                status.append(f"Slot {i + 1}: {vehicle.get_info()}")
            else:
                status.append(f"Slot {i + 1}: Empty EV")
        return "\n".join(status)
    
    def add_regular_slots(self, slots: List[ParkingSlot]) -> None:
        self.regular_slots.extend(slots)
    
    def add_ev_slots(self, slots: List[ParkingSlot]) -> None:
        self.ev_slots.extend(slots)
    
    def set_parent(self, parent: MultiLevelParkingLot) -> None:
        self.parent = parent

class ParkingLot:
    """Singleton class representing the parking lot"""
    
    _instance: Optional['ParkingLot'] = None
    levels: List['SingleLevelParkingLot'] = []
    observers: List['ParkingLotObserver'] = []
    command_history: List[Command] = []
    
    def __new__(cls) -> 'ParkingLot':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.levels = []
            self.observers = []
            self.command_history = []
    
    def _find_slots(self, predicate: Callable[[Vehicle.Vehicle], bool]) -> List[int]:
        """Find slots matching a predicate function"""
        slots: List[int] = []
        for level in self.levels:
            for i, slot in enumerate(level.get_slots()):
                vehicle = slot.get_vehicle()
                if vehicle and predicate(vehicle):
                    slots.append(i + 1)
        return slots
    
    def _find_slot(self, predicate: Callable[[Vehicle.Vehicle], bool]) -> Optional[int]:
        """Find first slot matching a predicate function"""
        for level in self.levels:
            for i, slot in enumerate(level.get_slots()):
                vehicle = slot.get_vehicle()
                if vehicle and predicate(vehicle):
                    return i + 1
        return None
    
    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle.Vehicle]:
        """Get all vehicles in a specific lot and level"""
        vehicles: Dict[int, Vehicle.Vehicle] = {}
        for level_obj in self.levels:
            if level_obj.get_name() == lot_name and level_obj.get_level() == level:
                for i, slot in enumerate(level_obj.get_slots()):
                    vehicle = slot.get_vehicle()
                    if vehicle:
                        vehicles[i + 1] = vehicle
        return vehicles
    
    def create_parking_lot(self, capacity: int, ev_capacity: int, level: int) -> None:
        """Create a new parking lot level"""
        level_obj = SingleLevelParkingLot(level)
        level_obj.add_regular_slots([ParkingSlot("standard") for _ in range(capacity)])
        level_obj.add_ev_slots([ParkingSlot("electric") for _ in range(ev_capacity)])
        self.levels.append(level_obj)
        self.notify_observers(f"Created parking lot level {level} with {capacity} regular slots and {ev_capacity} EV slots")
    
    def notify_observers(self, message: str) -> None:
        """Notify all observers of a change"""
        for observer in self.observers:
            observer.update(message)
    
    def register_observer(self, observer: 'ParkingLotObserver') -> None:
        """Register a new observer"""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer: 'ParkingLotObserver') -> None:
        """Remove an observer"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def get_status(self) -> str:
        """Get the status of all parking lots"""
        status: List[str] = []
        for level in self.levels:
            status.append(level.get_status())
        return "\n".join(status)
    
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
                return Vehicle.VehicleFactory.create_electric_motorcycle(reg, make, model, color)
            return Vehicle.VehicleFactory.create_electric_car(reg, make, model, color)
        if is_motorcycle:
            return Vehicle.VehicleFactory.create_motorcycle(reg, make, model, color)
        return Vehicle.VehicleFactory.create_car(reg, make, model, color)
    
    def park(self, reg: str, make: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle"""
        vehicle = self._create_vehicle(reg, make, model, color, is_electric, is_motorcycle)
        
        for level in self.levels:
            for i, slot in enumerate(level.get_slots()):
                if slot.can_park(vehicle) and slot.park(vehicle):
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
    parking_lot = ParkingLot.get_instance()
    
    # Create UI
    from ParkingLotUI import ParkingLotUI
    ui = ParkingLotUI(parking_lot)  # Pass parking lot directly
    ui.run()

if __name__ == '__main__':
    main()

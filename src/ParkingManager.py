"""
Parking Manager Module

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
"""

import Vehicle as Vehicle
from typing import Optional, List, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass

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
    
    def __init__(self, parking_lot: 'ParkingLot', capacity: int, ev_capacity: int, level: int):
        self._parking_lot = parking_lot
        self._capacity = capacity
        self._ev_capacity = ev_capacity
        self._level = level
        self._previous_slots: Optional[List[ParkingSlot]] = None
        self._previous_level: int = 0
    
    def execute(self) -> bool:
        self._previous_slots = self._parking_lot.slots.copy() if self._parking_lot.slots else None
        self._previous_level = self._parking_lot.level
        self._parking_lot.create_parking_lot(self._capacity, self._ev_capacity, self._level)
        return True
    
    def undo(self) -> bool:
        if self._previous_slots is not None:
            self._parking_lot.slots = self._previous_slots
            self._parking_lot.level = self._previous_level
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
        self._slot_number: Optional[int] = None
    
    def execute(self) -> bool:
        self._slot_number = self._parking_lot.park(
            self._registration_number, self._make, self._model,
            self._color, self._is_electric, self._is_motorcycle
        )
        return self._slot_number is not None
    
    def undo(self) -> bool:
        if self._slot_number is not None:
            return self._parking_lot.leave(self._slot_number)
        return False

class LeaveCommand:
    """Command to remove a vehicle"""
    
    def __init__(self, parking_lot: 'ParkingLot', slot_number: int):
        self._parking_lot = parking_lot
        self._slot_number = slot_number
        self._vehicle: Optional[Vehicle.Vehicle] = None
    
    def execute(self) -> bool:
        self._vehicle = self._parking_lot.get_vehicle(self._slot_number)
        return self._parking_lot.leave(self._slot_number)
    
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

class ParkingLot:
    """Class representing a parking lot"""
    
    _instance: Optional['ParkingLot'] = None
    
    def __new__(cls) -> 'ParkingLot':
        """Ensure only one instance of ParkingLot exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the parking lot if not already initialized"""
        if self._initialized:
            return
        
        self.slots: List[ParkingSlot] = []
        self.level: int = 0
        self._observers: List[ParkingLotObserver] = []
        self._command_history: List[Command] = []
        self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'ParkingLot':
        """Get the singleton instance of the parking lot"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer to receive updates"""
        self._observers.append(observer)
    
    def notify_observers(self, message: str) -> None:
        """Notify all observers of a change"""
        for observer in self._observers:
            observer.update(message)
    
    def execute_command(self, command: Command) -> bool:
        """Execute a command and add it to history if successful"""
        if command.execute():
            self._command_history.append(command)
            return True
        return False
    
    def undo_last_command(self) -> bool:
        """Undo the last command if possible"""
        if self._command_history:
            command = self._command_history.pop()
            return command.undo()
        return False
    
    def create_parking_lot(self, capacity: int, ev_capacity: int, level: int) -> None:
        """Create a new parking lot with the specified capacity"""
        self.slots = []
        self.level = level
        
        # Create regular slots
        for _ in range(capacity):
            self.slots.append(ParkingSlot("standard"))
        
        # Create EV slots
        for _ in range(ev_capacity):
            self.slots.append(ParkingSlot("electric"))
        
        self.notify_observers(f"Created parking lot with {capacity} regular slots and {ev_capacity} EV slots on level {level}")
    
    def park(self, registration_number: str, make: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle in the parking lot"""
        # Create vehicle using factory
        if is_electric:
            if is_motorcycle:
                vehicle = Vehicle.VehicleFactory.create_electric_motorcycle(registration_number, make, model, color)
            else:
                vehicle = Vehicle.VehicleFactory.create_electric_car(registration_number, make, model, color)
        else:
            if is_motorcycle:
                vehicle = Vehicle.VehicleFactory.create_motorcycle(registration_number, make, model, color)
            else:
                vehicle = Vehicle.VehicleFactory.create_car(registration_number, make, model, color)
        
        # Find suitable slot
        for i, slot in enumerate(self.slots):
            if slot.can_park(vehicle) and vehicle.can_park_in(slot.slot_type):
                if slot.park(vehicle):
                    self.notify_observers(f"Vehicle {registration_number} parked in slot {i + 1}")
                    return i + 1
        
        self.notify_observers(f"Could not park vehicle {registration_number}: No suitable slot available")
        return None
    
    def leave(self, slot_number: int) -> bool:
        """Remove a vehicle from the specified slot"""
        if not 1 <= slot_number <= len(self.slots):
            self.notify_observers(f"Invalid slot number: {slot_number}")
            return False
        
        slot = self.slots[slot_number - 1]
        vehicle = slot.leave()
        
        if vehicle:
            self.notify_observers(f"Vehicle {vehicle.registration_number} removed from slot {slot_number}")
            return True
        
        self.notify_observers(f"No vehicle in slot {slot_number}")
        return False
    
    def get_vehicle(self, slot_number: int) -> Optional[Vehicle.Vehicle]:
        """Get the vehicle in the specified slot"""
        if not 1 <= slot_number <= len(self.slots):
            return None
        return self.slots[slot_number - 1].get_vehicle()
    
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
    ui = ParkingLotUI(parking_lot)
    ui.run()

if __name__ == '__main__':
    main()

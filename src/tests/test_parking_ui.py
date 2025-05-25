"""
Test suite for the Parking Lot UI

This module contains tests for the ParkingLotUI class using unittest and tkinter testing utilities.
"""

import unittest
import tkinter as tk
from ParkingLotUI import ParkingLotUI, ParkingLotInterface, VehicleData, SearchCriteria, ParkingLotData
from typing import List, Dict, Optional, Any
from ParkingManager import ParkingLotObserver

class MockParkingLot(ParkingLotInterface):
    """Mock parking lot for testing UI functionality"""
    
    def __init__(self, name: str, levels: int, slots_per_level: int):
        self.name = name
        self.levels = levels
        self.slots_per_level = slots_per_level
        self.lots: Dict[str, Dict[int, Dict[int, Optional[VehicleData]]]] = {}
        self.vehicles: Dict[str, Dict[int, Dict[int, VehicleData]]] = {}
        self.observers: List[ParkingLotObserver] = []
        self.current_lot_name = name
        self.current_level = 1
        # Initialize the lot structure
        self.lots[name] = {}
        for level in range(1, levels + 1):
            self.lots[name][level] = {}
            for slot in range(1, slots_per_level + 1):
                self.lots[name][level][slot] = None
    
    def register_observer(self, observer: Any) -> None:
        self.observers.append(observer)
    
    def set_name(self, name: str) -> None:
        """Set the name of the parking lot"""
        self.name = name
    
    def create_parking_lot(self, data: ParkingLotData) -> None:
        """Create a new parking lot"""
        if data.name in self.lots:
            return
        self.lots[data.name] = {}
        self.lots[data.name][data.level] = {}
        for slot in range(1, data.regular_slots + 1):
            self.lots[data.name][data.level][slot] = None
        for slot in range(data.regular_slots + 1, data.regular_slots + data.ev_slots + 1):
            self.lots[data.name][data.level][slot] = None
        self.vehicles[data.name] = {}
        self.vehicles[data.name][data.level] = {}
        self.current_lot_name = data.name
        self.current_level = data.level
    
    def park(self, reg: str, make: str, model: str, color: str, is_electric: bool = False, is_motorcycle: bool = False) -> Optional[int]:
        data = VehicleData(reg, make, model, color, is_electric, is_motorcycle)
        lot_name = self.current_lot_name
        level = self.current_level
        # Find the next available slot
        if lot_name not in self.lots or level not in self.lots[lot_name]:
            return None
        for slot in sorted(self.lots[lot_name][level].keys()):
            if self.lots[lot_name][level][slot] is None:
                self.lots[lot_name][level][slot] = data
                self.vehicles[lot_name] = self.vehicles.get(lot_name, {})
                self.vehicles[lot_name][level] = self.vehicles[lot_name].get(level, {})
                self.vehicles[lot_name][level][slot] = data
                return slot
        return None
    
    def leave(self, slot_number: int) -> bool:
        """Remove a vehicle from a slot"""
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                if slot_number in level_data:
                    del level_data[slot_number]
                    return True
        return False
    
    def get_slot_by_registration(self, reg: str) -> Optional[int]:
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                for slot, vehicle in level_data.items():
                    if vehicle.registration == reg:
                        return slot
        return None
    
    def get_vehicle(self, slot_number: int) -> Optional[Any]:
        """Get vehicle by slot number"""
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                if slot_number in level_data:
                    return level_data[slot_number]
        return None
    
    def get_slots_by_color(self, color: str) -> List[int]:
        slots: List[int] = []
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                for slot, vehicle in level_data.items():
                    if vehicle.color == color:
                        slots.append(slot)
        return slots
    
    def get_slots_by_make(self, make: str) -> List[int]:
        slots: List[int] = []
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                for slot, vehicle in level_data.items():
                    if vehicle.make == make:
                        slots.append(slot)
        return slots
    
    def get_slots_by_model(self, model: str) -> List[int]:
        slots: List[int] = []
        for lot_data in self.vehicles.values():
            for level_data in lot_data.values():
                for slot, vehicle in level_data.items():
                    if vehicle.model == model:
                        slots.append(slot)
        return slots
    
    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Any]:
        """Get all vehicles in a specific lot and level"""
        print(f"[DEBUG] get_vehicles_in_lot called with lot_name={lot_name}, level={level}")
        if lot_name not in self.vehicles or level not in self.vehicles[lot_name]:
            return {}
        vehicles = self.vehicles[lot_name][level]
        print(f"[DEBUG] get_vehicles_in_lot returned {len(vehicles)} vehicles")
        return vehicles
    
    def _matches_criteria(self, vehicle: VehicleData, criteria: SearchCriteria, lot_name: str, level: int) -> bool:
        """Check if a vehicle matches the search criteria"""
        if criteria.search_type == "registration" and criteria.registration:
            return vehicle.registration.lower() == criteria.registration.lower()
        elif criteria.search_type == "color" and criteria.color:
            return vehicle.color.lower() == criteria.color.lower()
        elif criteria.search_type == "make" and criteria.make:
            return vehicle.make.lower() == criteria.make.lower()
        elif criteria.search_type == "model" and criteria.model:
            return vehicle.model.lower() == criteria.model.lower()
        return False
    
    def search_vehicles(self, criteria: SearchCriteria) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for lot_name, levels in self.lots.items():
            for level, slots_dict in levels.items():
                for slot, vehicle in slots_dict.items():
                    if vehicle and self._matches_criteria(vehicle, criteria, lot_name, level):
                        results.append({
                            "slot": slot,
                            "vehicle": vehicle,
                            "lot": lot_name,
                            "level": level
                        })
        return results
    
    def get_status(self) -> str:
        status_lines: List[str] = []
        for lot_name, levels in self.lots.items():
            for level, slots_dict in levels.items():
                status_lines.append(f"Parking Lot: {lot_name}")
                status_lines.append(f"Level {level} Status:")
                for slot, vehicle in slots_dict.items():
                    if vehicle is None:
                        status_lines.append(f"Slot {slot}: Empty")
                    else:
                        vehicle_type = "EV Motorcycle" if vehicle.is_electric and vehicle.is_motorcycle else \
                                     "EV" if vehicle.is_electric else \
                                     "Motorcycle" if vehicle.is_motorcycle else "Standard"
                        status_lines.append(f"Slot {slot}: {vehicle.registration} {vehicle.make} {vehicle.model} {vehicle.color} {vehicle_type}")
        self.status_output = status_lines
        return "\n".join(status_lines)
    
    def get_lot_names(self) -> List[str]:
        """Get all parking lot names"""
        return list(self.lots.keys())
    
    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get all levels in a specific lot"""
        if lot_name not in self.lots:
            return []
        return sorted(self.lots[lot_name].keys())
    
    def get_slots_for_level(self, lot_name: str, level: int) -> List[int]:
        """Get all slots in a specific level"""
        if lot_name not in self.lots or level not in self.lots[lot_name]:
            return []
        return sorted(self.lots[lot_name][level].keys())
    
    def get_available_slots(self, lot_name: str, level: int) -> List[int]:
        """Get all available slots in a specific level"""
        if lot_name not in self.lots or level not in self.lots[lot_name]:
            return []
        return [slot for slot, vehicle in self.lots[lot_name][level].items() if vehicle is None]
    
    def get_occupied_slots(self, lot_name: str, level: int) -> List[int]:
        """Get all occupied slots in a specific level"""
        if lot_name not in self.lots or level not in self.lots[lot_name]:
            return []
        return [slot for slot, vehicle in self.lots[lot_name][level].items() if vehicle is not None]
    
    def _update_status(self) -> None:
        """Update the status output"""
        self.get_status()

    def park_vehicle(self, data: VehicleData) -> Optional[int]:
        """Park a vehicle in the lot"""
        return self.park(
            data.registration,
            data.make,
            data.model,
            data.color,
            data.is_electric,
            data.is_motorcycle
        )

    def remove_vehicle(self, slot_number: int) -> bool:
        """Remove a vehicle from the lot"""
        return self.leave(slot_number)

class TestParkingLotUI(unittest.TestCase):
    """Test cases for the ParkingLotUI class"""

    def setUp(self):
        """Set up test environment before each test"""
        self.parking_lot = MockParkingLot("Test Lot", 1, 10)
        self.root = tk.Tk()
        self.ui = ParkingLotUI(self.parking_lot)
        self.root.withdraw()  # Hide the window during tests

    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()

    def clear_message(self):
        """Clear the message area"""
        self.ui.message_area.delete("1.0", tk.END)

    def get_message(self):
        """Get the current message"""
        return self.ui.message_area.get("1.0", tk.END).strip()

    def test_create_lot_valid_and_invalid(self):
        """Test creating parking lots with valid and invalid inputs"""
        # Invalid: empty name
        self.ui.lot_name_value.set("")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Please enter a lot name", self.get_message())

        # Invalid: non-integer slots
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("abc")
        self.ui.ev_num_value.set("xyz")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Please enter valid numbers", self.get_message())

        # Valid creation
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Created parking lot LotA", self.get_message())

    def test_duplicate_lot_names(self):
        """Test creating lots with duplicate names"""
        # Create first lot
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Created parking lot LotA", self.get_message())

        # Try to create another lot with same name
        self.ui.level_value.set("2")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Created parking lot LotA", self.get_message())

    def test_vehicle_parking_types_and_edge_cases(self):
        """Test parking different types of vehicles and edge cases"""
        # Create a lot first
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.ui.create_lot()

        # Test regular car
        self.ui.reg_value.set("ABC123")
        self.ui.make_value.set("Toyota")
        self.ui.model_value.set("Camry")
        self.ui.color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(False)
        self.clear_message()
        self.ui.park_button.invoke()
        self.assertIn("Vehicle parked in slot", self.get_message())

        # Test electric car
        self.ui.reg_value.set("DEF456")
        self.ui.make_value.set("Tesla")
        self.ui.model_value.set("Model 3")
        self.ui.color_value.set("Black")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(True)
        self.clear_message()
        self.ui.park_button.invoke()
        self.assertIn("Vehicle parked in slot", self.get_message())

        # Test motorcycle
        self.ui.reg_value.set("GHI789")
        self.ui.make_value.set("Honda")
        self.ui.model_value.set("CBR")
        self.ui.color_value.set("Blue")
        self.ui.vehicle_type_value.set("Motorcycle")
        self.ui.ev_value.set(False)
        self.clear_message()
        self.ui.park_button.invoke()
        self.assertIn("Vehicle parked in slot", self.get_message())

        # Test invalid input
        self.ui.reg_value.set("")
        self.clear_message()
        self.ui.park_button.invoke()
        self.assertIn("Please enter registration number", self.get_message())

    def test_remove_vehicle(self):
        """Test removing vehicles"""
        # Create a lot and park a vehicle
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.ui.create_lot()

        self.ui.reg_value.set("ABC123")
        self.ui.make_value.set("Toyota")
        self.ui.model_value.set("Camry")
        self.ui.color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(False)
        self.ui.park_button.invoke()

        # Show status to populate the tree
        self.ui.show_status_button.invoke()

        # Try to remove without selecting
        self.clear_message()
        self.ui.remove_button.invoke()
        self.assertIn("Please select a slot to remove", self.get_message())

        # Select and remove (only if there is a row)
        children = self.ui.results_tree.get_children()
        if children:
            self.ui.results_tree.selection_set(children[0])
            self.clear_message()
            self.ui.remove_button.invoke()
            self.assertIn("Vehicle removed from slot", self.get_message())
        else:
            self.fail("No rows in results tree to select for removal test.")

    def test_search_all_modes_and_edge_cases(self):
        """Test searching in all modes and edge cases"""
        # Create a lot and park some vehicles
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.ui.create_lot()

        # Park a red Toyota
        self.ui.reg_value.set("ABC123")
        self.ui.make_value.set("Toyota")
        self.ui.model_value.set("Camry")
        self.ui.color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(False)
        self.ui.park_button.invoke()

        # Search by registration
        self.ui.search_reg_value.set("ABC123")
        self.ui.search_color_value.set("")
        self.ui.search_make_value.set("")
        self.ui.search_model_value.set("")
        self.ui.search_type.set("registration")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 1)

        # Search by color
        self.ui.search_reg_value.set("")
        self.ui.search_color_value.set("Red")
        self.ui.search_make_value.set("")
        self.ui.search_model_value.set("")
        self.ui.search_type.set("color")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 1)

        # Search by make
        self.ui.search_reg_value.set("")
        self.ui.search_color_value.set("")
        self.ui.search_make_value.set("Toyota")
        self.ui.search_model_value.set("")
        self.ui.search_type.set("make")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 1)

        # Search by model
        self.ui.search_reg_value.set("")
        self.ui.search_color_value.set("")
        self.ui.search_make_value.set("")
        self.ui.search_model_value.set("Camry")
        self.ui.search_type.set("model")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 1)

        # Test empty search
        self.ui.search_reg_value.set("")
        self.ui.search_color_value.set("")
        self.ui.search_make_value.set("")
        self.ui.search_model_value.set("")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 0)

    def test_ui_edge_cases(self):
        """Test UI edge cases"""
        # Test whitespace handling
        self.ui.lot_name_value.set("  LotA  ")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Created parking lot LotA", self.get_message())

        # Test case sensitivity
        self.ui.reg_value.set("ABC123")
        self.ui.make_value.set("Toyota")
        self.ui.model_value.set("Camry")
        self.ui.color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(False)
        self.ui.park_button.invoke()

        self.ui.search_reg_value.set("abc123")
        self.ui.search_type.set("registration")
        self.clear_message()
        self.ui.search_button.invoke()
        self.assertEqual(len(self.ui.results_tree.get_children()), 1)

        # Test special characters
        self.ui.lot_name_value.set("Lot-A")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.clear_message()
        self.ui.create_lot()
        self.assertIn("Created parking lot Lot-A", self.get_message())

    def test_show_full_status(self):
        """Test showing full status"""
        self.ui.lot_name_value.set("LotA")
        self.ui.level_value.set("1")
        self.ui.num_value.set("10")
        self.ui.ev_num_value.set("5")
        self.ui.create_lot()
        self.ui.level_value.set("1")  # Ensure level is set after lot creation
        # Park a vehicle
        self.ui.reg_value.set("ABC123")
        self.ui.make_value.set("Toyota")
        self.ui.model_value.set("Camry")
        self.ui.color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.ev_value.set(False)
        self.ui.park_button.invoke()
    
        # Debug print for level value
        print(f"[TEST DEBUG] level_value before status: {self.ui.level_value.get()}")
        self.ui.level_value.set("1")  # Ensure level is set right before status
        # Call status_button to trigger status display
        self.ui.status_button.invoke()
    
        # Check if the results tree is populated
        self.assertNotEqual(len(self.ui.results_tree.get_children()), 0)

if __name__ == '__main__':
    unittest.main() 
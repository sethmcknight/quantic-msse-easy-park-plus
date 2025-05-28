"""
Integration tests for the Parking Management System

This module contains tests that verify the interaction between different components
of the system without modifying their functionality.
"""

import unittest
import tkinter as tk
from tkinter import ttk
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ParkingLotUI import ParkingLotUI
from ParkingManager import ParkingLot
from models import VehicleData, SearchCriteria, ParkingLotData, ParkingLevelData, ParkingSlotData, SlotType, VehicleType
from interfaces import ParkingLotObserver

class TestParkingSystemIntegration(unittest.TestCase):
    """Integration tests for the parking system components"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = tk.Tk()
        self.ui = ParkingLotUI()
        self.ui.main_window = self.root
        
        # Initialize UI state variables
        self.ui.state_manager.lot_name_value = tk.StringVar()
        self.ui.state_manager.parking_level_value = tk.StringVar()
        self.ui.state_manager.regular_slots_value = tk.StringVar()
        self.ui.state_manager.electric_vehicle_slots_value = tk.StringVar()
        self.ui.state_manager.registration_number_value = tk.StringVar()
        self.ui.state_manager.vehicle_manufacturer_value = tk.StringVar()
        self.ui.state_manager.vehicle_model_value = tk.StringVar()
        self.ui.state_manager.vehicle_color_value = tk.StringVar()
        self.ui.state_manager.vehicle_type_value = tk.StringVar()
        self.ui.state_manager.is_electric_value = tk.BooleanVar()
        self.ui.state_manager.park_lot_value = tk.StringVar()
        self.ui.state_manager.park_level_value = tk.StringVar()
        self.ui.state_manager.search_registration_number_value = tk.StringVar()
        self.ui.state_manager.search_type_value = tk.StringVar()
        
        # Create a test parking lot
        slots = []
        # Add regular slots
        for i in range(1, 6):
            slots.append(ParkingSlotData(
                slot_number=i,
                is_occupied=False,
                slot_type=SlotType.REGULAR,
                level=1,
                lot_name="Test Lot"
            ))
        # Add electric slots
        for i in range(6, 8):
            slots.append(ParkingSlotData(
                slot_number=i,
                is_occupied=False,
                slot_type=SlotType.ELECTRIC,
                level=1,
                lot_name="Test Lot"
            ))
        
        self.lot_data = ParkingLotData(
            name="Test Lot",
            levels=[ParkingLevelData(
                level=1,
                slots=slots,
                lot_name="Test Lot"
            )]
        )
        self.ui.parking_manager.create_lot(self.lot_data)
    
    def tearDown(self):
        """Clean up test environment"""
        self.root.destroy()
    
    def test_complete_parking_workflow(self):
        """Test the complete workflow from UI to parking manager"""
        # 1. Create parking lot through UI
        self.ui.state_manager.lot_name_value.set("Test Lot")
        self.ui.state_manager.parking_level_value.set("1")
        self.ui.state_manager.regular_slots_value.set("5")
        self.ui.state_manager.electric_vehicle_slots_value.set("2")
        self.ui._handle_create_lot()
        
        # Verify lot was created
        lots = self.ui.parking_manager.get_lot_names()
        self.assertIn("Test Lot", lots)
        
        # 2. Park a vehicle through UI
        self.ui.state_manager.registration_number_value.set("ABC123")
        self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
        self.ui.state_manager.vehicle_model_value.set("Camry")
        self.ui.state_manager.vehicle_color_value.set("Red")
        self.ui.state_manager.vehicle_type_value.set("Car")
        self.ui.state_manager.is_electric_value.set(False)
        self.ui.state_manager.park_lot_value.set("Test Lot")
        self.ui.state_manager.park_level_value.set("1")
        
        # Park the vehicle
        self.ui._handle_park()
        
        # Verify vehicle was parked
        vehicles = self.ui.parking_manager.get_vehicles_in_lot("Test Lot", 1)
        self.assertIn(1, vehicles)
        self.assertEqual(vehicles[1].registration_number, "ABC123")
        
        # 3. Search for the vehicle
        self.ui.state_manager.search_registration_number_value.set("ABC123")
        self.ui.state_manager.search_type_value.set("registration")
        self.ui._handle_search()
        
        # Verify search results
        items = self.ui.results_tree.get_children()
        self.assertTrue(len(items) > 0)
        
        # 4. Remove the vehicle
        self.ui.state_manager.park_lot_value.set("Test Lot")
        self.ui.state_manager.park_level_value.set("1")
        with patch.object(self.ui, '_get_selected_slot', return_value=1):
            self.ui._handle_remove()
        
        # Verify vehicle was removed
        vehicles = self.ui.parking_manager.get_vehicles_in_lot("Test Lot", 1)
        self.assertNotIn(1, vehicles)
    
    def test_error_handling_workflow(self):
        """Test error handling across components"""
        # 1. Try to park in non-existent lot
        self.ui.state_manager.registration_number_value.set("ABC123")
        self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
        self.ui.state_manager.vehicle_model_value.set("Camry")
        self.ui.state_manager.vehicle_color_value.set("Red")
        self.ui.state_manager.vehicle_type_value.set("Car")
        self.ui.state_manager.is_electric_value.set(False)
        self.ui.state_manager.park_lot_value.set("Non Existent Lot")
        self.ui.state_manager.park_level_value.set("1")
        
        # Park the vehicle
        self.ui._handle_park()
        
        # Verify error was handled
        self.assertIn("Error", self.ui.message_area.get("1.0", tk.END))
        
        # 2. Try to remove from non-existent lot
        self.ui.state_manager.park_lot_value.set("Non Existent Lot")
        self.ui.state_manager.park_level_value.set("1")
        with patch.object(self.ui, '_get_selected_slot', return_value=1):
            self.ui._handle_remove()
        
        # Verify error was handled
        self.assertIn("Error", self.ui.message_area.get("1.0", tk.END))
    
    def test_concurrent_operations(self):
        """Test handling of concurrent operations"""
        # 1. Park multiple vehicles
        vehicles = [
            ("ABC123", "Toyota", "Camry", "Red", False),
            ("DEF456", "Honda", "Civic", "Blue", False),
            ("GHI789", "Tesla", "Model 3", "White", True)
        ]
        
        for reg, man, mod, col, is_ev in vehicles:
            self.ui.state_manager.registration_number_value.set(reg)
            self.ui.state_manager.vehicle_manufacturer_value.set(man)
            self.ui.state_manager.vehicle_model_value.set(mod)
            self.ui.state_manager.vehicle_color_value.set(col)
            self.ui.state_manager.is_electric_value.set(is_ev)
            self.ui.state_manager.park_lot_value.set("Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            self.ui._handle_park()
        
        # Verify all vehicles were parked
        parked_vehicles = self.ui.parking_manager.get_vehicles_in_lot("Test Lot", 1)
        self.assertEqual(len(parked_vehicles), len(vehicles))
        
        # 2. Search for all vehicles
        for reg, _, _, _, _ in vehicles:
            self.ui.state_manager.search_registration_number_value.set(reg)
            self.ui.state_manager.search_type_value.set("registration")
            self.ui._handle_search()
            
            # Verify search results
            items = self.ui.results_tree.get_children()
            self.assertTrue(len(items) > 0)
    
    def test_boundary_conditions(self):
        """Test system behavior at boundaries"""
        # 1. Try to park more vehicles than slots
        for i in range(10):  # More than available slots
            self.ui.state_manager.registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
            self.ui.state_manager.vehicle_model_value.set("Camry")
            self.ui.state_manager.vehicle_color_value.set("Red")
            self.ui.state_manager.is_electric_value.set(False)
            self.ui.state_manager.park_lot_value.set("Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            self.ui._handle_park()
        
        # Verify only available slots were used
        parked_vehicles = self.ui.parking_manager.get_vehicles_in_lot("Test Lot", 1)
        self.assertLessEqual(len(parked_vehicles), 7)  # 5 regular + 2 electric slots
        
        # 2. Try to park electric vehicle in regular slot
        self.ui.state_manager.registration_number_value.set("EV123")
        self.ui.state_manager.vehicle_manufacturer_value.set("Tesla")
        self.ui.state_manager.vehicle_model_value.set("Model 3")
        self.ui.state_manager.vehicle_color_value.set("White")
        self.ui.state_manager.is_electric_value.set(True)
        self.ui.state_manager.park_lot_value.set("Test Lot")
        self.ui.state_manager.park_level_value.set("1")
        
        # Park the vehicle
        self.ui._handle_park()
        
        # Verify vehicle was parked in electric slot
        parked_vehicles = self.ui.parking_manager.get_vehicles_in_lot("Test Lot", 1)
        electric_slots = [slot for slot, vehicle in parked_vehicles.items() 
                         if vehicle.is_electric]
        self.assertTrue(len(electric_slots) > 0)

if __name__ == "__main__":
    unittest.main() 
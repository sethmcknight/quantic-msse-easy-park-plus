"""
Test suite for the Parking Lot UI

This module contains tests for the ParkingLotUI class using unittest and tkinter testing utilities.
The tests simulate user interactions with the app and verify that the UI responds correctly.

Note: This test suite intentionally accesses protected methods (prefixed with _) of the ParkingLotUI class
to test internal implementation details. This is a common practice in testing, and the linter warnings
about protected method access can be safely ignored.
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
from models import VehicleData, SearchCriteria, ParkingLotData, ParkingLevelData, VehicleType, SlotType
from interfaces import ParkingLotObserver

class TestParkingLotUI(unittest.TestCase):
    """Test cases for the ParkingLotUI class"""
    
    def setUp(self):
        """Set up test environment"""
        self.root = tk.Tk()
        self.ui = ParkingLotUI()
        self.ui.main_window = self.root
        
        # Mock the message area
        self.ui.message_area = tk.Text(self.root)
        self.ui.message_area.pack()
        
        # Mock the results tree
        self.ui.results_tree = ttk.Treeview(self.root)
        self.ui.results_tree.pack()
    
    def tearDown(self):
        """Clean up test environment"""
        self.root.destroy()
    
    def test_create_parking_lot(self):
        """Test creating a parking lot through the UI"""
        # Mock the parking manager
        self.ui.parking_manager.create_lot = MagicMock(return_value=True)
        
        # Set input values
        self.ui.lot_name_value.set("Test Lot")
        self.ui.parking_level_value.set("1")
        self.ui.regular_slots_value.set("5")
        self.ui.electric_vehicle_slots_value.set("2")
        
        # Click create button
        self.ui._handle_create_lot()
        
        # Verify parking manager was called with correct data
        self.ui.parking_manager.create_lot.assert_called_once()
        call_args = self.ui.parking_manager.create_lot.call_args[0][0]
        self.assertEqual(call_args.name, "Test Lot")
        self.assertEqual(len(call_args.levels), 1)
        self.assertEqual(call_args.levels[0].regular_slots, 5)
        self.assertEqual(call_args.levels[0].electric_slots, 2)
    
    def test_park_vehicle(self):
        """Test parking a vehicle through the UI"""
        # Mock the parking manager
        self.ui.parking_manager.park_vehicle = MagicMock(return_value=1)
        
        # Set input values
        self.ui.registration_number_value.set("ABC123")
        self.ui.vehicle_manufacturer_value.set("Toyota")
        self.ui.vehicle_model_value.set("Camry")
        self.ui.vehicle_color_value.set("Red")
        self.ui.vehicle_type_value.set("Car")
        self.ui.is_electric_value.set(False)
        self.ui.park_lot_value.set("Test Lot")
        self.ui.park_level_value.set("1")
        
        # Click park button
        self.ui._handle_park()
        
        # Verify parking manager was called with correct data
        self.ui.parking_manager.park_vehicle.assert_called_once()
        call_args = self.ui.parking_manager.park_vehicle.call_args[0]
        self.assertEqual(call_args[0], "Test Lot")  # lot_name
        self.assertEqual(call_args[1], 1)  # level
        self.assertEqual(call_args[2].registration_number, "ABC123")
        self.assertEqual(call_args[2].manufacturer, "Toyota")
        self.assertEqual(call_args[2].model, "Camry")
        self.assertEqual(call_args[2].color, "Red")
        self.assertFalse(call_args[2].is_electric)
        self.assertFalse(call_args[2].is_motorcycle)
    
    def test_remove_vehicle(self):
        """Test removing a vehicle through the UI"""
        # Mock the parking manager
        mock_vehicle = VehicleData(
            registration_number="ABC123",
            manufacturer="Toyota",
            model="Camry",
            color="Red",
            is_electric=False,
            is_motorcycle=False,
            vehicle_type=VehicleType.CAR
        )
        self.ui.parking_manager.remove_vehicle = MagicMock(return_value=mock_vehicle)
        
        # Set input values
        self.ui.park_lot_value.set("Test Lot")
        self.ui.park_level_value.set("1")
        
        # Mock selected slot
        with patch.object(self.ui, '_get_selected_slot', return_value=1):
            # Click remove button
            self.ui._handle_remove()
            
            # Verify parking manager was called with correct data
            self.ui.parking_manager.remove_vehicle.assert_called_once_with("Test Lot", 1, 1)
    
    def test_search_vehicles(self):
        """Test searching for vehicles through the UI"""
        # Mock the parking manager's search methods
        mock_vehicles = {
            1: VehicleData(
                registration_number="ABC123",
                manufacturer="Toyota",
                model="Camry",
                color="Red",
                is_electric=False,
                is_motorcycle=False,
                vehicle_type=VehicleType.CAR
            )
        }
        self.ui.parking_manager.get_vehicles_in_lot = MagicMock(return_value=mock_vehicles)
        self.ui.parking_manager.get_lot_names = MagicMock(return_value=["Test Lot"])
        self.ui.parking_manager.get_levels_for_lot = MagicMock(return_value=[1])
        
        # Test registration search
        self.ui.search_registration_number_value.set("ABC123")
        self.ui.search_type_value.set("registration")
        
        # Click search button
        self.ui._handle_search()
        
        # Verify search was performed
        self.ui.parking_manager.get_vehicles_in_lot.assert_called()
    
    def test_show_status(self):
        """Test showing parking lot status through the UI"""
        # Mock the parking manager's status methods
        mock_status = [
            MagicMock(
                level=1,
                slot=1,
                vehicle=VehicleData(
                    registration_number="ABC123",
                    manufacturer="Toyota",
                    model="Camry",
                    color="Red",
                    is_electric=False,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.CAR
                ),
                is_occupied=True,
                slot_type=SlotType.REGULAR
            )
        ]
        self.ui.parking_manager.get_lot_status = MagicMock(return_value=mock_status)
        
        # Set input values
        self.ui.park_lot_value.set("Test Lot")
        
        # Click show status button
        self.ui._handle_show_status()
        
        # Verify status was retrieved
        self.ui.parking_manager.get_lot_status.assert_called_once_with("Test Lot")
    
    def test_show_lots(self):
        """Test showing all parking lots through the UI"""
        # Mock the parking manager's methods
        self.ui.parking_manager.get_lot_names = MagicMock(return_value=["Test Lot"])
        self.ui.parking_manager.get_levels_for_lot = MagicMock(return_value=[1])
        mock_status = [
            MagicMock(
                level=1,
                slot=1,
                vehicle=None,
                is_occupied=False,
                slot_type=SlotType.REGULAR
            )
        ]
        self.ui.parking_manager.get_lot_status = MagicMock(return_value=mock_status)
        
        # Click show lots button
        self.ui._handle_show_lots()
        
        # Verify methods were called
        self.ui.parking_manager.get_lot_names.assert_called_once()
        self.ui.parking_manager.get_levels_for_lot.assert_called_once_with("Test Lot")
        self.ui.parking_manager.get_lot_status.assert_called()
    
    def test_show_details(self):
        """Test showing lot details through the UI"""
        # Mock the parking manager's methods
        mock_vehicles = {
            1: VehicleData(
                registration_number="ABC123",
                manufacturer="Toyota",
                model="Camry",
                color="Red",
                is_electric=False,
                is_motorcycle=False,
                vehicle_type=VehicleType.CAR
            )
        }
        self.ui.parking_manager.get_vehicles_in_lot = MagicMock(return_value=mock_vehicles)
        
        # Set input values
        self.ui.details_lot_name_value.set("Test Lot")
        self.ui.details_parking_level_value.set("1")
        
        # Click show details button
        self.ui._handle_show_details()
        
        # Verify details were retrieved
        self.ui.parking_manager.get_vehicles_in_lot.assert_called_once_with("Test Lot", 1)
    
    def test_vehicle_type_selection(self):
        """Test vehicle type selection in the UI"""
        # Test regular car
        self.ui.vehicle_type_value.set("Car")
        self.ui.is_electric_value.set(False)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.CAR)
        
        # Test electric car
        self.ui.vehicle_type_value.set("Car")
        self.ui.is_electric_value.set(True)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.ELECTRIC_CAR)
        
        # Test motorcycle
        self.ui.vehicle_type_value.set("Motorcycle")
        self.ui.is_electric_value.set(False)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.MOTORCYCLE)
        
        # Test electric motorcycle
        self.ui.vehicle_type_value.set("Motorcycle")
        self.ui.is_electric_value.set(True)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.ELECTRIC_MOTORCYCLE)
        
        # Test truck
        self.ui.vehicle_type_value.set("Truck")
        self.ui.is_electric_value.set(False)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.TRUCK)
        
        # Test bus
        self.ui.vehicle_type_value.set("Bus")
        self.ui.is_electric_value.set(False)
        vehicle_type = self.ui._get_vehicle_type()
        self.assertEqual(vehicle_type, VehicleType.BUS)
    
    def test_validation(self):
        """Test input validation in the UI"""
        # Test vehicle data validation
        valid_data = VehicleData(
            registration_number="ABC123",
            manufacturer="Toyota",
            model="Camry",
            color="Red",
            is_electric=False,
            is_motorcycle=False,
            vehicle_type=VehicleType.CAR
        )
        self.assertTrue(self.ui._validate_vehicle_data(valid_data))
        
        # Test invalid vehicle data
        with self.assertRaises(ValueError):
            VehicleData(
                registration_number="",
                manufacturer="",
                model="",
                color="",
                is_electric=False,
                is_motorcycle=False,
                vehicle_type=VehicleType.CAR
            )
        
        # Test lot data validation
        valid_lot_data = ParkingLotData(
            name="Test Lot",
            levels=[
                ParkingLevelData(
                    level_number=1,
                    regular_slots=5,
                    electric_slots=2,
                    motorcycle_slots=1,
                    ev_motorcycle_slots=1
                )
            ]
        )
        self.assertTrue(self.ui._validate_lot_data(valid_lot_data))
        
        # Test invalid lot data
        with self.assertRaises(ValueError):
            ParkingLotData(
                name="",
                levels=[
                    ParkingLevelData(
                        level_number=1,
                        regular_slots=0,
                        electric_slots=-1,
                        motorcycle_slots=-1,
                        ev_motorcycle_slots=-1
                    )
                ]
            )
    
    def test_error_handling(self):
        """Test error handling in the UI"""
        # Test invalid lot creation
        self.ui.lot_name_value.set("")  # Empty lot name
        self.ui._handle_create_lot()
        self.assertIn("invalid literal for int()", self.ui.message_area.get("1.0", "end"))
        
        # Test invalid vehicle parking
        self.ui.registration_number_value.set("")  # Empty registration
        self.ui._handle_park()
        self.assertIn("Registration number is required", self.ui.message_area.get("1.0", "end"))
        
        # Test invalid vehicle removal
        with patch.object(self.ui, '_get_selected_slot', return_value=None):
            self.ui._handle_remove()
            self.assertIn("No slot selected", self.ui.message_area.get("1.0", "end"))
    
    def test_ui_updates(self):
        """Test UI updates after operations"""
        # Mock the parking manager
        self.ui.parking_manager.get_lot_names = MagicMock(return_value=["Test Lot"])
        self.ui.parking_manager.get_levels_for_lot = MagicMock(return_value=[1])
        
        # Create a lot
        self.ui.lot_name_value.set("Test Lot")
        self.ui.parking_level_value.set("1")
        self.ui.regular_slots_value.set("5")
        self.ui.electric_vehicle_slots_value.set("2")
        self.ui._handle_create_lot()
        
        # Verify UI updates
        self.assertEqual(tuple(self.ui.park_lot_combo['values']), ("Test Lot",))
        self.assertEqual(tuple(self.ui.park_level_combo['values']), ("1",))
        self.assertEqual(tuple(self.ui.details_lot_combo['values']), ("Test Lot",))
        self.assertEqual(tuple(self.ui.details_level_combo['values']), ("1",))

if __name__ == '__main__':
    unittest.main()
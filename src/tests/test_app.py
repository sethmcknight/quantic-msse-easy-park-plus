"""
Unit tests for the parking management system core functionality.

This module contains unit tests that verify the correct functionality
of the Vehicle classes, ParkingLot operations, and basic system components.
"""

import unittest
import sys
from unittest.mock import MagicMock

# Prevent GUI initialization during testing by mocking tkinter modules
# This prevents tests from hanging when GUI components are imported
if 'tkinter' not in sys.modules:
    sys.modules['tkinter'] = MagicMock()
if 'tkinter.ttk' not in sys.modules:
    sys.modules['tkinter.ttk'] = MagicMock()
if 'tkinter.messagebox' not in sys.modules:
    sys.modules['tkinter.messagebox'] = MagicMock()

from Vehicle import VehicleType, create_vehicle
from ParkingManager import ParkingLot

class TestVehicle(unittest.TestCase):
    """Test cases for Vehicle class and factory functions."""
    def test_vehicle_attributes(self):
        """Test that vehicle attributes are correctly set during creation."""
        v = create_vehicle("ABC123", "Toyota", "Camry", "Red", VehicleType.CAR, False)
        self.assertEqual(v.manufacturer, "Toyota")
        self.assertEqual(v.model, "Camry")
        self.assertEqual(v.color, "Red")
        self.assertEqual(v.registration_number, "ABC123")
        self.assertEqual(v.vehicle_type, VehicleType.CAR)
        self.assertFalse(v.is_electric)

    def test_car_type(self):
        """Test that car type is correctly identified."""
        c = create_vehicle("DEF456", "Honda", "Civic", "Blue", VehicleType.CAR, False)
        self.assertEqual(c.get_type(), "car")

    def test_truck_type(self):
        t = create_vehicle("GHI789", "Ford", "F-150", "Black", VehicleType.TRUCK, False)
        self.assertEqual(t.get_type(), "truck")

    def test_motorcycle_type(self):
        m = create_vehicle("JKL012", "Yamaha", "YZF", "Yellow", VehicleType.MOTORCYCLE, False)
        self.assertEqual(m.get_type(), "motorcycle")

    def test_bus_type(self):
        b = create_vehicle("MNO345", "Mercedes", "Sprinter", "White", VehicleType.BUS, False)
        self.assertEqual(b.get_type(), "bus")

class TestElectricVehicle(unittest.TestCase):
    def test_electric_car_attributes(self):
        electric_vehicle = create_vehicle("EV123", "Tesla", "Model 3", "White", VehicleType.CAR, True)
        self.assertEqual(electric_vehicle.manufacturer, "Tesla")
        self.assertEqual(electric_vehicle.model, "Model 3")
        self.assertEqual(electric_vehicle.color, "White")
        self.assertEqual(electric_vehicle.registration_number, "EV123")
        # Electric vehicles should have a random initial charge between 20-100%
        charge = electric_vehicle.get_battery_charge()
        self.assertIsNotNone(charge)
        if charge is not None:
            self.assertGreaterEqual(charge, 20.0)
            self.assertLessEqual(charge, 100.0)
        electric_vehicle.set_battery_charge(80)
        self.assertEqual(electric_vehicle.get_battery_charge(), 80)
        self.assertTrue(electric_vehicle.is_electric)
        self.assertEqual(electric_vehicle.vehicle_type, VehicleType.CAR)

    def test_electric_car_type(self):
        ec = create_vehicle("EV456", "Nissan", "Leaf", "Green", VehicleType.CAR, True)
        self.assertEqual(ec.get_type(), "electric_car")

    def test_electric_motorcycle_type(self):
        em = create_vehicle("EV789", "Zero", "SR/F", "Black", VehicleType.MOTORCYCLE, True)
        self.assertEqual(em.get_type(), "electric_motorcycle")

class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.lot = ParkingLot("TestLot")
        # Add a level with 3 regular slots and 1 electric slot
        self.lot.add_level(1, 3, 1)

    def test_park_regular_and_ev(self):
        # Create vehicles
        regular_car = create_vehicle("REG1", "Toyota", "Corolla", "Red", VehicleType.CAR, False)
        electric_car = create_vehicle("EV1", "Tesla", "Model S", "Blue", VehicleType.CAR, True)
        motorcycle = create_vehicle("REG2", "Honda", "CBR", "Black", VehicleType.MOTORCYCLE, False)
        electric_car2 = create_vehicle("EV2", "Nissan", "Leaf", "Green", VehicleType.CAR, True)
        
        # Park regular car - should go to slot 1 (first regular slot)
        slot = self.lot.park_vehicle(1, regular_car)
        self.assertEqual(slot, 1)
        
        # Park EV car - should go to slot 4 (the electric slot)
        slot_ev = self.lot.park_vehicle(1, electric_car)
        self.assertEqual(slot_ev, 4)
        
        # Park regular motorcycle - should go to slot 2 (second regular slot)
        slot2 = self.lot.park_vehicle(1, motorcycle)
        self.assertEqual(slot2, 2)
        
        # Try to park another electric car - electric slot is full, should return None
        slot3 = self.lot.park_vehicle(1, electric_car2)
        self.assertIsNone(slot3)
        
        # Park another regular car in slot 3 (third regular slot)
        regular_car2 = create_vehicle("REG3", "Ford", "Focus", "White", VehicleType.CAR, False)
        slot4 = self.lot.park_vehicle(1, regular_car2)
        self.assertEqual(slot4, 3)
        
        # Try to park another regular car when all slots are full - should return None
        regular_car3 = create_vehicle("REG4", "Honda", "Civic", "Silver", VehicleType.CAR, False)
        slot5 = self.lot.park_vehicle(1, regular_car3)
        self.assertIsNone(slot5)

    def test_remove_vehicle(self):
        # Park a vehicle
        regular_car = create_vehicle("REG1", "Toyota", "Corolla", "Red", VehicleType.CAR, False)
        slot = self.lot.park_vehicle(1, regular_car)
        self.assertIsNotNone(slot)
        
        if slot is not None:
            # Remove the vehicle
            removed_vehicle = self.lot.remove_vehicle(1, slot)
            self.assertIsNotNone(removed_vehicle)
            if removed_vehicle is not None:
                self.assertEqual(removed_vehicle.registration_number, "REG1")
            
            # Try to remove from same slot again - should return None
            removed_again = self.lot.remove_vehicle(1, slot)
            self.assertIsNone(removed_again)

    def test_get_vehicle(self):
        # Park a vehicle
        regular_car = create_vehicle("REG1", "Toyota", "Corolla", "Red", VehicleType.CAR, False)
        slot = self.lot.park_vehicle(1, regular_car)
        self.assertIsNotNone(slot)
        
        if slot is not None:
            # Get the vehicle
            retrieved_vehicle = self.lot.get_vehicle(1, slot)
            self.assertIsNotNone(retrieved_vehicle)
            if retrieved_vehicle is not None:
                self.assertEqual(retrieved_vehicle.registration_number, "REG1")

    def test_status(self):
        # Park some vehicles
        regular_car = create_vehicle("REG1", "Toyota", "Corolla", "Red", VehicleType.CAR, False)
        electric_car = create_vehicle("EV1", "Tesla", "Model S", "Blue", VehicleType.CAR, True)
        
        self.lot.park_vehicle(1, regular_car)
        self.lot.park_vehicle(1, electric_car)
        
        # Get status
        status = self.lot.get_status()
        self.assertEqual(len(status), 1)  # One level
        self.assertEqual(status[0].level, 1)
        
        # Check that we have vehicles parked
        occupied_slots = [slot for slot in status[0].slots if slot.is_occupied]
        self.assertEqual(len(occupied_slots), 2)

if __name__ == "__main__":
    unittest.main()

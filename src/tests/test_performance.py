"""
Performance tests for the Parking Management System

This module contains tests that verify system performance under various loads
without modifying system functionality.
"""

import unittest
import tkinter as tk
import time
import sys
import os
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ParkingLotUI import ParkingLotUI
from models import ParkingLotData, ParkingLevelData, ParkingSlotData, SlotType, VehicleType

class TestParkingSystemPerformance(unittest.TestCase):
    """Performance tests for the parking system"""
    
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
        
        # Create a large test parking lot
        slots = []
        # Add regular slots
        for i in range(1, 101):
            slots.append(ParkingSlotData(
                slot_number=i,
                is_occupied=False,
                slot_type=SlotType.REGULAR,
                level=1,
                lot_name="Performance Test Lot"
            ))
        # Add electric slots
        for i in range(101, 121):
            slots.append(ParkingSlotData(
                slot_number=i,
                is_occupied=False,
                slot_type=SlotType.ELECTRIC,
                level=1,
                lot_name="Performance Test Lot"
            ))
        
        self.lot_data = ParkingLotData(
            name="Performance Test Lot",
            levels=[ParkingLevelData(
                level=1,
                slots=slots,
                lot_name="Performance Test Lot"
            )]
        )
        self.ui.parking_manager.create_lot(self.lot_data)
    
    def tearDown(self):
        """Clean up test environment"""
        self.root.destroy()
    
    def test_parking_performance(self):
        """Test performance of parking operations"""
        # Measure time to park multiple vehicles
        start_time = time.time()
        
        # Park 50 vehicles
        for i in range(50):
            self.ui.state_manager.registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
            self.ui.state_manager.vehicle_model_value.set("Camry")
            self.ui.state_manager.vehicle_color_value.set("Red")
            self.ui.state_manager.vehicle_type_value.set("Car")
            self.ui.state_manager.is_electric_value.set(False)
            self.ui.state_manager.park_lot_value.set("Performance Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            self.ui._handle_park()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify performance is within acceptable limits
        self.assertLess(total_time, 5.0)  # Should complete within 5 seconds
        
        # Verify all vehicles were parked
        parked_vehicles = self.ui.parking_manager.get_vehicles_in_lot("Performance Test Lot", 1)
        self.assertEqual(len(parked_vehicles), 50)
    
    def test_search_performance(self):
        """Test performance of search operations"""
        # First park some vehicles
        for i in range(50):
            self.ui.state_manager.registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
            self.ui.state_manager.vehicle_model_value.set("Camry")
            self.ui.state_manager.vehicle_color_value.set("Red")
            self.ui.state_manager.vehicle_type_value.set("Car")
            self.ui.state_manager.is_electric_value.set(False)
            self.ui.state_manager.park_lot_value.set("Performance Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            self.ui._handle_park()
        
        # Measure search performance
        start_time = time.time()
        
        # Perform multiple searches
        for i in range(50):
            self.ui.state_manager.search_registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.search_type_value.set("registration")
            self.ui._handle_search()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify performance is within acceptable limits
        self.assertLess(total_time, 5.0)  # Should complete within 5 seconds
    
    def test_ui_responsiveness(self):
        """Test UI responsiveness during operations"""
        # Park vehicles while measuring UI response time
        response_times = []
        
        for i in range(20):
            start_time = time.time()
            
            # Update UI
            self.ui.state_manager.registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
            self.ui.state_manager.vehicle_model_value.set("Camry")
            self.ui.state_manager.vehicle_color_value.set("Red")
            self.ui.state_manager.vehicle_type_value.set("Car")
            self.ui.state_manager.is_electric_value.set(False)
            self.ui.state_manager.park_lot_value.set("Performance Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            
            # Process events to update UI
            self.root.update()
            
            end_time = time.time()
            response_times.append(end_time - start_time)
        
        # Verify UI remains responsive
        avg_response_time = sum(response_times) / len(response_times)
        self.assertLess(avg_response_time, 0.1)  # Average response time should be under 100ms
    
    def test_memory_usage(self):
        """Test memory usage during operations"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform operations
        for i in range(100):
            self.ui.state_manager.registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.vehicle_manufacturer_value.set("Toyota")
            self.ui.state_manager.vehicle_model_value.set("Camry")
            self.ui.state_manager.vehicle_color_value.set("Red")
            self.ui.state_manager.vehicle_type_value.set("Car")
            self.ui.state_manager.is_electric_value.set(False)
            self.ui.state_manager.park_lot_value.set("Performance Test Lot")
            self.ui.state_manager.park_level_value.set("1")
            self.ui._handle_park()
            
            # Search for the vehicle
            self.ui.state_manager.search_registration_number_value.set(f"ABC{i}")
            self.ui.state_manager.search_type_value.set("registration")
            self.ui._handle_search()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage is within acceptable limits
        self.assertLess(memory_increase, 50 * 1024 * 1024)  # Should use less than 50MB additional memory

if __name__ == "__main__":
    unittest.main() 
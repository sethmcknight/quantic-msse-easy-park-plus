"""
Parking Lot UI Module

This module provides a graphical user interface for the parking lot management system.

[DEBUG LOGGING]
This module contains temporary debug logging statements that should be removed before final submission.
These logs help track:
- Data flow between UI and parking lot manager
- State changes in the parking lot
- User input validation
- Search and display operations

To remove debug logging:
1. Remove all print statements starting with [DEBUG]
2. Remove this debug logging section from the docstring
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Optional, Union
from Vehicle import Vehicle, ElectricVehicle, Motorcycle
from ParkingManager import ParkingLot
from models import VehicleData, SearchCriteria, ParkingLotData
from interfaces import ParkingLotObserver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParkingLotUI(ParkingLotObserver):
    """Class representing the parking lot UI"""
    
    def __init__(self):
        """Initialize the UI"""
        self.parking_lot = ParkingLot()
        self.parking_lot.register_observer(self)
        # Create main window
        self.main_window = tk.Tk()  # Renamed from self.root
        self.main_window.title("Parking Lot Management System")
        # Initialize UI state
        self._init_state()
        # Create and layout widgets
        self._create_widgets()
        self._layout_widgets()
        # Initialize dropdowns
        # self._update_lot_names()
        # self._update_levels()

    def _init_state(self):
        """Initialize UI state variables"""
        # Admin tab variables
        self.lot_name_value = tk.StringVar()
        self.parking_level_value = tk.StringVar()
        self.regular_slots_value = tk.StringVar()
        self.electric_vehicle_slots_value = tk.StringVar()
        # Vehicle Operations variables
        self.registration_number_value = tk.StringVar()
        self.vehicle_manufacturer_value = tk.StringVar()
        self.vehicle_model_value = tk.StringVar()
        self.vehicle_color_value = tk.StringVar()
        self.vehicle_type_value = tk.StringVar(value="Car")
        self.is_electric_value = tk.BooleanVar()
        self.park_lot_value = tk.StringVar()
        self.park_level_value = tk.StringVar()
        # Search tab variables
        self.search_registration_number_value = tk.StringVar()
        self.search_vehicle_color_value = tk.StringVar()
        self.search_vehicle_manufacturer_value = tk.StringVar()
        self.search_vehicle_model_value = tk.StringVar()
        self.search_type_value = tk.StringVar(value="registration")
        self.search_value_value = tk.StringVar()
        # Details tab variables
        self.details_lot_name_value = tk.StringVar()
        self.details_parking_level_value = tk.StringVar()
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_window)
        
        # Create tabs
        self.vehicle_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        self.admin_tab = ttk.Frame(self.notebook)
        self.details_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.vehicle_tab, text="Vehicle Operations")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.add(self.admin_tab, text="Parking Lot Admin")
        self.notebook.add(self.details_tab, text="Lot Details")
        
        # Create vehicle operations frame
        self.vehicle_frame = ttk.LabelFrame(self.vehicle_tab, text="Vehicle Operations")
        self._create_vehicle_widgets()
        
        # Create search frame
        self.search_frame = ttk.LabelFrame(self.search_tab, text="Search")
        self._create_search_widgets()
        
        # Create admin frame
        self.admin_frame = ttk.LabelFrame(self.admin_tab, text="Parking Lot Administration")
        self._create_admin_widgets()
        
        # Create details frame
        self.details_frame = ttk.LabelFrame(self.details_tab, text="Lot Details")
        self._create_details_widgets()
        
        # Create results tree
        self._create_results_tree()
        
        # Create message area
        self.message_area = tk.Text(self.main_window, height=10, width=50)
    
    def _create_vehicle_widgets(self):
        """Create widgets for vehicle operations"""
        # Create lot selection frame
        self.park_lot_frame = ttk.Frame(self.vehicle_frame)
        self.park_lot_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Create lot selection widgets
        self.park_lot_label = ttk.Label(self.park_lot_frame, text="Lot Name:")
        self.park_lot_combo = ttk.Combobox(self.park_lot_frame, textvariable=self.park_lot_value, state="readonly")
        
        self.park_level_label = ttk.Label(self.park_lot_frame, text="Level:")
        self.park_level_combo = ttk.Combobox(self.park_lot_frame, textvariable=self.park_level_value, state="readonly")
        
        # Layout lot selection widgets
        self.park_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.park_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.park_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.park_level_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Create vehicle input widgets
        self.registration_label = ttk.Label(self.vehicle_frame, text="Registration Number:")
        self.registration_entry = ttk.Entry(self.vehicle_frame, textvariable=self.registration_number_value)
        self.manufacturer_label = ttk.Label(self.vehicle_frame, text="Manufacturer:")
        self.manufacturer_entry = ttk.Entry(self.vehicle_frame, textvariable=self.vehicle_manufacturer_value)
        self.model_label = ttk.Label(self.vehicle_frame, text="Model:")
        self.model_entry = ttk.Entry(self.vehicle_frame, textvariable=self.vehicle_model_value)
        self.color_label = ttk.Label(self.vehicle_frame, text="Color:")
        self.color_entry = ttk.Entry(self.vehicle_frame, textvariable=self.vehicle_color_value)
        self.vehicle_type_label = ttk.Label(self.vehicle_frame, text="Vehicle Type:")
        self.vehicle_type_combo = ttk.Combobox(self.vehicle_frame, textvariable=self.vehicle_type_value, state="readonly",
                                               values=["Car", "Truck", "Bus", "Motorcycle"])
        self.electric_vehicle_check = ttk.Checkbutton(self.vehicle_frame, text="Electric Vehicle", variable=self.is_electric_value)
        self.park_button = ttk.Button(self.vehicle_frame, text="Park", command=self._handle_park)
        self.remove_button = ttk.Button(self.vehicle_frame, text="Remove", command=self._handle_remove)
        
        # Layout vehicle input widgets
        self.registration_label.grid(row=1, column=0, padx=5, pady=5)
        self.registration_entry.grid(row=1, column=1, padx=5, pady=5)
        self.manufacturer_label.grid(row=2, column=0, padx=5, pady=5)
        self.manufacturer_entry.grid(row=2, column=1, padx=5, pady=5)
        self.model_label.grid(row=3, column=0, padx=5, pady=5)
        self.model_entry.grid(row=3, column=1, padx=5, pady=5)
        self.color_label.grid(row=4, column=0, padx=5, pady=5)
        self.color_entry.grid(row=4, column=1, padx=5, pady=5)
        self.vehicle_type_label.grid(row=5, column=0, padx=5, pady=5)
        self.vehicle_type_combo.grid(row=5, column=1, padx=5, pady=5)
        self.electric_vehicle_check.grid(row=6, column=0, padx=5, pady=5)
        self.park_button.grid(row=7, column=0, padx=5, pady=5)
        self.remove_button.grid(row=7, column=1, padx=5, pady=5)
        
        # Update lot names in combo box
        self._update_park_lot_names()
    
    def _create_search_widgets(self):
        """Create widgets for search operations"""
        self.search_registration_label = ttk.Label(self.search_frame, text="Registration:")
        self.search_registration_entry = ttk.Entry(self.search_frame, textvariable=self.search_registration_number_value)
        self.search_color_label = ttk.Label(self.search_frame, text="Color:")
        self.search_color_entry = ttk.Entry(self.search_frame, textvariable=self.search_vehicle_color_value)
        self.search_manufacturer_label = ttk.Label(self.search_frame, text="Manufacturer:")
        self.search_manufacturer_entry = ttk.Entry(self.search_frame, textvariable=self.search_vehicle_manufacturer_value)
        self.search_model_label = ttk.Label(self.search_frame, text="Model:")
        self.search_model_entry = ttk.Entry(self.search_frame, textvariable=self.search_vehicle_model_value)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self._handle_search)
        self.show_status_button = ttk.Button(self.search_frame, text="Show Full Status", command=self._handle_show_status)
    
    def _create_admin_widgets(self):
        """Create admin tab widgets"""
        # Create admin widgets
        self.lot_name_label = ttk.Label(self.admin_frame, text="Lot Name:")
        self.lot_name_entry = ttk.Entry(self.admin_frame, textvariable=self.lot_name_value)
        self.level_label = ttk.Label(self.admin_frame, text="Level:")
        self.level_entry = ttk.Entry(self.admin_frame, textvariable=self.parking_level_value)
        self.num_label = ttk.Label(self.admin_frame, text="Number of Regular Slots:")
        self.num_entry = ttk.Entry(self.admin_frame, textvariable=self.regular_slots_value)
        self.electric_vehicle_num_label = ttk.Label(self.admin_frame, text="Number of Electric Vehicle Slots:")
        self.electric_vehicle_num_entry = ttk.Entry(self.admin_frame, textvariable=self.electric_vehicle_slots_value)
        self.create_button = ttk.Button(self.admin_frame, text="Create Parking Lot", command=self._handle_create_lot)
        self.status_button = ttk.Button(self.admin_frame, text="Show Full Status", command=self._handle_show_status)
        self.show_lots_button = ttk.Button(self.admin_frame, text="Show All Lots", command=self._handle_show_lots)
        
        # Create admin results tree
        self.admin_tree = ttk.Treeview(self.admin_tab, columns=("Lot Name", "Levels", "Regular Capacity", "EV Capacity", "Available Regular", "Available EV"),
                                     show="headings")
        self.admin_tree.heading("Lot Name", text="Lot Name")
        self.admin_tree.heading("Levels", text="Levels")
        self.admin_tree.heading("Regular Capacity", text="Regular Capacity")
        self.admin_tree.heading("EV Capacity", text="EV Capacity")
        self.admin_tree.heading("Available Regular", text="Available Regular")
        self.admin_tree.heading("Available EV", text="Available EV")
    
    def _create_details_widgets(self):
        """Create widgets for lot details view"""
        # Create lot selection frame
        self.details_select_frame = ttk.Frame(self.details_frame)
        self.details_select_frame.pack(fill="x", padx=5, pady=5)
        
        # Create lot selection widgets
        self.details_lot_label = ttk.Label(self.details_select_frame, text="Lot Name:")
        self.details_lot_combo = ttk.Combobox(self.details_select_frame, textvariable=self.details_lot_name_value, state="readonly")
        
        self.details_level_label = ttk.Label(self.details_select_frame, text="Level:")
        self.details_level_combo = ttk.Combobox(self.details_select_frame, textvariable=self.details_parking_level_value, state="readonly")
        
        self.details_show_button = ttk.Button(self.details_select_frame, text="Show Details", command=self._handle_show_details)
        
        # Layout selection widgets
        self.details_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.details_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.details_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.details_level_combo.grid(row=0, column=3, padx=5, pady=5)
        self.details_show_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Create details tree
        self.details_tree = ttk.Treeview(self.details_frame, 
                                       columns=("Level", "Slot", "Registration", "Manufacturer", "Model", "Color", "Slot Type", "Vehicle Type", "Charge Status"),
                                       show="headings")
        
        # Configure tree columns
        column_widths = {
            "Level": 60,
            "Slot": 60,
            "Registration": 100,
            "Manufacturer": 100,
            "Model": 100,
            "Color": 80,
            "Slot Type": 80,
            "Vehicle Type": 100,
            "Charge Status": 80
        }
        
        for col, width in column_widths.items():
            self.details_tree.heading(col, text=col)
            self.details_tree.column(col, width=width, anchor="center")
        
        # Layout details tree
        self.details_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Update lot names in combo box
        self._update_details_lot_names()
    
    def _create_results_tree(self):
        """Create the results tree view"""
        self.results_tree = ttk.Treeview(self.search_tab, columns=("Slot", "Registration", "Manufacturer", "Model", "Color", "Slot Type", "Vehicle Type", "Charge Status"),
                                       show="headings")
        self.results_tree.heading("Slot", text="Slot")
        self.results_tree.heading("Registration", text="Registration")
        self.results_tree.heading("Manufacturer", text="Manufacturer")
        self.results_tree.heading("Model", text="Model")
        self.results_tree.heading("Color", text="Color")
        self.results_tree.heading("Slot Type", text="Slot Type")
        self.results_tree.heading("Vehicle Type", text="Vehicle Type")
        self.results_tree.heading("Charge Status", text="Charge Status")
    
    def _handle_park(self):
        """Handle park vehicle button click"""
        try:
            # Get selected lot and level
            lot_name = self.park_lot_value.get()
            level = int(self.park_level_value.get())
            
            if not lot_name:
                self._show_error("Please select a lot")
                return
            
            data = VehicleData(
                registration_number=self.registration_number_value.get(),  # Updated from registration
                manufacturer=self.vehicle_manufacturer_value.get(),
                model=self.vehicle_model_value.get(),
                color=self.vehicle_color_value.get(),
                is_electric=self.is_electric_value.get(),
                is_motorcycle=self.vehicle_type_value.get() == "Motorcycle"
            )
            
            if not self._validate_vehicle_data(data):
                return
            
            slot = self.parking_lot.park(
                data.registration_number,
                data.manufacturer,
                data.model,
                data.color,
                data.is_electric,
                data.is_motorcycle,
                lot_name,
                level
            )
            
            if slot is not None:
                self._show_message(f"Vehicle parked in slot {slot} of {lot_name} level {level}")
                self._clear_park_fields()
            else:
                self._show_error("No available slots in the selected lot and level")
        
        except Exception as e:
            logger.error(f"Error parking vehicle: {e}")
            self._show_error("Error parking vehicle")
    
    def _handle_remove(self):
        """Handle remove vehicle button click"""
        try:
            slot = self._get_selected_slot()
            if slot is None:
                self._show_error("Please select a slot to remove")
                return
            
            if self.parking_lot.leave(slot):
                self._show_message(f"Vehicle removed from slot {slot}")
            else:
                self._show_error("Error removing vehicle")
        
        except Exception as e:
            logger.error(f"Error removing vehicle: {e}")
            self._show_error("Error removing vehicle")
    
    def _handle_search(self):
        """Handle search button click"""
        try:
            criteria = SearchCriteria(
                registration=self.search_registration_number_value.get(),  # Updated from registration
                color=self.search_vehicle_color_value.get(),
                manufacturer=self.search_vehicle_manufacturer_value.get(),
                model=self.search_vehicle_model_value.get(),
                search_type=self.search_type_value.get()
            )
            
            self._perform_search(criteria)
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            self._show_error("Error performing search")
    
    def _handle_create_lot(self):
        """Handle create lot button click"""
        try:
            # Get values from entry fields
            lot_name = self.lot_name_value.get().strip()
            level_str = self.parking_level_value.get().strip()
            num_str = self.regular_slots_value.get().strip()
            ev_num_str = self.electric_vehicle_slots_value.get().strip()
            
            # Validate inputs
            if not lot_name:
                self._show_error("Please enter a lot name")
                return
            if not level_str:
                self._show_error("Please enter a level")
                return
            if not num_str:
                self._show_error("Please enter number of regular slots")
                return
            if not ev_num_str:
                self._show_error("Please enter number of electric vehicle slots")
                return
            
            try:
                level = int(level_str)
                num = int(num_str)
                ev_num = int(ev_num_str)
            except ValueError:
                self._show_error("Invalid numeric value")
                return
            
            # Create parking lot data
            data = ParkingLotData(
                name=lot_name,
                level=level,
                regular_slots=num,
                electric_vehicle_slots=ev_num
            )
            
            # Validate lot data
            if not self._validate_lot_data(data):
                return
            
            # Create parking lot
            self.parking_lot.create_parking_lot(data)
            
            # Show success message
            self._show_message(f"Created parking lot '{lot_name}' with {num} regular slots and {ev_num} electric vehicle slots on level {level}")
            
            # Clear input fields
            self.lot_name_value.set("")
            self.parking_level_value.set("")
            self.regular_slots_value.set("")
            self.electric_vehicle_slots_value.set("")
            
            # Update lot names in combo boxes
            self._update_details_lot_names()
            self._update_park_lot_names()
            
        except Exception as e:
            logger.error(f"Error creating parking lot: {e}")
            self._show_error("Error creating parking lot")
    
    def _handle_show_status(self):
        """Handle show status button click"""
        try:
            # Clear previous results
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Get all vehicles in the lot
            vehicles = self.parking_lot.get_vehicles_in_lot("Main", 1)  # Use default values
            for slot_number, vehicle in vehicles.items():
                self._add_vehicle_to_tree(vehicle, slot_number)
            
            # Also show status message
            status = self.parking_lot.get_status()
            self._show_message(status)
            if not self.results_tree.get_children():
                self._show_message("No vehicles found in the parking lot.")
        except Exception as e:
            logger.error(f"Error showing status: {e}")
            self._show_error("Error getting status")
    
    def _handle_show_lots(self):
        """Handle show all lots button click"""
        try:
            # Clear previous results
            self.admin_tree.delete(*self.admin_tree.get_children())
            
            # Configure column widths
            column_widths = {
                "Lot Name": 150,
                "Levels": 80,
                "Regular Capacity": 120,
                "EV Capacity": 120,
                "Available Regular": 120,
                "Available EV": 120
            }
            
            for col, width in column_widths.items():
                self.admin_tree.column(col, width=width, anchor="center")
            
            # Get all lot names
            lot_names = self.parking_lot.get_lot_names()
            
            for lot_name in lot_names:
                # Get levels for this lot
                levels = self.parking_lot.get_levels_for_lot(lot_name)
                
                # Initialize counters for this lot
                total_regular_capacity = 0
                total_ev_capacity = 0
                occupied_regular = 0
                occupied_ev = 0
                
                for level in levels:
                    # Get vehicles in this level
                    vehicles = self.parking_lot.get_vehicles_in_lot(lot_name, level)
                    
                    # Count occupied slots by type
                    for vehicle in vehicles.values():
                        if isinstance(vehicle, ElectricVehicle):
                            occupied_ev += 1
                        else:
                            occupied_regular += 1
                    
                    # Get the level object to determine capacity
                    level_obj = next((l for l in self.parking_lot.levels if l.level == level and l.name == lot_name), None)
                    if level_obj:
                        total_regular_capacity += len(level_obj.regular_slots)
                        total_ev_capacity += len(level_obj.electric_vehicle_slots)
                
                # Calculate available slots
                available_regular = total_regular_capacity - occupied_regular
                available_ev = total_ev_capacity - occupied_ev
                
                # Add lot information to tree
                values = (
                    lot_name,
                    len(levels),
                    total_regular_capacity,
                    total_ev_capacity,
                    available_regular,
                    available_ev
                )
                
                self.admin_tree.insert("", "end", values=values)
            
            if not self.admin_tree.get_children():
                self._show_message("No parking lots found.")
                
        except Exception as e:
            logger.error(f"Error showing lots: {e}")
            self._show_error("Error showing lots information")
    
    def _validate_vehicle_data(self, data: VehicleData) -> bool:
        """Validate vehicle data"""
        if not data.registration_number:
            self._show_error("Please enter registration number")
            return False
        if not data.manufacturer:
            self._show_error("Please enter manufacturer")
            return False
        if not data.model:
            self._show_error("Please enter model")
            return False
        if not data.color:
            self._show_error("Please enter color")
            return False
        return True
    
    def _validate_lot_data(self, data: ParkingLotData) -> bool:
        """Validate parking lot data"""
        if not data.name:
            self._show_error("Please enter a lot name")
            return False
        if data.regular_slots <= 0:
            self._show_error("Please enter valid numbers")
            return False
        if data.electric_vehicle_slots < 0:
            self._show_error("Please enter valid numbers")
            return False
        return True
    
    def _get_selected_slot(self) -> Optional[int]:
        """Get the selected slot number from the tree view"""
        selection = self.results_tree.selection()
        if not selection:
            return None
        item = self.results_tree.item(selection[0])
        return int(item['values'][0])
    
    def _perform_search(self, criteria: SearchCriteria):
        """Perform search based on criteria"""
        # Clear previous results
        self.results_tree.delete(*self.results_tree.get_children())
        if criteria.search_type == "registration" and criteria.registration:
            registration_search = criteria.registration.strip().casefold()
            slot = None
            found_vehicle = None
            # Search all lots and levels for a matching registration (case-insensitive, whitespace-insensitive)
            for lot_name in self.parking_lot.get_lot_names():
                for level in self.parking_lot.get_levels_for_lot(lot_name):
                    vehicles = self.parking_lot.get_vehicles_in_lot(lot_name, level)
                    for s, vehicle in vehicles.items():
                        registration_number = vehicle.registration_number
                        if registration_number is None:
                            registration_number = vehicle.registration_number
                        registration_number = registration_number.strip().casefold() if registration_number else ""
                        if registration_number == registration_search:
                            slot = s
                            found_vehicle = vehicle
                            break
                    if slot is not None:
                        break
                if slot is not None:
                    break
            if slot is not None and found_vehicle is not None:
                self._add_vehicle_to_tree(found_vehicle, slot)
        elif criteria.search_type == "color" and criteria.color:
            slots = self.parking_lot.get_slots_by_color(criteria.color.strip())
            for slot in slots:
                vehicle = self.parking_lot.get_vehicle(slot)
                if vehicle:
                    self._add_vehicle_to_tree(vehicle, slot)
        elif criteria.search_type == "manufacturer" and criteria.manufacturer:
            slots: list[int] = self.parking_lot.get_slots_by_manufacturer(criteria.manufacturer.strip())
            for slot in slots:
                vehicle = self.parking_lot.get_vehicle(slot)
                if vehicle:
                    self._add_vehicle_to_tree(vehicle, slot)
        elif criteria.search_type == "model" and criteria.model:
            slots = self.parking_lot.get_slots_by_model(criteria.model.strip())
            for slot in slots:
                vehicle = self.parking_lot.get_vehicle(slot)
                if vehicle:
                    self._add_vehicle_to_tree(vehicle, slot)
    
    def _add_vehicle_to_tree(self, vehicle: Union[Vehicle, VehicleData], slot: int) -> None:
        """Add a vehicle to the results tree (supports both Vehicle and VehicleData)"""
        # Get vehicle attributes
        if isinstance(vehicle, Vehicle):
            registration_number = vehicle.registration_number
            manufacturer = vehicle.vehicle_manufacturer
            model = vehicle.model
            color = vehicle.color
            is_ev = isinstance(vehicle, ElectricVehicle)
            is_motorcycle = isinstance(vehicle, Motorcycle)
            charge_status = f"{vehicle.current_battery_charge}%" if is_ev and hasattr(vehicle, "current_battery_charge") else "N/A"  # Updated to use renamed attribute
        else:  # VehicleData
            registration_number = vehicle.registration_number
            manufacturer = vehicle.manufacturer
            model = vehicle.model
            color = vehicle.color
            is_ev = vehicle.is_electric
            is_motorcycle = vehicle.is_motorcycle
            charge_status = "N/A"  # VehicleData doesn't have charge info

        vehicle_type = (
            "EV Motorcycle" if is_ev and is_motorcycle else
            "EV" if is_ev else
            "Motorcycle" if is_motorcycle else "Standard"
        )

        self.results_tree.insert("", "end", values=(
            str(slot),
            str(registration_number),
            str(manufacturer),
            str(model),
            str(color),
            "EV" if is_ev else "Standard",
            vehicle_type,
            str(charge_status)
        ))
    
    def _clear_park_fields(self):
        """Clear vehicle input fields"""
        self.registration_number_value.set("")
        self.vehicle_manufacturer_value.set("")
        self.vehicle_model_value.set("")
        self.vehicle_color_value.set("")
        self.vehicle_type_value.set("Car")
        self.is_electric_value.set(False)
    
    def _show_message(self, message: str):
        """Show a message in the message area"""
        self.message_area.insert("end", f"{message}\n")
        self.message_area.see("end")
    
    def _show_error(self, message: str):
        """Show an error message"""
        self._show_message(message)
    
    def update(self, message: str):
        """Handle updates from the parking lot"""
        self._show_message(message)
    
    def run(self):
        """Run the UI"""
        self.main_window.mainloop()

    def _layout_widgets(self):
        """Layout UI widgets"""
        # Layout notebook
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout vehicle frame
        self.vehicle_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.park_lot_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.park_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.park_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.park_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.park_level_combo.grid(row=0, column=3, padx=5, pady=5)
        self.registration_label.grid(row=1, column=0, padx=5, pady=5)
        self.registration_entry.grid(row=1, column=1, padx=5, pady=5)
        self.manufacturer_label.grid(row=2, column=0, padx=5, pady=5)
        self.manufacturer_entry.grid(row=2, column=1, padx=5, pady=5)
        self.model_label.grid(row=3, column=0, padx=5, pady=5)
        self.model_entry.grid(row=3, column=1, padx=5, pady=5)
        self.color_label.grid(row=4, column=0, padx=5, pady=5)
        self.color_entry.grid(row=4, column=1, padx=5, pady=5)
        self.vehicle_type_label.grid(row=5, column=0, padx=5, pady=5)
        self.vehicle_type_combo.grid(row=5, column=1, padx=5, pady=5)
        self.electric_vehicle_check.grid(row=6, column=0, padx=5, pady=5)
        self.park_button.grid(row=7, column=0, padx=5, pady=5)
        self.remove_button.grid(row=7, column=1, padx=5, pady=5)
        
        # Layout search frame
        self.search_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.search_registration_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_registration_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_color_label.grid(row=1, column=0, padx=5, pady=5)
        self.search_color_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_manufacturer_label.grid(row=2, column=0, padx=5, pady=5)
        self.search_manufacturer_entry.grid(row=2, column=1, padx=5, pady=5)
        self.search_model_label.grid(row=3, column=0, padx=5, pady=5)
        self.search_model_entry.grid(row=3, column=1, padx=5, pady=5)
        self.search_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.show_status_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # Layout admin frame
        self.admin_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.lot_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.lot_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.level_label.grid(row=1, column=0, padx=5, pady=5)
        self.level_entry.grid(row=1, column=1, padx=5, pady=5)
        self.num_label.grid(row=2, column=0, padx=5, pady=5)
        self.num_entry.grid(row=2, column=1, padx=5, pady=5)
        self.electric_vehicle_num_label.grid(row=3, column=0, padx=5, pady=5)
        self.electric_vehicle_num_entry.grid(row=3, column=1, padx=5, pady=5)
        self.create_button.grid(row=4, column=0, padx=5, pady=5)
        self.status_button.grid(row=4, column=1, padx=5, pady=5)
        self.show_lots_button.grid(row=4, column=2, padx=5, pady=5)
        
        # Layout details frame
        self.details_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout results tree
        self.results_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout admin tree
        self.admin_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout message area
        self.message_area.pack(expand=True, fill="both", padx=5, pady=5)

    def _show_full_status(self) -> None:
        """Show full status of the parking lot"""
        try:
            selected_lot = self.lot_name_value.get()
            selected_level = int(self.parking_level_value.get())
            print(f"[DEBUG] _show_full_status called with lot={selected_lot}, level={selected_level}")
            
            if not selected_lot:
                self._show_error("Please select a parking lot")
                return
            
            # Clear previous results
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Get all vehicles in the lot
            vehicles: Dict[int, Vehicle] = self.parking_lot.get_vehicles_in_lot(selected_lot, selected_level)
            print(f"[DEBUG] _show_full_status received {len(vehicles)} vehicles")
            for slot_number, vehicle in vehicles.items():
                self._add_vehicle_to_tree(vehicle, slot_number)
            
            if not self.results_tree.get_children():
                self._show_message("No vehicles found in the selected lot and level.")
        
        except Exception as e:
            logger.error(f"Error showing full status: {str(e)}")
            self._show_error(f"Error showing full status: {str(e)}")

    def _show_status(self) -> None:
        """Show parking lot status"""
        status = self.parking_lot.get_status()
        self._show_message(status)

    def create_lot(self):
        """Create a new parking lot"""
        self._handle_create_lot()

    def _update_details_lot_names(self):
        """Update the lot names in the details combo box"""
        lot_names = self.parking_lot.get_lot_names()
        self.details_lot_combo['values'] = lot_names
        if lot_names:
            self.details_lot_combo.set(lot_names[0])
            self._update_details_levels()

    def _update_park_levels(self):
        """Update the levels in the park combo box based on selected lot"""
        lot_name = self.park_lot_value.get()
        if lot_name:
            levels = self.parking_lot.get_levels_for_lot(lot_name)
            self.park_level_combo['values'] = levels
            if levels:
                self.park_level_combo.set(levels[0])

    def _update_details_levels(self):
        """Update the levels in the details combo box based on selected lot"""
        lot_name = self.details_lot_name_value.get()
        if lot_name:
            levels = self.parking_lot.get_levels_for_lot(lot_name)
            self.details_level_combo['values'] = levels
            if levels:
                self.details_level_combo.set(levels[0])

    def _handle_show_details(self):
        """Handle show details button click"""
        try:
            # Clear previous results
            self.details_tree.delete(*self.details_tree.get_children())
            
            # Get selected lot and level
            lot_name = self.details_lot_name_value.get()
            level = int(self.details_parking_level_value.get())
            
            if not lot_name:
                self._show_error("Please select a lot")
                return
            
            # Get vehicles in the lot
            vehicles = self.parking_lot.get_vehicles_in_lot(lot_name, level)
            
            # Add vehicles to tree
            for slot, vehicle in vehicles.items():
                if vehicle:
                    # Get vehicle attributes
                    registration_number = getattr(vehicle, 'registration_number', '')
                    manufacturer = getattr(vehicle, 'manufacturer', '')
                    model = getattr(vehicle, 'model', '')
                    color = getattr(vehicle, 'color', '')
                    is_ev = isinstance(vehicle, ElectricVehicle)
                    is_motorcycle = isinstance(vehicle, Motorcycle)
                    charge_status = f"{getattr(vehicle, 'charge', 'N/A')}%" if is_ev and hasattr(vehicle, 'charge') else "N/A"
                    
                    vehicle_type = (
                        "EV Motorcycle" if is_ev and is_motorcycle else
                        "EV" if is_ev else
                        "Motorcycle" if is_motorcycle else "Standard"
                    )
                    
                    slot_type = "EV" if is_ev else "Standard"
                    
                    values = (
                        level,
                        slot,
                        registration_number,
                        manufacturer,
                        model,
                        color,
                        slot_type,
                        vehicle_type,
                        charge_status
                    )
                    
                    self.details_tree.insert("", "end", values=values)
            
            if not self.details_tree.get_children():
                self._show_message("No vehicles found in the selected lot and level.")
                
        except Exception as e:
            logger.error(f"Error showing details: {e}")
            self._show_error("Error showing lot details")

    def _update_park_lot_names(self):
        """Update the lot names in the park combo box"""
        lot_names = self.parking_lot.get_lot_names()
        self.park_lot_combo['values'] = lot_names
        if lot_names:
            self.park_lot_combo.set(lot_names[0])
            self._update_park_levels()


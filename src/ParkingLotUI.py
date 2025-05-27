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
from ParkingManager import ParkingLotManagerImpl
from models import VehicleData, SearchCriteria, ParkingLotData, ParkingLevelData, VehicleType, SlotType
from interfaces import ParkingLotObserver

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ParkingLotUI(ParkingLotObserver):
    """Class representing the parking lot UI"""
    
    def __init__(self):
        """Initialize the UI"""
        logger.debug("[DEBUG] Initializing ParkingLotUI")
        self.parking_manager = ParkingLotManagerImpl()
        self.parking_manager.register_observer(self)
        # Create main window
        self.main_window = tk.Tk()
        self.main_window.title("Parking Lot Management System")
        # Initialize UI state
        self._init_state()
        # Create and layout widgets
        self._create_widgets()
        self._layout_widgets()
        # Initialize dropdowns
        self._update_park_lot_names()
        self._update_park_levels()
        logger.debug("[DEBUG] ParkingLotUI initialization complete")

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
        
        # Set column widths
        for col in ("Lot Name", "Levels", "Regular Capacity", "EV Capacity", "Available Regular", "Available EV"):
            self.admin_tree.column(col, width=100, anchor="center")
    
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
        
        # Add filter options
        self.details_filter_label = ttk.Label(self.details_select_frame, text="Filter:")
        self.details_filter_value = tk.StringVar(value="All Slots")
        self.details_filter_combo = ttk.Combobox(self.details_select_frame, 
                                               textvariable=self.details_filter_value,
                                               values=["All Slots", "Available Slots", "Occupied Slots", "All Levels"],
                                               state="readonly")
        
        self.details_show_button = ttk.Button(self.details_select_frame, text="Show Details", command=self._handle_show_details)
        
        # Layout selection widgets
        self.details_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.details_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.details_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.details_level_combo.grid(row=0, column=3, padx=5, pady=5)
        self.details_filter_label.grid(row=0, column=4, padx=5, pady=5)
        self.details_filter_combo.grid(row=0, column=5, padx=5, pady=5)
        self.details_show_button.grid(row=0, column=6, padx=5, pady=5)
        
        # Create details tree
        self.details_tree = ttk.Treeview(self.details_frame, 
                                       columns=("Level", "Slot", "Status", "Registration", "Manufacturer", "Model", "Color", "Slot Type", "Vehicle Type", "Charge Status"),
                                       show="headings")
        
        # Configure tree columns
        column_widths = {
            "Level": 60,
            "Slot": 60,
            "Status": 80,
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
        
        # Set column widths
        for col in ("Slot", "Registration", "Manufacturer", "Model", "Color", "Slot Type", "Vehicle Type", "Charge Status"):
            self.results_tree.column(col, width=100, anchor="center")
        
        # Pack the tree
        self.results_tree.pack(expand=True, fill="both", padx=5, pady=5)
    
    def _handle_park(self):
        """Handle park button click"""
        try:
            # Get vehicle data
            data = VehicleData(
                registration_number=self.registration_number_value.get(),
                manufacturer=self.vehicle_manufacturer_value.get(),
                model=self.vehicle_model_value.get(),
                color=self.vehicle_color_value.get(),
                is_electric=self.is_electric_value.get(),
                is_motorcycle=self.vehicle_type_value.get() == "Motorcycle",
                vehicle_type=self._get_vehicle_type()
            )
            
            # Validate data
            if not self._validate_vehicle_data(data):
                return
            
            # Get lot and level
            lot_name = self.park_lot_value.get()
            level = int(self.park_level_value.get())
            
            # Park vehicle
            slot = self.parking_manager.park_vehicle(lot_name, level, data)
            if slot is not None:
                self._show_message(f"Vehicle parked in slot {slot}")
                self._clear_park_fields()
            else:
                self._show_error("Failed to park vehicle")
            
        except ValueError as e:
            self._show_error(str(e))
    
    def _handle_remove(self):
        """Handle remove button click"""
        try:
            slot = self._get_selected_slot()
            if slot is None:
                self._show_error("No slot selected")
                return
            lot_name = self.park_lot_value.get()
            level = int(self.park_level_value.get())
            vehicle = self.parking_manager.remove_vehicle(lot_name, level, slot)
            if vehicle:
                self._show_message(f"Removed vehicle {vehicle.registration_number} from slot {slot}")
            else:
                self._show_error("No vehicle found in selected slot")
        except ValueError as e:
            self._show_error(str(e))
    
    def _handle_search(self):
        """Handle search button click"""
        try:
            criteria = SearchCriteria(
                registration_number=self.search_registration_number_value.get(),
                color=self.search_vehicle_color_value.get(),
                manufacturer=self.search_vehicle_manufacturer_value.get(),
                model=self.search_vehicle_model_value.get(),
                # Do not include search_type, as it's not a field in SearchCriteria
            )
            self._perform_search(criteria)
        except Exception as e:
            logger.error(f"Error searching: {e}")
            self._show_error("Error performing search")
    
    def _handle_create_lot(self):
        """Handle create lot button click"""
        try:
            # Get lot data
            lot_name = self.lot_name_value.get()
            level = int(self.parking_level_value.get())
            regular_slots = int(self.regular_slots_value.get())
            electric_slots = int(self.electric_vehicle_slots_value.get())
            # Create level data
            level_data = ParkingLevelData(
                level_number=level,
                regular_slots=regular_slots,
                electric_slots=electric_slots,
                motorcycle_slots=0,  # Default to 0 for now
                ev_motorcycle_slots=0  # Default to 0 for now
            )
            # Create lot data
            lot_data = ParkingLotData(
                name=lot_name,
                levels=[level_data]
            )
            # Validate data
            if not self._validate_lot_data(lot_data):
                return
            # Create parking lot
            if self.parking_manager.create_lot(lot_data):
                self._show_message(f"Created parking lot {lot_name}")
                self._update_park_lot_names()
                self._update_park_levels()
                self._update_details_lot_names()
                self._update_details_levels()
                # Set combo box values explicitly
                self.park_lot_combo['values'] = self.parking_manager.get_lot_names()
                self.park_level_combo['values'] = self.parking_manager.get_levels_for_lot(lot_name)
                self.details_lot_combo['values'] = self.parking_manager.get_lot_names()
                self.details_level_combo['values'] = self.parking_manager.get_levels_for_lot(lot_name)
            else:
                self._show_error("Failed to create parking lot")
        except ValueError as e:
            self._show_error(str(e))
    
    def _handle_show_status(self):
        """Handle show status button click"""
        try:
            # Get lot name
            lot_name = self.park_lot_value.get()
            logger.debug(f"[DEBUG] Showing status for lot: {lot_name}")
            
            # Get status
            statuses = self.parking_manager.get_lot_status(lot_name)
            logger.debug(f"[DEBUG] Retrieved {len(statuses)} status entries")
            
            # Clear tree
            self.admin_tree.delete(*self.admin_tree.get_children())
            logger.debug("[DEBUG] Cleared admin tree")
            
            # Add statuses to tree
            for status in statuses:
                logger.debug(f"[DEBUG] Processing status: level={status.level}, slot={status.slot}, is_occupied={status.is_occupied}")
                if status.vehicle is not None:
                    logger.debug(f"[DEBUG] Adding vehicle to tree: {status.vehicle.registration_number}")
                    values = (
                        f"Level {status.level}",
                        f"Slot {status.slot}",
                        status.vehicle.registration_number,
                        status.vehicle.manufacturer,
                        status.vehicle.model,
                        status.vehicle.color,
                        "EV" if status.vehicle.is_electric else "Standard",
                        "Motorcycle" if status.vehicle.is_motorcycle else "Standard",
                        f"{status.vehicle.charge}%" if status.vehicle.is_electric else "N/A"
                    )
                    self.admin_tree.insert("", "end", values=values)
                else:
                    logger.debug("[DEBUG] No vehicle in this slot")
            
            # Show message
            self._show_message(f"Showing status for lot {lot_name}")
            logger.debug("[DEBUG] Status display complete")
            
        except ValueError as e:
            logger.error(f"[DEBUG] Error showing status: {e}")
            self._show_error(str(e))
    
    def _handle_show_lots(self):
        """Handle show lots button click"""
        try:
            logger.debug("[DEBUG] Starting show lots operation")
            # Clear tree
            self.admin_tree.delete(*self.admin_tree.get_children())
            logger.debug("[DEBUG] Cleared admin tree")
            
            # Get all lot names
            lot_names = self.parking_manager.get_lot_names()
            logger.debug(f"[DEBUG] Retrieved {len(lot_names)} lots: {lot_names}")
            
            for lot_name in lot_names:
                logger.debug(f"[DEBUG] Processing lot: {lot_name}")
                # Get levels for this lot
                levels = self.parking_manager.get_levels_for_lot(lot_name)
                logger.debug(f"[DEBUG] Lot {lot_name} has {len(levels)} levels: {levels}")
                
                # Initialize counters for this lot
                total_regular = 0
                total_ev = 0
                available_regular = 0
                available_ev = 0
                
                for level in levels:
                    logger.debug(f"[DEBUG] Processing level {level} in lot {lot_name}")
                    # Get status for this level
                    statuses = self.parking_manager.get_lot_status(lot_name)
                    logger.debug(f"[DEBUG] Retrieved {len(statuses)} status entries for level {level}")
                    
                    # Count slots by type
                    for status in statuses:
                        if status.level == level:
                            logger.debug(f"[DEBUG] Processing status: slot={status.slot}, type={status.slot_type}, occupied={status.is_occupied}")
                            if status.slot_type == SlotType.REGULAR:
                                total_regular += 1
                                if not status.is_occupied:
                                    available_regular += 1
                            elif status.slot_type == SlotType.ELECTRIC:
                                total_ev += 1
                                if not status.is_occupied:
                                    available_ev += 1
                
                logger.debug(f"[DEBUG] Lot {lot_name} summary: regular={total_regular}, ev={total_ev}, avail_reg={available_regular}, avail_ev={available_ev}")
                # Add lot info to tree
                values = (
                    lot_name,
                    len(levels),
                    total_regular,
                    total_ev,
                    available_regular,
                    available_ev
                )
                logger.debug(f"[DEBUG] Inserting lot info into tree: {values}")
                self.admin_tree.insert("", "end", values=values)
            
            # Show message
            self._show_message("Showing all parking lots")
            logger.debug("[DEBUG] Show lots operation complete")
            
        except ValueError as e:
            logger.error(f"[DEBUG] Error showing lots: {e}")
            self._show_error(str(e))
    
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
        
        # Validate each level's data
        for level in data.levels:
            if level.regular_slots <= 0:
                self._show_error("Please enter valid numbers for regular slots")
                return False
            if level.electric_slots < 0:
                self._show_error("Please enter valid numbers for electric slots")
                return False
            if level.motorcycle_slots < 0:
                self._show_error("Please enter valid numbers for motorcycle slots")
                return False
            if level.ev_motorcycle_slots < 0:
                self._show_error("Please enter valid numbers for EV motorcycle slots")
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
        search_type = self.search_type_value.get()
        if search_type == "registration" and criteria.registration_number:
            registration_search = criteria.registration_number.strip().casefold()
            slot = None
            found_vehicle = None
            # Search all lots and levels for a matching registration (case-insensitive, whitespace-insensitive)
            for lot_name in self.parking_manager.get_lot_names():
                for level in self.parking_manager.get_levels_for_lot(lot_name):
                    vehicles = self.parking_manager.get_vehicles_in_lot(lot_name, level)
                    for s, vehicle in vehicles.items():
                        registration_number = vehicle.registration_number
                        if registration_number is None:
                            registration_number = vehicle.registration_number
                        registration_number = registration_number.strip().casefold() if registration_number else ""
                        if registration_number == registration_search:
                            self._add_vehicle_to_tree(vehicle, s)
                            found_vehicle = vehicle
            if not found_vehicle:
                self._show_error("No vehicle found with that registration number")
        # Add other search types as needed
    
    def _add_vehicle_to_tree(self, vehicle: Union[Vehicle, VehicleData], slot: int) -> None:
        """Add a vehicle to the results tree"""
        logger.debug(f"[DEBUG] Adding vehicle to tree: slot={slot}, vehicle={vehicle}")
        try:
            # Get vehicle attributes
            if isinstance(vehicle, Vehicle):
                registration_number = vehicle.registration_number
                manufacturer = vehicle.vehicle_manufacturer
                model = vehicle.model
                color = vehicle.color
                is_ev = isinstance(vehicle, ElectricVehicle)
                is_motorcycle = isinstance(vehicle, Motorcycle)
                charge_status = f"{vehicle.current_battery_charge}%" if is_ev and hasattr(vehicle, "current_battery_charge") else "N/A"
            else:  # VehicleData
                registration_number = vehicle.registration_number
                manufacturer = vehicle.manufacturer
                model = vehicle.model
                color = vehicle.color
                is_ev = vehicle.is_electric
                is_motorcycle = vehicle.is_motorcycle
                charge_status = "N/A"

            vehicle_type = (
                "EV Motorcycle" if is_ev and is_motorcycle else
                "EV" if is_ev else
                "Motorcycle" if is_motorcycle else "Standard"
            )

            values = (
                str(slot),
                str(registration_number),
                str(manufacturer),
                str(model),
                str(color),
                "EV" if is_ev else "Standard",
                vehicle_type,
                str(charge_status)
            )
            logger.debug(f"[DEBUG] Inserting vehicle into tree with values: {values}")
            self.results_tree.insert("", "end", values=values)
            logger.debug("[DEBUG] Vehicle added to tree successfully")
        except Exception as e:
            logger.error(f"[DEBUG] Error adding vehicle to tree: {e}")
            raise
    
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
        self.show_lots_button.grid(row=4, column=1, padx=5, pady=5)
        
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
            vehicles: Dict[int, Vehicle] = self.parking_manager.get_vehicles_in_lot(selected_lot, selected_level)
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
        status = self.parking_manager.get_status()
        self._show_message(status)

    def create_lot(self):
        """Create a new parking lot"""
        self._handle_create_lot()

    def _update_details_lot_names(self):
        """Update the lot names in the details combo box"""
        lot_names = self.parking_manager.get_lot_names()
        self.details_lot_combo['values'] = lot_names
        if lot_names:
            self.details_lot_combo.set(lot_names[0])
            self._update_details_levels()

    def _update_park_levels(self):
        """Update the levels in the park combo box based on selected lot"""
        lot_name = self.park_lot_value.get()
        if lot_name:
            levels = self.parking_manager.get_levels_for_lot(lot_name)
            self.park_level_combo['values'] = levels
            if levels:
                self.park_level_combo.set(levels[0])

    def _update_details_levels(self):
        """Update the levels in the details combo box based on selected lot"""
        lot_name = self.details_lot_name_value.get()
        if lot_name:
            levels = self.parking_manager.get_levels_for_lot(lot_name)
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
            filter_type = self.details_filter_value.get()
            
            if not lot_name:
                self._show_error("Please select a lot")
                return
            
            # Get all levels for the lot
            levels = self.parking_manager.get_levels_for_lot(lot_name)
            
            # Process based on filter type
            if filter_type == "All Levels":
                # Show all levels
                for level in levels:
                    self._add_level_details(lot_name, level)
            else:
                # Show specific level
                level = int(self.details_parking_level_value.get())
                self._add_level_details(lot_name, level, filter_type)
            
            if not self.details_tree.get_children():
                self._show_message("No slots found matching the criteria.")
                
        except Exception as e:
            logger.error(f"Error showing details: {e}")
            self._show_error("Error showing lot details")

    def _add_level_details(self, lot_name: str, level: int, filter_type: str = "All Slots"):
        """Add details for a specific level to the tree"""
        try:
            # Get status for this level
            statuses = self.parking_manager.get_lot_status(lot_name)
            
            for status in statuses:
                if status.level != level:
                    continue
                    
                # Apply filter
                if filter_type == "Available Slots" and status.is_occupied:
                    continue
                if filter_type == "Occupied Slots" and not status.is_occupied:
                    continue
                
                # Prepare values
                slot_status = "Occupied" if status.is_occupied else "Available"
                registration = status.vehicle.registration_number if status.vehicle else ""
                manufacturer = status.vehicle.manufacturer if status.vehicle else ""
                model = status.vehicle.model if status.vehicle else ""
                color = status.vehicle.color if status.vehicle else ""
                slot_type = "EV" if status.slot_type == SlotType.ELECTRIC else "Standard"
                vehicle_type = (
                    "EV Motorcycle" if status.vehicle and status.vehicle.is_electric and status.vehicle.is_motorcycle else
                    "EV" if status.vehicle and status.vehicle.is_electric else
                    "Motorcycle" if status.vehicle and status.vehicle.is_motorcycle else
                    "Standard" if status.vehicle else "N/A"
                )
                charge_status = f"{status.vehicle.charge}%" if status.vehicle and status.vehicle.is_electric else "N/A"
                
                values = (
                    level,
                    status.slot,
                    slot_status,
                    registration,
                    manufacturer,
                    model,
                    color,
                    slot_type,
                    vehicle_type,
                    charge_status
                )
                
                self.details_tree.insert("", "end", values=values)
                
        except Exception as e:
            logger.error(f"Error adding level details: {e}")
            raise

    def _update_park_lot_names(self):
        """Update the lot names in the park combo box"""
        lot_names = self.parking_manager.get_lot_names()
        self.park_lot_combo['values'] = lot_names
        if lot_names:
            self.park_lot_combo.set(lot_names[0])
            self._update_park_levels()

    def _get_vehicle_type(self) -> VehicleType:
        """Get the vehicle type based on UI selections"""
        if self.is_electric_value.get():
            if self.vehicle_type_value.get() == "Motorcycle":
                return VehicleType.ELECTRIC_MOTORCYCLE
            return VehicleType.ELECTRIC_CAR
        else:
            if self.vehicle_type_value.get() == "Motorcycle":
                return VehicleType.MOTORCYCLE
            elif self.vehicle_type_value.get() == "Truck":
                return VehicleType.TRUCK
            elif self.vehicle_type_value.get() == "Bus":
                return VehicleType.BUS
            return VehicleType.CAR


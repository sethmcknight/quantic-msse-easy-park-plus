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
from typing import List, Dict, Optional, Any, Protocol, Union
from dataclasses import dataclass
from Vehicle import Vehicle, ElectricVehicle, Motorcycle
from ParkingManager import ParkingLotObserver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VehicleData:
    """Data class for vehicle information in the UI"""
    registration: str
    make: str
    model: str
    color: str
    is_electric: bool
    is_motorcycle: bool

@dataclass
class SearchCriteria:
    """Data class for search criteria"""
    registration: Optional[str] = None
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    search_type: str = "registration"

@dataclass
class ParkingLotData:
    """Data class for parking lot information"""
    name: str
    level: int
    regular_slots: int
    ev_slots: int

class ParkingLotInterface(Protocol):
    """Protocol defining the interface for parking lot operations"""
    
    def create_parking_lot(self, data: ParkingLotData) -> None:
        """Create a new parking lot"""
        ...
    
    def park_vehicle(self, data: VehicleData) -> Optional[int]:
        """Park a vehicle"""
        ...
    
    def remove_vehicle(self, slot_number: int) -> bool:
        """Remove a vehicle"""
        ...
    
    def search_vehicles(self, criteria: SearchCriteria) -> List[Dict[str, Any]]:
        """Search for vehicles"""
        ...
    
    def get_status(self) -> str:
        """Get parking lot status"""
        ...
    
    def get_lot_names(self) -> List[str]:
        """Get all parking lot names"""
        ...
    
    def get_levels_for_lot(self, lot_name: str) -> List[int]:
        """Get levels for a lot"""
        ...
    
    def register_observer(self, observer: ParkingLotObserver) -> None:
        """Register an observer"""
        ...
    
    def get_slot_by_registration(self, reg: str) -> Optional[int]:
        """Get slot number by registration number"""
        ...
    
    def get_vehicle(self, slot_number: int) -> Optional[Vehicle]:
        """Get vehicle by slot number"""
        ...
    
    def set_name(self, name: str) -> None:
        """Set the name of the parking lot"""
        ...
    
    def park(self, reg: str, make: str, model: str, color: str, is_electric: bool, is_motorcycle: bool) -> Optional[int]:
        """Park a vehicle"""
        ...
    
    def leave(self, slot_number: int) -> bool:
        """Remove a vehicle from a slot"""
        ...
    
    def get_slots_by_color(self, color: str) -> List[int]:
        """Get slot numbers by vehicle color"""
        ...
    
    def get_slots_by_make(self, make: str) -> List[int]:
        """Get slot numbers by vehicle make"""
        ...
    
    def get_slots_by_model(self, model: str) -> List[int]:
        """Get slot numbers by vehicle model"""
        ...
    
    def get_vehicles_in_lot(self, lot_name: str, level: int) -> Dict[int, Vehicle]:
        """Get all vehicles in a specific lot and level"""
        ...

class ParkingLotUI(ParkingLotObserver):
    """Class representing the parking lot UI"""
    
    def __init__(self, parking_lot: ParkingLotInterface):
        """Initialize the UI"""
        self.parking_lot = parking_lot
        self.parking_lot.register_observer(self)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Parking Lot Management System")
        
        # Initialize UI state
        self._init_state()
        
        # Create and layout widgets
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()
        
        # Initialize dropdowns
        self._update_lot_names()
        self._update_levels()
    
    def _init_state(self):
        """Initialize UI state variables"""
        # Persistent Lot Name and Level dropdowns
        self.lot_name_value = tk.StringVar()
        self.level_value = tk.StringVar()
        
        # Vehicle Operations variables
        self.reg_value = tk.StringVar()
        self.make_value = tk.StringVar()
        self.model_value = tk.StringVar()
        self.color_value = tk.StringVar()
        self.vehicle_type_value = tk.StringVar(value="Car")
        self.ev_value = tk.BooleanVar()
        
        # Search tab variables
        self.search_reg_value = tk.StringVar()
        self.search_color_value = tk.StringVar()
        self.search_make_value = tk.StringVar()
        self.search_model_value = tk.StringVar()
        self.search_type = tk.StringVar(value="registration")
        self.search_value = tk.StringVar()
        
        # Admin tab variables
        self.num_value = tk.StringVar()
        self.ev_num_value = tk.StringVar()
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Create top frame for persistent dropdowns
        self.top_frame = ttk.Frame(self.root)
        
        # Create persistent dropdowns
        self.lot_name_label = ttk.Label(self.top_frame, text="Lot Name:")
        self.lot_name_combo = ttk.Combobox(self.top_frame, textvariable=self.lot_name_value, state="readonly")
        self.level_label = ttk.Label(self.top_frame, text="Level:")
        self.level_combo = ttk.Combobox(self.top_frame, textvariable=self.level_value, state="readonly")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs
        self.vehicle_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        self.admin_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.vehicle_tab, text="Vehicle Operations")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.add(self.admin_tab, text="Parking Lot Admin")
        
        # Create vehicle operations frame
        self.vehicle_frame = ttk.LabelFrame(self.vehicle_tab, text="Vehicle Operations")
        self._create_vehicle_widgets()
        
        # Create search frame
        self.search_frame = ttk.LabelFrame(self.search_tab, text="Search")
        self._create_search_widgets()
        
        # Create admin frame
        self.admin_frame = ttk.LabelFrame(self.admin_tab, text="Parking Lot Administration")
        self._create_admin_widgets()
        
        # Create results tree
        self._create_results_tree()
        
        # Create message area
        self.message_area = tk.Text(self.root, height=10, width=50)
    
    def _create_vehicle_widgets(self):
        """Create widgets for vehicle operations"""
        self.reg_label = ttk.Label(self.vehicle_frame, text="Registration:")
        self.reg_entry = ttk.Entry(self.vehicle_frame, textvariable=self.reg_value)
        self.make_label = ttk.Label(self.vehicle_frame, text="Make:")
        self.make_entry = ttk.Entry(self.vehicle_frame, textvariable=self.make_value)
        self.model_label = ttk.Label(self.vehicle_frame, text="Model:")
        self.model_entry = ttk.Entry(self.vehicle_frame, textvariable=self.model_value)
        self.color_label = ttk.Label(self.vehicle_frame, text="Color:")
        self.color_entry = ttk.Entry(self.vehicle_frame, textvariable=self.color_value)
        self.vehicle_type_label = ttk.Label(self.vehicle_frame, text="Vehicle Type:")
        self.vehicle_type_combo = ttk.Combobox(self.vehicle_frame, textvariable=self.vehicle_type_value, state="readonly",
                                               values=["Car", "Truck", "Bus", "Motorcycle"])
        self.ev_check = ttk.Checkbutton(self.vehicle_frame, text="Electric Vehicle", variable=self.ev_value)
        self.park_button = ttk.Button(self.vehicle_frame, text="Park", command=self._handle_park)
        self.remove_button = ttk.Button(self.vehicle_frame, text="Remove", command=self._handle_remove)
    
    def _create_search_widgets(self):
        """Create widgets for search operations"""
        self.search_reg_label = ttk.Label(self.search_frame, text="Registration:")
        self.search_reg_entry = ttk.Entry(self.search_frame, textvariable=self.search_reg_value)
        self.search_color_label = ttk.Label(self.search_frame, text="Color:")
        self.search_color_entry = ttk.Entry(self.search_frame, textvariable=self.search_color_value)
        self.search_make_label = ttk.Label(self.search_frame, text="Make:")
        self.search_make_entry = ttk.Entry(self.search_frame, textvariable=self.search_make_value)
        self.search_model_label = ttk.Label(self.search_frame, text="Model:")
        self.search_model_entry = ttk.Entry(self.search_frame, textvariable=self.search_model_value)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self._handle_search)
        self.show_status_button = ttk.Button(self.search_frame, text="Show Full Status", command=self._handle_show_status)
    
    def _create_admin_widgets(self):
        """Create widgets for admin operations"""
        self.lot_name_label = ttk.Label(self.admin_frame, text="Lot Name:")
        self.lot_name_entry = ttk.Entry(self.admin_frame, textvariable=self.lot_name_value)
        self.level_label = ttk.Label(self.admin_frame, text="Level:")
        self.level_entry = ttk.Entry(self.admin_frame, textvariable=self.level_value)
        self.num_label = ttk.Label(self.admin_frame, text="Regular Slots:")
        self.num_entry = ttk.Entry(self.admin_frame, textvariable=self.num_value)
        self.ev_num_label = ttk.Label(self.admin_frame, text="EV Slots:")
        self.ev_num_entry = ttk.Entry(self.admin_frame, textvariable=self.ev_num_value)
        self.create_button = ttk.Button(self.admin_frame, text="Create Lot", command=self._handle_create_lot)
        self.status_button = ttk.Button(self.admin_frame, text="Show Status", command=self._handle_show_status)
    
    def _create_results_tree(self):
        """Create the results tree view"""
        self.results_tree = ttk.Treeview(self.search_tab, columns=("Slot", "Registration", "Make", "Model", "Color", "Slot Type", "Vehicle Type", "Charge Status"),
                                       show="headings")
        self.results_tree.heading("Slot", text="Slot")
        self.results_tree.heading("Registration", text="Registration")
        self.results_tree.heading("Make", text="Make")
        self.results_tree.heading("Model", text="Model")
        self.results_tree.heading("Color", text="Color")
        self.results_tree.heading("Slot Type", text="Slot Type")
        self.results_tree.heading("Vehicle Type", text="Vehicle Type")
        self.results_tree.heading("Charge Status", text="Charge Status")
    
    def _bind_events(self):
        """Bind event handlers"""
        self.lot_name_combo.bind('<<ComboboxSelected>>', self._handle_lot_change)
        self.level_combo.bind('<<ComboboxSelected>>', self._handle_level_change)
    
    def _handle_park(self):
        """Handle park vehicle button click"""
        try:
            data = VehicleData(
                registration=self.reg_value.get(),
                make=self.make_value.get(),
                model=self.model_value.get(),
                color=self.color_value.get(),
                is_electric=self.ev_value.get(),
                is_motorcycle=self.vehicle_type_value.get() == "Motorcycle"
            )
            
            if not self._validate_vehicle_data(data):
                return
            
            slot = self.parking_lot.park(
                data.registration, data.make, data.model,
                data.color, data.is_electric, data.is_motorcycle
            )
            
            if slot is not None:
                self._show_message(f"Vehicle parked in slot {slot}")
                self._clear_park_fields()
            else:
                self._show_error("No available slots")
        
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
                registration=self.search_reg_value.get(),
                color=self.search_color_value.get(),
                make=self.search_make_value.get(),
                model=self.search_model_value.get(),
                search_type=self.search_type.get()
            )
            
            self._perform_search(criteria)
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            self._show_error("Error performing search")
    
    def _handle_create_lot(self):
        """Handle create lot button click"""
        try:
            print(f"[UI DEBUG] lot_name_value: '{self.lot_name_value.get()}', level_value: '{self.level_value.get()}', num_value: '{self.num_value.get()}', ev_num_value: '{self.ev_num_value.get()}'")
            data = ParkingLotData(
                name=self.lot_name_value.get().strip(),
                level=int(self.level_value.get()),
                regular_slots=int(self.num_value.get()),
                ev_slots=int(self.ev_num_value.get())
            )
            
            if not self._validate_lot_data(data):
                return
            
            self.parking_lot.create_parking_lot(data.regular_slots, data.ev_slots, data.level)
            self.parking_lot.set_name(data.name)
            self._show_message(f"Created parking lot {data.name}")
            self._update_lot_names()
            self._update_levels()

            # Ensure level value is set to first available after creation
            levels = self.parking_lot.get_levels_for_lot(data.name)
            if levels:
                self.level_value.set(str(levels[0]))
        
        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            self._show_error("Please enter valid numbers")
        except Exception as e:
            logger.error(f"Error creating lot: {e}")
            self._show_error("Error creating parking lot")
    
    def _handle_show_status(self):
        """Handle show status button click"""
        try:
            selected_lot = self.lot_name_value.get().strip()
            level_str = self.level_value.get().strip()
            if not selected_lot:
                self._show_error("Please select a parking lot")
                return
            if not level_str:
                self._show_error("Please select a level")
                return
            try:
                selected_level = int(level_str)
            except ValueError:
                self._show_error("Invalid level value")
                return
            # Clear previous results
            self.results_tree.delete(*self.results_tree.get_children())
            # Get all vehicles in the lot
            vehicles = self.parking_lot.get_vehicles_in_lot(selected_lot, selected_level)
            for slot_number, vehicle in vehicles.items():
                self._add_vehicle_to_tree(vehicle, slot_number)
            # Also show status message
            status = self.parking_lot.get_status()
            self._show_message(status)
            if not self.results_tree.get_children():
                self._show_message("No vehicles found in the selected lot and level.")
        except Exception as e:
            logger.error(f"Error showing status: {e}")
            self._show_error("Error getting status")
    
    def _handle_lot_change(self, event: Any):
        """Handle lot name change"""
        self._update_levels()
    
    def _handle_level_change(self, event: Any):
        """Handle level change"""
        pass  # Add any level-specific updates here
    
    def _validate_vehicle_data(self, data: VehicleData) -> bool:
        """Validate vehicle data"""
        if not data.registration:
            self._show_error("Please enter registration number")
            return False
        if not data.make:
            self._show_error("Please enter make")
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
        if data.ev_slots < 0:
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
            reg_search = criteria.registration.strip().casefold()
            slot = None
            found_vehicle = None
            # Search all lots and levels for a matching registration (case-insensitive, whitespace-insensitive)
            for lot_name in self.parking_lot.get_lot_names():
                for level in self.parking_lot.get_levels_for_lot(lot_name):
                    vehicles = self.parking_lot.get_vehicles_in_lot(lot_name, level)
                    for s, vehicle in vehicles.items():
                        reg = getattr(vehicle, 'registration_number', None)
                        if reg is None:
                            reg = getattr(vehicle, 'registration', '')
                        reg = reg.strip().casefold()
                        if reg == reg_search:
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
        elif criteria.search_type == "make" and criteria.make:
            slots = self.parking_lot.get_slots_by_make(criteria.make.strip())
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
            reg = vehicle.registration_number
            make = vehicle.make
            model = vehicle.model
            color = vehicle.color
            is_ev = isinstance(vehicle, ElectricVehicle)
            is_motorcycle = isinstance(vehicle, Motorcycle)
            charge_status = f"{vehicle.charge}%" if isinstance(vehicle, ElectricVehicle) else "N/A"
        else:  # VehicleData
            reg = vehicle.registration
            make = vehicle.make
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
            slot,
            reg,
            make,
            model,
            color,
            "EV" if is_ev else "Standard",
            vehicle_type,
            charge_status
        ))
    
    def _clear_park_fields(self):
        """Clear vehicle input fields"""
        self.reg_value.set("")
        self.make_value.set("")
        self.model_value.set("")
        self.color_value.set("")
        self.vehicle_type_value.set("Car")
        self.ev_value.set(False)
    
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
        self.root.mainloop()

    def _update_lot_names(self) -> None:
        """Update the lot name combobox with current lot names"""
        lot_names = self.parking_lot.get_lot_names()
        self.lot_name_combo['values'] = lot_names
        if lot_names:
            self.lot_name_combo.set(lot_names[0])
        self._update_levels()
    
    def _update_levels(self) -> None:
        """Update the level combobox with current levels"""
        selected_lot = self.lot_name_value.get()
        if selected_lot:
            levels = self.parking_lot.get_levels_for_lot(selected_lot)
            self.level_combo['values'] = levels
            # Always set to first available level if not set or invalid
            current_level = self.level_value.get()
            if not current_level or current_level not in map(str, levels):
                if levels:
                    self.level_combo.set(str(levels[0]))
    
    def _show_full_status(self) -> None:
        """Show full status of the parking lot"""
        try:
            selected_lot = self.lot_name_value.get()
            selected_level = int(self.level_value.get())
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

    def _layout_widgets(self):
        """Layout UI widgets"""
        # Layout top frame with persistent dropdowns
        self.top_frame.pack(fill="x", padx=5, pady=5)
        self.lot_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.lot_name_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.level_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.level_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Layout notebook
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout vehicle frame
        self.vehicle_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.reg_label.grid(row=0, column=0, padx=5, pady=5)
        self.reg_entry.grid(row=0, column=1, padx=5, pady=5)
        self.make_label.grid(row=1, column=0, padx=5, pady=5)
        self.make_entry.grid(row=1, column=1, padx=5, pady=5)
        self.model_label.grid(row=2, column=0, padx=5, pady=5)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)
        self.color_label.grid(row=3, column=0, padx=5, pady=5)
        self.color_entry.grid(row=3, column=1, padx=5, pady=5)
        self.vehicle_type_label.grid(row=4, column=0, padx=5, pady=5)
        self.vehicle_type_combo.grid(row=4, column=1, padx=5, pady=5)
        self.ev_check.grid(row=5, column=0, padx=5, pady=5)
        self.park_button.grid(row=6, column=0, padx=5, pady=5)
        self.remove_button.grid(row=6, column=1, padx=5, pady=5)
        
        # Layout search frame
        self.search_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.search_reg_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_reg_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_color_label.grid(row=1, column=0, padx=5, pady=5)
        self.search_color_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_make_label.grid(row=2, column=0, padx=5, pady=5)
        self.search_make_entry.grid(row=2, column=1, padx=5, pady=5)
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
        self.ev_num_label.grid(row=3, column=0, padx=5, pady=5)
        self.ev_num_entry.grid(row=3, column=1, padx=5, pady=5)
        self.create_button.grid(row=4, column=0, padx=5, pady=5)
        self.status_button.grid(row=4, column=1, padx=5, pady=5)
        
        # Layout results tree
        self.results_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout message area
        self.message_area.pack(expand=True, fill="both", padx=5, pady=5) 
"""
Parking Lot UI Module

This module implements the user interface for the parking lot management system.
It uses the Observer pattern to receive updates from the parking lot and update the UI accordingly.

Anti-patterns Removed:
1. UI-Business Logic Coupling
   - Removed: Direct UI manipulation from business logic
   - Solution: Observer pattern for UI updates
   - Benefit: Separation of concerns

2. Global Variables
   - Removed: Global Tkinter variables
   - Solution: Instance attributes in UI class
   - Benefit: Better encapsulation

3. Hard-Coded UI Elements
   - Removed: Hard-coded colors, fonts, and layouts
   - Solution: Configuration constants
   - Benefit: Easier to maintain and modify

Design Patterns Implemented:
1. Observer Pattern
   - Purpose: Decouple UI from business logic
   - Components: ParkingLotUI as observer
   - Benefit: Clean separation of concerns

2. Builder Pattern
   - Purpose: Construct UI components
   - Components: UI builder methods
   - Benefit: Encapsulated UI construction

Usage:
    The ParkingLotUI class is the main entry point for the application.
    It creates and manages the UI components and handles user interactions.

Example:
    >>> from ParkingManager import ParkingLot
    >>> from ParkingLotUI import ParkingLotUI
    >>> parking_lot = ParkingLot()
    >>> ui = ParkingLotUI(parking_lot)
    >>> ui.run()
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
        self.main_window = tk.Tk()
        self.main_window.title(self.WINDOW_TITLE)
        self.main_window.geometry(self.WINDOW_SIZE)
        
        # Initialize UI state
        self._init_state()
        
        # Create and layout widgets
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self) -> None:
        """Create all UI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.main_window, padding=self.PADDING)
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
        
        # Park vehicle section
        self.park_frame = self._create_section("Park Vehicle")
        self.registration_entry = self._create_labeled_entry(self.park_frame, "Registration:", self.state.registration_number)
        self.make_entry = self._create_labeled_entry(self.park_frame, "Make:", self.state.make)
        self.model_entry = self._create_labeled_entry(self.park_frame, "Model:", self.state.model)
        self.color_entry = self._create_labeled_entry(self.park_frame, "Color:", self.state.color)
        self.electric_vehicle_checkbox = self._create_checkbox(self.park_frame, "Electric Vehicle", self.state.is_electric)
        self.motorcycle_checkbox = self._create_checkbox(self.park_frame, "Motorcycle", self.state.is_motorcycle)
        self.park_button = ttk.Button(self.park_frame, text="Park Vehicle", command=self._park_vehicle)
        
        # Remove vehicle section
        self.remove_frame = self._create_section("Remove Vehicle")
        self.remove_registration_entry = self._create_labeled_entry(self.remove_frame, "Registration:", "")
        self.remove_button = ttk.Button(self.remove_frame, text="Remove Vehicle", command=self._remove_vehicle)
        
    def _create_section(self, title: str) -> ttk.LabelFrame:
        """Create a labeled frame section"""
        return ttk.LabelFrame(self.main_frame, text=title, padding=self.PADDING)
        
    def _create_labeled_entry(self, parent: Union[ttk.Frame, ttk.LabelFrame], label: str, default: str) -> ttk.Entry:
        """Create a labeled entry field"""
        frame = ttk.Frame(parent)
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, default)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        frame.pack(fill=tk.X, pady=2)
        return entry
        
    def _create_checkbox(self, parent: Union[ttk.Frame, ttk.LabelFrame], label: str, default: bool) -> ttk.Checkbutton:
        """Create a checkbox"""
        var = tk.BooleanVar(value=default)
        check = ttk.Checkbutton(parent, text=label, variable=var)
        check.pack(fill=tk.X, pady=2)
        return check
        
    def _layout_widgets(self) -> None:
        """Layout all UI widgets"""
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create parking lot section
        self.create_lot_frame.pack(fill=tk.X, pady=5)
        self.create_lot_button.pack(pady=5)
        
        # Park vehicle section
        self.park_frame.pack(fill=tk.X, pady=5)
        self.park_button.pack(pady=5)
        
        # Remove vehicle section
        self.remove_frame.pack(fill=tk.X, pady=5)
        self.remove_button.pack(pady=5)
        
    def _create_lot(self) -> None:
        """Handle create lot button click"""
        try:
            level = int(self.level_entry.get())
            if level <= 0:
                raise ValueError("Level must be positive")
            self.parking_lot.create_parking_lot(level)
            self._show_message("Parking lot created successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def _park_vehicle(self) -> None:
        """Handle park vehicle button click"""
        try:
            # Get vehicle information
            registration_number = self.registration_entry.get().strip()
            make = self.make_entry.get().strip()
            model = self.model_entry.get().strip()
            color = self.color_entry.get().strip()
            is_electric = self.electric_vehicle_checkbox.instate(['selected'])
            is_motorcycle = self.motorcycle_checkbox.instate(['selected'])
            
            # Validate input
            if not all([registration_number, make, model, color]):
                raise ValueError("All fields are required")
                
            # Park the vehicle
            self.parking_lot.park(registration_number, make, model, color, is_electric, is_motorcycle)
            self._show_message("Vehicle parked successfully")
            
            # Clear input fields
            self.registration_entry.delete(0, tk.END)
            self.make_entry.delete(0, tk.END)
            self.model_entry.delete(0, tk.END)
            self.color_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def _remove_vehicle(self) -> None:
        """Handle remove vehicle button click"""
        try:
            registration_number = self.remove_registration_entry.get().strip()
            if not registration_number:
                raise ValueError("Registration number is required")
                
            self.parking_lot.remove(registration_number)
            self._show_message("Vehicle removed successfully")
            self.remove_registration_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def _show_message(self, message: str) -> None:
        """Show a message in the text display"""
        self.text_display.insert(tk.END, f"{message}\n")
        self.text_display.see(tk.END)
        
    def update(self, message: str) -> None:
        """Handle updates from the parking lot"""
        self._show_message(message)
        
    def run(self) -> None:
        """Start the UI main loop"""
        self.main_window.mainloop()

if __name__ == "__main__":
    from ParkingManager import ParkingLot
    parking_lot = ParkingLot()
    ui = ParkingLotUI(parking_lot)
    ui.run()
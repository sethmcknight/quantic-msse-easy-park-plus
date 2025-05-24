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
from tkinter import ttk, messagebox
from typing import Optional, Callable, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
from ParkingManager import ParkingLot

class ParkingLotObserver(ABC):
    """Abstract base class for parking lot observers"""
    
    @abstractmethod
    def update(self, message: str) -> None:
        """Handle updates from the parking lot"""
        pass

@dataclass
class UIState:
    """Data class to hold UI state"""
    registration_number: str = ""
    make: str = ""
    model: str = ""
    color: str = ""
    level: str = ""
    is_electric: bool = False
    is_motorcycle: bool = False

class ParkingLotUI(ParkingLotObserver):
    """UI class for the parking lot management system"""
    
    # UI Configuration
    WINDOW_TITLE = "Parking Lot Management System"
    WINDOW_SIZE = "800x600"
    PADDING = 10
    FONT = ("Arial", 12)
    HEADER_FONT = ("Arial", 14, "bold")
    
    def __init__(self, parking_lot: ParkingLot):
        """Initialize the UI with a parking lot instance"""
        self.parking_lot = parking_lot
        self.parking_lot.register_observer(self)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.WINDOW_SIZE)
        
        # Initialize UI state
        self.state = UIState()
        
        # Create UI components
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self) -> None:
        """Create all UI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding=self.PADDING)
        
        # Text display area
        self.text_display = tk.Text(self.main_frame, height=10, width=60)
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Create parking lot section
        self.create_lot_frame = self._create_section("Create Parking Lot")
        self.level_entry = self._create_labeled_entry(self.create_lot_frame, "Level:", self.state.level)
        self.create_lot_button = ttk.Button(self.create_lot_frame, text="Create Lot", command=self._create_lot)
        
        # Park vehicle section
        self.park_frame = self._create_section("Park Vehicle")
        self.reg_entry = self._create_labeled_entry(self.park_frame, "Registration:", self.state.registration_number)
        self.make_entry = self._create_labeled_entry(self.park_frame, "Make:", self.state.make)
        self.model_entry = self._create_labeled_entry(self.park_frame, "Model:", self.state.model)
        self.color_entry = self._create_labeled_entry(self.park_frame, "Color:", self.state.color)
        self.ev_check = self._create_checkbox(self.park_frame, "Electric Vehicle", self.state.is_electric)
        self.motor_check = self._create_checkbox(self.park_frame, "Motorcycle", self.state.is_motorcycle)
        self.park_button = ttk.Button(self.park_frame, text="Park Vehicle", command=self._park_vehicle)
        
        # Remove vehicle section
        self.remove_frame = self._create_section("Remove Vehicle")
        self.remove_reg_entry = self._create_labeled_entry(self.remove_frame, "Registration:", "")
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
            reg = self.reg_entry.get().strip()
            make = self.make_entry.get().strip()
            model = self.model_entry.get().strip()
            color = self.color_entry.get().strip()
            is_electric = self.ev_check.instate(['selected'])
            is_motorcycle = self.motor_check.instate(['selected'])
            
            # Validate input
            if not all([reg, make, model, color]):
                raise ValueError("All fields are required")
                
            # Park the vehicle
            self.parking_lot.park(reg, make, model, color, is_electric, is_motorcycle)
            self._show_message("Vehicle parked successfully")
            
            # Clear input fields
            self.reg_entry.delete(0, tk.END)
            self.make_entry.delete(0, tk.END)
            self.model_entry.delete(0, tk.END)
            self.color_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def _remove_vehicle(self) -> None:
        """Handle remove vehicle button click"""
        try:
            reg = self.remove_reg_entry.get().strip()
            if not reg:
                raise ValueError("Registration number is required")
                
            self.parking_lot.remove(reg)
            self._show_message("Vehicle removed successfully")
            self.remove_reg_entry.delete(0, tk.END)
            
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
        self.root.mainloop()

if __name__ == "__main__":
    from ParkingManager import ParkingLot
    parking_lot = ParkingLot()
    ui = ParkingLotUI(parking_lot)
    ui.run() 
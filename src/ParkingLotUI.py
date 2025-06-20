"""
Parking Lot UI Module

This module provides a graphical user interface for the parking lot management system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Optional, List, Any, Tuple, TypedDict, Protocol, Union, TYPE_CHECKING
from Vehicle import Vehicle, VehicleType
from ParkingManager import ParkingLotManagerImpl
from models import (
    VehicleData, SearchCriteria, ParkingLotData, ParkingLevelData,
    VehicleType, SlotType, ParkingSlotData, SearchResult
)
from interfaces import ParkingLotObserver, ValidationError, OperationError

if TYPE_CHECKING:
    from tkinter import _tkinter  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parking_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ParkingLotUIError(Exception):
    """Base exception for ParkingLotUI errors"""
    pass

class TreeviewItemDict(TypedDict):
    """Type definition for Treeview item dictionary"""
    values: Tuple[str, ...]
    text: str
    image: str
    open: bool
    tags: Tuple[str, ...]

class VehicleProtocol(Protocol):
    """Protocol for vehicle-like objects"""
    registration_number: str
    manufacturer: str
    model: str
    color: str
    is_electric: bool
    vehicle_type: VehicleType
    is_motorcycle: bool
    current_battery_charge: Optional[float]

class UIStateManager:
    """Manages UI state variables"""
    def __init__(self):
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
        
        # Remove section variables
        self.remove_lot_value = tk.StringVar()
        self.remove_level_value = tk.StringVar()
        self.remove_slot_value = tk.StringVar()
        
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
        self.details_filter_value = tk.StringVar(value="All Slots")

class TreeViewManager:
    """Manages tree view operations"""
    def __init__(self, tree: ttk.Treeview):
        self.tree = tree

    def clear(self):
        """Clear all items from the tree"""
        self.tree.delete(*self.tree.get_children())

    def add_vehicle(self, vehicle: Union[Vehicle, VehicleData], slot: int):
        """Add a vehicle to the tree"""
        registration_number: str = vehicle.registration_number
        manufacturer: str = vehicle.manufacturer
        model: str = vehicle.model
        color: str = vehicle.color
        is_ev: bool = vehicle.is_electric
        is_motorcycle: bool = vehicle.vehicle_type == VehicleType.MOTORCYCLE
        
        charge_status: str = "N/A"
        if is_ev:
            if isinstance(vehicle, Vehicle) and hasattr(vehicle, 'current_battery_charge'):
                charge_status = f"{vehicle.current_battery_charge:.1f}%"
            elif isinstance(vehicle, VehicleData) and hasattr(vehicle, 'current_battery_charge'):
                charge_status = f"{vehicle.current_battery_charge:.1f}%"

        vehicle_type: str = (
            "EV Motorcycle" if is_ev and is_motorcycle else
            "EV" if is_ev else
            "Motorcycle" if is_motorcycle else "Standard"
        )

        values: Tuple[str, ...] = (
            str(slot),
            str(registration_number),
            str(manufacturer),
            str(model),
            str(color),
            "EV" if is_ev else "Standard",
            vehicle_type,
            charge_status
        )

        self.tree.insert("", "end", values=values)

class MessageManager:
    """Manages message display"""
    def __init__(self, message_area: tk.Text):
        self.message_area = message_area

    def show_message(self, message: str):
        """Show a message in the message area"""
        self.message_area.insert("end", f"{message}\n")
        self.message_area.see("end")

    def show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)  # type: ignore

class ValidationManager:
    """Manages input validation"""
    @staticmethod
    def validate_vehicle_data(data: VehicleData) -> bool:
        """Validate vehicle data"""
        try:
            if not data.registration_number:
                raise ValidationError("Please enter registration number")
            if not data.manufacturer:
                raise ValidationError("Please enter manufacturer")
            if not data.model:
                raise ValidationError("Please enter model")
            if not data.color:
                raise ValidationError("Please enter color")
            return True
        except ValidationError as e:
            raise ValidationError(str(e))

    @staticmethod
    def validate_lot_data(data: ParkingLotData) -> bool:
        """Validate parking lot data"""
        if not data.name:
            raise ValidationError("Please enter a lot name")
        
        for level in data.levels:
            regular_slots = len([s for s in level.slots if s.slot_type == SlotType.REGULAR])
            electric_slots = len([s for s in level.slots if s.slot_type == SlotType.ELECTRIC])
            
            if regular_slots <= 0:
                raise ValidationError("Please enter valid numbers for regular slots")
            if electric_slots < 0:
                raise ValidationError("Please enter valid numbers for electric slots")
        
        return True

class ParkingLotUI(ParkingLotObserver):
    """Class representing the parking lot UI"""
    
    def __init__(self):
        """Initialize the UI"""
        logger.info("Initializing ParkingLotUI")
        self.parking_manager = ParkingLotManagerImpl()
        
        # Create main window
        self.main_window = tk.Tk()
        self.main_window.title("Parking Lot Management System")
        
        # Initialize managers
        self.state_manager = UIStateManager()
        self.validation_manager = ValidationManager()
        
        # Create and layout widgets
        self._create_widgets()
        self._layout_widgets()
        
        # Initialize message manager after creating message_area
        self.message_manager = MessageManager(self.message_area)
        
        # Initialize tree manager after creating results_tree
        self.tree_manager = TreeViewManager(self.results_tree)
        
        # Register as observer after all managers are initialized
        self.parking_manager.register_observer(self)
        
        # Initialize dropdowns
        logger.info("Initializing dropdowns")
        self._update_park_lot_names()
        self._update_park_levels()
        self._update_remove_lot_names()
        logger.info("ParkingLotUI initialization complete")

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
        
        # Create search widgets
        self._create_search_widgets()
        
        # Create admin frame
        self.admin_frame = ttk.LabelFrame(self.admin_tab, text="Parking Lot Administration")
        self._create_admin_widgets()
        
        # Create details frame
        self.details_frame = ttk.LabelFrame(self.details_tab, text="Lot Details")
        self._create_details_widgets()
        
        # Create message area
        self.message_area = tk.Text(self.main_window, height=10, width=50)
    
    def _create_vehicle_widgets(self):
        """Create widgets for vehicle operations"""
        # Create Park Vehicle frame
        self.park_frame = ttk.LabelFrame(self.vehicle_frame, text="Park Vehicle")
        self.park_frame.pack(fill="x", padx=5, pady=5)
        
        # Create lot selection frame
        self.park_lot_frame = ttk.Frame(self.park_frame)
        self.park_lot_frame.pack(fill="x", padx=5, pady=5)
        
        # Create lot selection widgets
        self.park_lot_label = ttk.Label(self.park_lot_frame, text="Lot Name:")
        self.park_lot_combo = ttk.Combobox(self.park_lot_frame, textvariable=self.state_manager.park_lot_value, state="readonly")
        
        self.park_level_label = ttk.Label(self.park_lot_frame, text="Level:")
        self.park_level_combo = ttk.Combobox(self.park_lot_frame, textvariable=self.state_manager.park_level_value, state="readonly")
        
        # Layout lot selection widgets
        self.park_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.park_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.park_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.park_level_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Create vehicle input frame
        self.vehicle_input_frame = ttk.Frame(self.park_frame)
        self.vehicle_input_frame.pack(fill="x", padx=5, pady=5)
        
        # Create vehicle input widgets
        self.registration_label = ttk.Label(self.vehicle_input_frame, text="Registration Number:")
        self.registration_entry = ttk.Entry(self.vehicle_input_frame, textvariable=self.state_manager.registration_number_value)
        self.manufacturer_label = ttk.Label(self.vehicle_input_frame, text="Manufacturer:")
        self.manufacturer_entry = ttk.Entry(self.vehicle_input_frame, textvariable=self.state_manager.vehicle_manufacturer_value)
        self.model_label = ttk.Label(self.vehicle_input_frame, text="Model:")
        self.model_entry = ttk.Entry(self.vehicle_input_frame, textvariable=self.state_manager.vehicle_model_value)
        self.color_label = ttk.Label(self.vehicle_input_frame, text="Color:")
        self.color_entry = ttk.Entry(self.vehicle_input_frame, textvariable=self.state_manager.vehicle_color_value)
        self.vehicle_type_label = ttk.Label(self.vehicle_input_frame, text="Vehicle Type:")
        self.vehicle_type_combo = ttk.Combobox(self.vehicle_input_frame, textvariable=self.state_manager.vehicle_type_value, state="readonly",
                                               values=["Car", "Truck", "Bus", "Motorcycle"])
        self.electric_vehicle_check = ttk.Checkbutton(self.vehicle_input_frame, text="Electric Vehicle", variable=self.state_manager.is_electric_value)
        self.park_button = ttk.Button(self.vehicle_input_frame, text="Park", command=self._handle_park)
        
        # Layout vehicle input widgets
        self.registration_label.grid(row=0, column=0, padx=5, pady=5)
        self.registration_entry.grid(row=0, column=1, padx=5, pady=5)
        self.manufacturer_label.grid(row=1, column=0, padx=5, pady=5)
        self.manufacturer_entry.grid(row=1, column=1, padx=5, pady=5)
        self.model_label.grid(row=2, column=0, padx=5, pady=5)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)
        self.color_label.grid(row=3, column=0, padx=5, pady=5)
        self.color_entry.grid(row=3, column=1, padx=5, pady=5)
        self.vehicle_type_label.grid(row=4, column=0, padx=5, pady=5)
        self.vehicle_type_combo.grid(row=4, column=1, padx=5, pady=5)
        self.electric_vehicle_check.grid(row=5, column=0, padx=5, pady=5)
        self.park_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        # Create Remove Vehicle frame
        self.remove_frame = ttk.LabelFrame(self.vehicle_frame, text="Remove Vehicle")
        self.remove_frame.pack(fill="x", padx=5, pady=5)
        
        # Create remove vehicle widgets
        self.remove_lot_label = ttk.Label(self.remove_frame, text="Lot Name:")
        self.remove_lot_combo = ttk.Combobox(self.remove_frame, textvariable=self.state_manager.remove_lot_value, state="readonly")
        
        self.remove_level_label = ttk.Label(self.remove_frame, text="Level:")
        self.remove_level_combo = ttk.Combobox(self.remove_frame, textvariable=self.state_manager.remove_level_value, state="readonly")
        
        self.remove_slot_label = ttk.Label(self.remove_frame, text="Slot Number:")
        self.remove_slot_combo = ttk.Combobox(self.remove_frame, textvariable=self.state_manager.remove_slot_value, state="readonly")
        
        self.remove_button = ttk.Button(self.remove_frame, text="Remove", command=self._handle_remove)
        
        # Create vehicle info frame
        self.vehicle_info_frame = ttk.Frame(self.remove_frame)
        self.vehicle_info_label = ttk.Label(self.vehicle_info_frame, text="No vehicle selected")
        
        # Layout remove vehicle widgets
        self.remove_lot_label.grid(row=0, column=0, padx=5, pady=5)
        self.remove_lot_combo.grid(row=0, column=1, padx=5, pady=5)
        self.remove_level_label.grid(row=0, column=2, padx=5, pady=5)
        self.remove_level_combo.grid(row=0, column=3, padx=5, pady=5)
        self.remove_slot_label.grid(row=1, column=0, padx=5, pady=5)
        self.remove_slot_combo.grid(row=1, column=1, padx=5, pady=5)
        self.remove_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # Layout vehicle info
        self.vehicle_info_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        self.vehicle_info_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Bind events
        self.remove_lot_combo.bind('<<ComboboxSelected>>', self._on_remove_lot_selected)
        self.remove_level_combo.bind('<<ComboboxSelected>>', self._on_remove_level_selected)
        self.remove_slot_combo.bind('<<ComboboxSelected>>', self._on_remove_slot_selected)
        
        # Update lot names in combo boxes
        self._update_remove_lot_names()
        self._update_park_lot_names()
    
    def _create_search_widgets(self):
        """Create widgets for search operations"""
        # Create search form frame
        self.search_form_frame = ttk.Frame(self.search_tab)
        self.search_form_frame.pack(fill="x", padx=5, pady=5)
        
        # Create search widgets
        self.search_registration_label = ttk.Label(self.search_form_frame, text="Registration:")
        self.search_registration_entry = ttk.Entry(self.search_form_frame, textvariable=self.state_manager.search_registration_number_value)
        self.search_color_label = ttk.Label(self.search_form_frame, text="Color:")
        self.search_color_entry = ttk.Entry(self.search_form_frame, textvariable=self.state_manager.search_vehicle_color_value)
        self.search_manufacturer_label = ttk.Label(self.search_form_frame, text="Manufacturer:")
        self.search_manufacturer_entry = ttk.Entry(self.search_form_frame, textvariable=self.state_manager.search_vehicle_manufacturer_value)
        self.search_model_label = ttk.Label(self.search_form_frame, text="Model:")
        self.search_model_entry = ttk.Entry(self.search_form_frame, textvariable=self.state_manager.search_vehicle_model_value)
        
        # Create button frame
        self.search_button_frame = ttk.Frame(self.search_form_frame)
        self.search_button = ttk.Button(self.search_button_frame, text="Search", command=self._handle_search)
        
        # Layout search widgets
        self.search_registration_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_registration_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_color_label.grid(row=0, column=2, padx=5, pady=5)
        self.search_color_entry.grid(row=0, column=3, padx=5, pady=5)
        self.search_manufacturer_label.grid(row=1, column=0, padx=5, pady=5)
        self.search_manufacturer_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_model_label.grid(row=1, column=2, padx=5, pady=5)
        self.search_model_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Layout button frame
        self.search_button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        self.search_button.pack(side="left", padx=5)
        
        # Create results tree
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
    
    def _create_admin_widgets(self):
        """Create admin tab widgets"""
        # Create admin widgets
        self.lot_name_label = ttk.Label(self.admin_frame, text="Lot Name:")
        self.lot_name_entry = ttk.Entry(self.admin_frame, textvariable=self.state_manager.lot_name_value)
        self.level_label = ttk.Label(self.admin_frame, text="Level:")
        self.level_entry = ttk.Entry(self.admin_frame, textvariable=self.state_manager.parking_level_value)
        self.num_label = ttk.Label(self.admin_frame, text="Number of Regular Slots:")
        self.num_entry = ttk.Entry(self.admin_frame, textvariable=self.state_manager.regular_slots_value)
        self.electric_vehicle_num_label = ttk.Label(self.admin_frame, text="Number of Electric Vehicle Slots:")
        self.electric_vehicle_num_entry = ttk.Entry(self.admin_frame, textvariable=self.state_manager.electric_vehicle_slots_value)
        self.create_button = ttk.Button(self.admin_frame, text="Create Parking Lot", command=self._handle_create_lot)
        self.show_lots_button = ttk.Button(self.admin_frame, text="Show All Lots", command=self._handle_show_lots)
        self.load_sample_button = ttk.Button(self.admin_frame, text="Load Sample Data", command=self._handle_load_sample_data)
        
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
        self.details_lot_combo = ttk.Combobox(self.details_select_frame, textvariable=self.state_manager.details_lot_name_value, state="readonly")
        
        self.details_level_label = ttk.Label(self.details_select_frame, text="Level:")
        self.details_level_combo = ttk.Combobox(self.details_select_frame, textvariable=self.state_manager.details_parking_level_value, state="readonly")
        
        # Add filter options
        self.details_filter_label = ttk.Label(self.details_select_frame, text="Filter:")
        self.details_filter_combo = ttk.Combobox(self.details_select_frame, 
                                               textvariable=self.state_manager.details_filter_value,
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
    
    def _handle_park(self):
        """Handle park button click"""
        try:
            # Get and validate vehicle data
            vehicle_data = self._get_vehicle_data()
            if not self.validation_manager.validate_vehicle_data(vehicle_data):
                return
            
            # Get lot and level
            lot_name = self.state_manager.park_lot_value.get()
            level_str = self.state_manager.park_level_value.get()
            
            if not lot_name or not level_str:
                raise ValidationError("Please select lot and level")
            
            try:
                level = int(level_str)
            except ValueError:
                raise ValidationError("Invalid level number")
            
            # Park vehicle
            slot = self.parking_manager.park_vehicle(lot_name, level, vehicle_data)
            if slot is not None:
                self.message_manager.show_message(f"Parked vehicle in slot {slot}")
                self._update_remove_slots(lot_name, level)
            else:
                raise OperationError("Failed to park vehicle - no available slots")
                
        except ValidationError as e:
            self.message_manager.show_error(str(e))
        except OperationError as e:
            self.message_manager.show_error(str(e))
        except Exception as e:
            logger.error(f"Error in _handle_park: {e}")
            self.message_manager.show_error("An unexpected error occurred")

    def _get_vehicle_data(self) -> VehicleData:
        """Get vehicle data from UI fields"""
        try:
            vehicle_type = self._get_vehicle_type()
            is_motorcycle = vehicle_type == VehicleType.MOTORCYCLE
            return VehicleData(
                registration_number=self.state_manager.registration_number_value.get().strip(),
                manufacturer=self.state_manager.vehicle_manufacturer_value.get().strip(),
                model=self.state_manager.vehicle_model_value.get().strip(),
                color=self.state_manager.vehicle_color_value.get().strip(),
                is_electric=self.state_manager.is_electric_value.get(),
                is_motorcycle=is_motorcycle,
                vehicle_type=vehicle_type
            )
        except Exception as e:
            raise ValidationError(f"Error getting vehicle data: {e}")

    def _handle_remove(self):
        """Handle remove button click"""
        try:
            # Get and validate input
            lot_name, level, slot = self._get_remove_input()
            if not all([lot_name, level, slot]):
                return
            
            # Verify slot exists and is occupied
            if not self._verify_slot_occupied(lot_name, level, slot):
                return
            
            # Remove vehicle
            vehicle = self.parking_manager.remove_vehicle(lot_name, level, slot)
            if vehicle:
                self.message_manager.show_message(f"Removed vehicle {vehicle.registration_number} from slot {slot}")
                self._update_remove_slots(lot_name, level)
            else:
                raise OperationError("No vehicle found in selected slot")
                
        except ValidationError as e:
            self.message_manager.show_error(str(e))
        except OperationError as e:
            self.message_manager.show_error(str(e))
        except Exception as e:
            logger.error(f"Error in _handle_remove: {e}")
            self.message_manager.show_error("An unexpected error occurred")

    def _get_remove_input(self) -> tuple[str, int, int]:
        """Get and validate remove input"""
        lot_name = self.state_manager.remove_lot_value.get()
        level_str = self.state_manager.remove_level_value.get()
        slot_str = self.state_manager.remove_slot_value.get()
        
        if not lot_name or not level_str or not slot_str:
            raise ValidationError("Please select lot, level, and slot")
        
        try:
            level = int(level_str)  # Keep 1-based indexing
            slot = int(slot_str)
            return lot_name, level, slot
        except ValueError:
            raise ValidationError("Invalid level or slot number")

    def _verify_slot_occupied(self, lot_name: str, level: int, slot: int) -> bool:
        """Verify that the slot exists and is occupied"""
        try:
            statuses = self.parking_manager.get_lot_status(lot_name)
            for level_data in statuses:
                if level_data.level == level:  # Use level directly
                    for slot_data in level_data.slots:
                        if slot_data.slot_number == slot:
                            if not slot_data.is_occupied:
                                self.message_manager.show_error("Selected slot is empty")
                                return False
                            return True
            self.message_manager.show_error("Selected slot does not exist")
            return False
        except Exception as e:
            logger.error(f"Error verifying slot: {e}")
            raise OperationError("Error verifying slot status")

    def _handle_search(self):
        """Handle search button click"""
        try:
            # Create search criteria
            criteria = SearchCriteria(
                registration_number=self.state_manager.search_registration_number_value.get().strip(),
                color=self.state_manager.search_vehicle_color_value.get().strip(),
                manufacturer=self.state_manager.search_vehicle_manufacturer_value.get().strip(),
                model=self.state_manager.search_vehicle_model_value.get().strip()
            )
            
            # Clear previous results
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Search in all lots
            found_any = False
            for lot_name in self.parking_manager.get_lot_names():
                results = self.parking_manager.search_vehicles(lot_name, criteria)
                for status in results:
                    if status.vehicle:
                        self._add_vehicle_to_tree(status.vehicle, status.slot)
                        found_any = True
            
            if not found_any:
                self.message_manager.show_message("No vehicles found matching the search criteria")
            
        except ValidationError as e:
            self.message_manager.show_error(str(e))
        except OperationError as e:
            self.message_manager.show_error(str(e))
        except Exception as e:
            logger.error(f"Error performing search: {e}")
            self.message_manager.show_error("Error performing search")
    
    def _handle_create_lot(self):
        """Handle create lot button click"""
        try:
            lot_name = self.state_manager.lot_name_value.get()
            level_number = int(self.state_manager.parking_level_value.get())
            regular_slots = int(self.state_manager.regular_slots_value.get())
            electric_slots = int(self.state_manager.electric_vehicle_slots_value.get())
            
            # Create level data
            level_data = ParkingLevelData(
                level=level_number,
                slots=[
                    ParkingSlotData(slot_number=i+1, is_occupied=False, slot_type=SlotType.REGULAR)
                    for i in range(regular_slots)
                ] + [
                    ParkingSlotData(slot_number=regular_slots+i+1, is_occupied=False, slot_type=SlotType.ELECTRIC)
                    for i in range(electric_slots)
                ]
            )
            
            # Create lot data
            lot_data = ParkingLotData(
                name=lot_name,
                levels=[level_data]
            )
            
            # Validate data
            if not self.validation_manager.validate_lot_data(lot_data):
                return
            
            # Create parking lot
            if self.parking_manager.create_lot(lot_data):
                self.message_manager.show_message(f"Created parking lot {lot_name}")
                # Update all dropdowns
                self._update_park_lot_names()
                self._update_park_levels()
                self._update_details_lot_names()
                self._update_details_levels()
                self._update_remove_lot_names()
                # Set combo box values explicitly
                self.park_lot_combo['values'] = self.parking_manager.get_lot_names()
                self.park_level_combo['values'] = self.parking_manager.get_levels_for_lot(lot_name)
                self.details_lot_combo['values'] = self.parking_manager.get_lot_names()
                self.details_level_combo['values'] = self.parking_manager.get_levels_for_lot(lot_name)
                self.remove_lot_combo['values'] = self.parking_manager.get_lot_names()
            else:
                self.message_manager.show_error("Failed to create parking lot")
        except ValueError as e:
            self.message_manager.show_error(str(e))
    
    def _handle_show_lots(self) -> None:
        """Handle showing all parking lots"""
        try:
            lots = self.parking_manager.get_lot_names()
            
            # Clear previous results
            self.admin_tree.delete(*self.admin_tree.get_children())
            
            # Add each lot to the tree
            for lot_name in lots:
                levels = self.parking_manager.get_levels_for_lot(lot_name)
                
                # Get lot status
                statuses = self.parking_manager.get_lot_status(lot_name)
                
                # Calculate aggregations
                total_regular_capacity = 0
                total_ev_capacity = 0
                total_available_regular = 0
                total_available_ev = 0
                
                for level_data in statuses:
                    for slot in level_data.slots:
                        if slot.slot_type == SlotType.REGULAR:
                            total_regular_capacity += 1
                            if not slot.is_occupied:
                                total_available_regular += 1
                        elif slot.slot_type == SlotType.ELECTRIC:
                            total_ev_capacity += 1
                            if not slot.is_occupied:
                                total_available_ev += 1
                
                self.admin_tree.insert("", "end", values=(
                    lot_name,
                    len(levels),
                    total_regular_capacity,
                    total_ev_capacity,
                    total_available_regular,
                    total_available_ev
                ))
            
            # Switch to admin tab to show results
            self.notebook.select(self.admin_tab)  # type: ignore
            
        except Exception as e:
            logger.error(f"Error showing lots: {e}")
            self.message_manager.show_error("Error showing lots")
    
    def _get_selected_slot(self) -> Optional[int]:
        """Get the selected slot number from the tree view"""
        selection = self.results_tree.selection()
        if not selection:
            return None
        item = self.results_tree.item(selection[0])
        return int(item['values'][0])
    
    def _add_vehicle_to_tree(self, vehicle: Union[Vehicle, VehicleData], slot: int) -> None:
        """Add a vehicle to the results tree"""
        self.tree_manager.add_vehicle(vehicle, slot)
    
    def _clear_park_fields(self):
        """Clear vehicle input fields"""
        self.state_manager.registration_number_value.set("")
        self.state_manager.vehicle_manufacturer_value.set("")
        self.state_manager.vehicle_model_value.set("")
        self.state_manager.vehicle_color_value.set("")
        self.state_manager.vehicle_type_value.set("Car")
        self.state_manager.is_electric_value.set(False)
    
    def _show_message(self, message: str) -> None:
        """Show a message in the message area"""
        self.message_manager.show_message(message)
    
    def _show_error(self, message: str) -> None:
        """Show error message"""
        self.message_manager.show_error(message)
    
    def update(self, message: str):
        """Handle updates from the parking lot
        
        Args:
            message: The name of the lot that was updated
        """
        # Update UI state
        self._update_park_lot_names()
        self._update_remove_lot_names()
        self._update_details_lot_names()
        
        # Show status message
        status = self.parking_manager.get_lot_status(message)
        if status:
            self.message_manager.show_message(f"Updated status for lot: {message}")
            self._show_status()
    
    def run(self):
        """Run the UI"""
        self.main_window.mainloop()

    def _layout_widgets(self):
        """Layout UI widgets"""
        # Layout notebook
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout vehicle frame
        self.vehicle_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout search frame and results tree
        self.search_form_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.results_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
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
        self.load_sample_button.grid(row=4, column=2, padx=5, pady=5)
        self.admin_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout details frame
        self.details_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Layout message area
        self.message_area.pack(expand=True, fill="both", padx=5, pady=5)

    def _show_full_status(self) -> None:
        """Show full status of the parking lot"""
        try:
            selected_lot = self.state_manager.lot_name_value.get()
            selected_level = int(self.state_manager.parking_level_value.get())
            logger.debug(f"_show_full_status called with lot={selected_lot}, level={selected_level}")
            
            if not selected_lot:
                self.message_manager.show_error("Please select a parking lot")
                return
            
            # Clear previous results
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Get all vehicles in the lot
            vehicles: Dict[int, Vehicle] = self.parking_manager.get_vehicles_in_lot(selected_lot, selected_level)
            logger.debug(f"_show_full_status received {len(vehicles)} vehicles")
            for slot_number, vehicle in vehicles.items():
                self._add_vehicle_to_tree(vehicle, slot_number)
            
            if not self.results_tree.get_children():
                self.message_manager.show_message("No vehicles found in the selected lot and level.")
        
        except Exception as e:
            logger.error(f"Error showing full status: {str(e)}")
            self.message_manager.show_error(f"Error showing full status: {str(e)}")

    def _show_status(self) -> None:
        """Show parking lot status"""
        lot_name = self.state_manager.lot_name_value.get() or self.state_manager.park_lot_value.get()
        if not lot_name:
            self.message_manager.show_error("Please select a lot to show status.")
            return
        status = self.parking_manager.get_lot_status(lot_name)
        if isinstance(status, str):
            self.message_manager.show_message(status)
        else:
            self.message_manager.show_message(str(status))

    def create_lot(self):
        """Create a new parking lot"""
        self._handle_create_lot()

    def _update_details_lot_names(self):
        """Update the lot names in the details combo box"""
        lot_names = self.parking_manager.get_lot_names()
        self.details_lot_combo['values'] = lot_names
        if lot_names:
            self.state_manager.details_lot_name_value.set(lot_names[0])
            self._update_details_levels()

    def _update_park_levels(self):
        """Update the levels in the park combo box based on selected lot"""
        lot_name = self.state_manager.park_lot_value.get()
        if lot_name:
            levels = self.parking_manager.get_levels_for_lot(lot_name)
            self.park_level_combo['values'] = [str(level) for level in levels]
            self.remove_level_combo['values'] = [str(level) for level in levels]
            if levels:
                self.state_manager.park_level_value.set(str(levels[0]))
                self.state_manager.remove_level_value.set(str(levels[0]))
                self._update_slot_numbers(lot_name, levels[0])

    def _update_slot_numbers(self, lot_name: str, level: int):
        """Update the slot numbers in the remove combo box"""
        try:
            # Get all slots for the selected lot and level
            statuses = self.parking_manager.get_lot_status(lot_name)
            occupied_slots: List[str] = []
            
            for level_data in statuses:
                if level_data.level == level:
                    for slot in level_data.slots:
                        if slot.is_occupied:
                            occupied_slots.append(str(slot.slot_number))
            
            # Update the combo box
            self.remove_slot_combo['values'] = occupied_slots
            if occupied_slots:
                self.remove_slot_combo.set(occupied_slots[0])
            else:
                self.remove_slot_combo.set('')
            
        except Exception as e:
            logger.error(f"Error updating slot numbers: {e}")
            self.message_manager.show_error("Error updating slot numbers")

    def _update_details_levels(self):
        """Update the levels in the details combo box based on selected lot"""
        lot_name = self.state_manager.details_lot_name_value.get()
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
            lot_name = self.state_manager.details_lot_name_value.get()
            filter_type = self.state_manager.details_filter_value.get()
            
            if not lot_name:
                self.message_manager.show_error("Please select a lot")
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
                level = int(self.state_manager.details_parking_level_value.get())
                self._add_level_details(lot_name, level, filter_type)
            
            if not self.details_tree.get_children():
                self.message_manager.show_message("No slots found matching the criteria.")
                
        except Exception as e:
            logger.error(f"Error showing details: {e}")
            self.message_manager.show_error("Error showing lot details")

    def _add_level_details(self, lot_name: str, level: int, filter_type: str = "All Slots") -> None:
        """Add details for a specific level to the tree"""
        try:
            # Get status for this level
            statuses: List[ParkingLevelData] = self.parking_manager.get_lot_status(lot_name)
            
            for level_data in statuses:
                if level_data.level != level:
                    continue
                    
                for slot in level_data.slots:
                    # Apply filter
                    if filter_type == "Available Slots" and slot.is_occupied:
                        continue
                    if filter_type == "Occupied Slots" and not slot.is_occupied:
                        continue
                    
                    # Get slot details
                    slot_status: str = "Occupied" if slot.is_occupied else "Available"
                    registration: str = slot.vehicle.registration_number if slot.vehicle else ""
                    manufacturer: str = slot.vehicle.manufacturer if slot.vehicle else ""
                    model: str = slot.vehicle.model if slot.vehicle else ""
                    color: str = slot.vehicle.color if slot.vehicle else ""
                    slot_type: str = "EV" if slot.slot_type == SlotType.ELECTRIC else "Standard"
                    vehicle_type: str = self._get_vehicle_type_display(slot.vehicle) if slot.vehicle else "Unknown"
                    charge_status: str = self._get_battery_charge_display(slot.vehicle) if slot.vehicle else "N/A"
                    
                    values: Tuple[str, ...] = (
                        str(level),
                        str(slot.slot_number),
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
            self.state_manager.park_lot_value.set(lot_names[0])
            self._update_park_levels()

    def _get_vehicle_type(self) -> VehicleType:
        """Get the vehicle type based on UI selections"""
        type_str = self.state_manager.vehicle_type_value.get()
        return VehicleType.from_string(type_str)

    def _handle_load_sample_data(self):
        """Handle loading sample data button click"""
        try:
            # Create Downtown Parking Lot with 2 levels
            downtown_lot = ParkingLotData(
                name="Downtown",
                levels=[
                    # Level 1
                    ParkingLevelData(
                        level=1,
                        slots=[
                            ParkingSlotData(slot_number=i+1, is_occupied=False, slot_type=SlotType.REGULAR)
                            for i in range(15)
                        ] + [
                            ParkingSlotData(slot_number=i+16, is_occupied=False, slot_type=SlotType.ELECTRIC)
                            for i in range(5)
                        ]
                    ),
                    # Level 2
                    ParkingLevelData(
                        level=2,
                        slots=[
                            ParkingSlotData(slot_number=i+1, is_occupied=False, slot_type=SlotType.REGULAR)
                            for i in range(20)
                        ] + [
                            ParkingSlotData(slot_number=i+21, is_occupied=False, slot_type=SlotType.ELECTRIC)
                            for i in range(8)
                        ]
                    )
                ]
            )
            
            # Create Airport Parking Lot with 2 levels
            airport_lot = ParkingLotData(
                name="Airport",
                levels=[
                    # Level 1
                    ParkingLevelData(
                        level=1,
                        slots=[
                            ParkingSlotData(slot_number=i+1, is_occupied=False, slot_type=SlotType.REGULAR)
                            for i in range(25)
                        ] + [
                            ParkingSlotData(slot_number=i+26, is_occupied=False, slot_type=SlotType.ELECTRIC)
                            for i in range(10)
                        ]
                    ),
                    # Level 2
                    ParkingLevelData(
                        level=2,
                        slots=[
                            ParkingSlotData(slot_number=i+1, is_occupied=False, slot_type=SlotType.REGULAR)
                            for i in range(30)
                        ] + [
                            ParkingSlotData(slot_number=i+31, is_occupied=False, slot_type=SlotType.ELECTRIC)
                            for i in range(15)
                        ]
                    )
                ]
            )
            
            # Create lots
            self.parking_manager.create_lot(downtown_lot)
            self.parking_manager.create_lot(airport_lot)
            
            # Create sample vehicles for Downtown lot
            downtown_vehicles = [
                # Level 1 vehicles
                VehicleData(
                    registration_number="DTN001",
                    manufacturer="Toyota",
                    model="Camry",
                    color="Red",
                    is_electric=False,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.CAR
                ),
                VehicleData(
                    registration_number="DTN002",
                    manufacturer="Tesla",
                    model="Model 3",
                    color="Black",
                    is_electric=True,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.CAR
                ),
                VehicleData(
                    registration_number="DTN003",
                    manufacturer="Honda",
                    model="CBR",
                    color="Blue",
                    is_electric=False,
                    is_motorcycle=True,
                    vehicle_type=VehicleType.MOTORCYCLE
                ),
                VehicleData(
                    registration_number="DTN004",
                    manufacturer="Zero",
                    model="SR",
                    color="White",
                    is_electric=True,
                    is_motorcycle=True,
                    vehicle_type=VehicleType.MOTORCYCLE
                ),
                # Level 2 vehicles
                VehicleData(
                    registration_number="DTN005",
                    manufacturer="Ford",
                    model="F-150",
                    color="Silver",
                    is_electric=False,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.TRUCK
                ),
                VehicleData(
                    registration_number="DTN006",
                    manufacturer="Rivian",
                    model="R1T",
                    color="Green",
                    is_electric=True,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.TRUCK
                )
            ]

            # Create sample vehicles for Airport lot
            airport_vehicles = [
                # Level 1 vehicles
                VehicleData(
                    registration_number="AIR001",
                    manufacturer="Mercedes",
                    model="Sprinter",
                    color="White",
                    is_electric=False,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.BUS
                ),
                VehicleData(
                    registration_number="AIR002",
                    manufacturer="BYD",
                    model="K9",
                    color="Blue",
                    is_electric=True,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.BUS
                ),
                VehicleData(
                    registration_number="AIR003",
                    manufacturer="Harley-Davidson",
                    model="Street Bob",
                    color="Black",
                    is_electric=False,
                    is_motorcycle=True,
                    vehicle_type=VehicleType.MOTORCYCLE
                ),
                VehicleData(
                    registration_number="AIR004",
                    manufacturer="LiveWire",
                    model="One",
                    color="Orange",
                    is_electric=True,
                    is_motorcycle=True,
                    vehicle_type=VehicleType.MOTORCYCLE
                ),
                # Level 2 vehicles
                VehicleData(
                    registration_number="AIR005",
                    manufacturer="Chevrolet",
                    model="Silverado",
                    color="Gray",
                    is_electric=False,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.TRUCK
                ),
                VehicleData(
                    registration_number="AIR006",
                    manufacturer="Tesla",
                    model="Cybertruck",
                    color="Silver",
                    is_electric=True,
                    is_motorcycle=False,
                    vehicle_type=VehicleType.TRUCK
                )
            ]

            # Park vehicles in Downtown lot
            for vehicle in downtown_vehicles[:4]:  # First 4 vehicles in Level 1
                slot = self.parking_manager.park_vehicle("Downtown", 1, vehicle)
                if slot is None:
                    logger.error(f"Failed to park vehicle {vehicle.registration_number}")
            
            for vehicle in downtown_vehicles[4:]:  # Last 2 vehicles in Level 2
                slot = self.parking_manager.park_vehicle("Downtown", 2, vehicle)
                if slot is None:
                    logger.error(f"Failed to park vehicle {vehicle.registration_number}")

            # Park vehicles in Airport lot
            for vehicle in airport_vehicles[:4]:  # First 4 vehicles in Level 1
                slot = self.parking_manager.park_vehicle("Airport", 1, vehicle)
                if slot is None:
                    logger.error(f"Failed to park vehicle {vehicle.registration_number}")
            
            for vehicle in airport_vehicles[4:]:  # Last 2 vehicles in Level 2
                slot = self.parking_manager.park_vehicle("Airport", 2, vehicle)
                if slot is None:
                    logger.error(f"Failed to park vehicle {vehicle.registration_number}")

            # Update UI
            self._update_park_lot_names()
            self._update_park_levels()
            self._update_details_lot_names()
            self._update_details_levels()
            self._update_remove_lot_names()
            
            # Show success message
            self.message_manager.show_message("Sample data loaded successfully")
            
            # Refresh the lots display
            self._handle_show_lots()
            
        except Exception as e:
            logger.error(f"Error loading sample data: {e}")
            self.message_manager.show_error(f"Error loading sample data: {str(e)}")

    def _update_remove_lot_names(self):
        """Update the lot names in the remove combo box"""
        try:
            logger.debug("[DEBUG] Starting _update_remove_lot_names")
            lot_names = self.parking_manager.get_lot_names()
            logger.debug(f"[DEBUG] Retrieved lot names: {lot_names}")
            
            if lot_names:
                logger.debug(f"[DEBUG] Setting lot names in combo box: {lot_names}")
                self.remove_lot_combo['values'] = lot_names
                self.state_manager.remove_lot_value.set(lot_names[0])
                logger.debug(f"[DEBUG] Selected first lot: {lot_names[0]}")
                self._update_remove_levels(lot_names[0])
            else:
                logger.debug("[DEBUG] No lot names available")
                self.remove_lot_combo['values'] = []
                self.state_manager.remove_lot_value.set('')
                self.remove_level_combo['values'] = []
                self.state_manager.remove_level_value.set('')
                self.remove_slot_combo['values'] = []
                self.state_manager.remove_slot_value.set('')
        except Exception as e:
            logger.error(f"[DEBUG] Error in _update_remove_lot_names: {e}")
            self.message_manager.show_error("Error updating lot names")

    def _update_remove_levels(self, lot_name: str):
        """Update the levels in the remove combo box based on selected lot"""
        try:
            logger.debug(f"[DEBUG] Starting _update_remove_levels for lot: {lot_name}")
            levels = self.parking_manager.get_levels_for_lot(lot_name)
            logger.debug(f"[DEBUG] Retrieved levels: {levels}")
            
            if levels:
                level_values = [str(level) for level in levels]
                logger.debug(f"[DEBUG] Setting level values in combo box: {level_values}")
                self.remove_level_combo['values'] = level_values
                self.state_manager.remove_level_value.set(str(levels[0]))
                logger.debug(f"[DEBUG] Selected first level: {levels[0]}")
                self._update_remove_slots(lot_name, levels[0])
            else:
                logger.debug("[DEBUG] No levels available")
                self.remove_level_combo['values'] = []
                self.state_manager.remove_level_value.set('')
                self.remove_slot_combo['values'] = []
                self.state_manager.remove_slot_value.set('')
        except Exception as e:
            logger.error(f"[DEBUG] Error in _update_remove_levels: {e}")
            self.message_manager.show_error("Error updating levels")

    def _update_remove_slots(self, lot_name: str, level: int) -> None:
        """Update the slot numbers in the remove combo box"""
        try:
            logger.debug(f"Updating remove slots for lot: {lot_name}, level: {level}")
            # Get all slots for the selected lot and level
            statuses = self.parking_manager.get_lot_status(lot_name)
            
            occupied_slots: List[str] = []
            for level_data in statuses:
                if level_data.level == level:
                    for slot in level_data.slots:
                        if slot.is_occupied:
                            occupied_slots.append(str(slot.slot_number))
                            logger.debug(f"Found occupied slot: {slot.slot_number}")
            
            logger.debug(f"Found {len(occupied_slots)} occupied slots")
            
            # Update the combo box
            if occupied_slots:
                self.remove_slot_combo['values'] = occupied_slots
                self.state_manager.remove_slot_value.set(occupied_slots[0])
                self._update_vehicle_info(lot_name, level, int(occupied_slots[0]))
            else:
                self.remove_slot_combo['values'] = []
                self.state_manager.remove_slot_value.set('')
                self.vehicle_info_label.config(text="No vehicles in selected level")
            
        except Exception as e:
            logger.error(f"Error updating slot numbers: {e}")
            self.message_manager.show_error("Error updating slot numbers")

    def _update_vehicle_info(self, lot_name: str, level: int, slot: int) -> None:
        """Update the vehicle information display"""
        try:
            statuses: List[ParkingLevelData] = self.parking_manager.get_lot_status(lot_name)
            for level_data in statuses:
                if level_data.level == level:
                    for slot_data in level_data.slots:
                        if slot_data.slot_number == slot and slot_data.vehicle:
                            vehicle = slot_data.vehicle
                            vehicle_type = self._get_vehicle_type_display(vehicle)
                            info_text: str = (
                                f"Vehicle Information:\n"
                                f"Registration: {vehicle.registration_number}\n"
                                f"Manufacturer: {vehicle.manufacturer}\n"
                                f"Model: {vehicle.model}\n"
                                f"Color: {vehicle.color}\n"
                                f"Type: {vehicle_type}"
                            )
                            if vehicle.is_electric:
                                info_text += f"\nBattery Charge: {self._get_battery_charge_display(vehicle)}"
                            self.vehicle_info_label.config(text=info_text)
                            return
            self.vehicle_info_label.config(text="No vehicle found in selected slot")
        except Exception as e:
            logger.error(f"Error updating vehicle info: {e}")
            self.vehicle_info_label.config(text="Error loading vehicle information")

    def _on_remove_lot_selected(self, event: Any) -> None:
        """Handle lot selection in remove section"""
        try:
            lot_name = self.state_manager.remove_lot_value.get()
            if lot_name:
                self._update_remove_levels(lot_name)
        except Exception as e:
            logger.error(f"Error in _on_remove_lot_selected: {e}")
            self.message_manager.show_error("Error updating levels")

    def _on_remove_level_selected(self, event: Any) -> None:
        """Handle level selection in remove section"""
        try:
            lot_name = self.state_manager.remove_lot_value.get()
            level_str = self.state_manager.remove_level_value.get()
            if lot_name and level_str:
                self._update_remove_slots(lot_name, int(level_str))
        except Exception as e:
            logger.error(f"Error in _on_remove_level_selected: {e}")
            self.message_manager.show_error("Error updating slots")

    def _on_remove_slot_selected(self, event: Any) -> None:
        """Handle slot selection in remove section"""
        try:
            lot_name = self.state_manager.remove_lot_value.get()
            level_str = self.state_manager.remove_level_value.get()
            slot_str = self.state_manager.remove_slot_value.get()
            if lot_name and level_str and slot_str:
                self._update_vehicle_info(lot_name, int(level_str), int(slot_str))
        except Exception as e:
            logger.error(f"Error in _on_remove_slot_selected: {e}")
            self.message_manager.show_error("Error updating vehicle info")

    def _is_motorcycle(self, vehicle: VehicleData) -> bool:
        """Check if vehicle is a motorcycle"""
        return vehicle.vehicle_type == VehicleType.MOTORCYCLE

    def _get_vehicle_type_display(self, vehicle: Union[Vehicle, VehicleData]) -> str:
        """Get display string for vehicle type"""
        if not vehicle:
            return "Unknown"
            
        is_ev = vehicle.is_electric
        vehicle_type = vehicle.vehicle_type
        
        type_map = {
            VehicleType.MOTORCYCLE: "Motorcycle",
            VehicleType.CAR: "Car",
            VehicleType.TRUCK: "Truck",
            VehicleType.BUS: "Bus"
        }
        
        base_type = type_map.get(vehicle_type, "Unknown")
        return f"Electric {base_type}" if is_ev else base_type

    def _get_battery_charge_display(self, vehicle: Union[Vehicle, VehicleData]) -> str:
        """Get display string for battery charge"""
        if not vehicle or not vehicle.is_electric:
            return "N/A"
            
        if hasattr(vehicle, 'current_battery_charge') and vehicle.current_battery_charge is not None:
            return f"{vehicle.current_battery_charge:.1f}%"
            
        return "N/A"

    def _get_vehicle_type_from_ui(self) -> VehicleType:
        """Get vehicle type from UI selection"""
        type_str = self.state_manager.vehicle_type_value.get()
        return VehicleType.from_string(type_str)

    def _create_vehicle_data(self) -> VehicleData:
        """Get vehicle data from UI fields"""
        try:
            vehicle_type = self._get_vehicle_type()
            is_motorcycle = vehicle_type == VehicleType.MOTORCYCLE
            return VehicleData(
                registration_number=self.state_manager.registration_number_value.get().strip(),
                manufacturer=self.state_manager.vehicle_manufacturer_value.get().strip(),
                model=self.state_manager.vehicle_model_value.get().strip(),
                color=self.state_manager.vehicle_color_value.get().strip(),
                is_electric=self.state_manager.is_electric_value.get(),
                is_motorcycle=is_motorcycle,
                vehicle_type=vehicle_type
            )
        except Exception as e:
            raise ValidationError(f"Error getting vehicle data: {e}")

    def _update_results_tree(self, results: List[SearchResult]) -> None:
        """Update search results tree"""
        self.results_tree.delete(*self.results_tree.get_children())
        for result in results:
            vehicle_type = self._get_vehicle_type_display(result.vehicle)
            self.results_tree.insert(
                "",
                "end",
                values=(
                    result.slot,
                    result.vehicle.registration_number,
                    result.vehicle.manufacturer,
                    result.vehicle.model,
                    result.vehicle.color,
                    "Electric" if result.vehicle.is_electric else "Regular",
                    vehicle_type,
                    f"{result.vehicle.current_battery_charge:.1f}%" if result.vehicle.is_electric else "N/A"
                )
            )


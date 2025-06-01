"""
Application Services Layer

This module contains the application services that orchestrate business operations
and coordinate between the domain and infrastructure layers.
"""

from typing import List, Optional, Dict, Any
from dataclasses import asdict

from domain.entities import Vehicle, VehicleType, SlotType
from domain.value_objects import SearchCriteria, SearchResult, ParkingSlot, ParkingLevelInfo
from config.exceptions import ValidationError, OperationError, ParkingSystemError
from infrastructure.interfaces import (
    ParkingLotService, VehicleFactory, NotificationService, 
    ParkingLotObserver, ParkingLotRepository
)
from infrastructure.services import (
    ConcreteParkingLotService, StandardVehicleFactory, 
    FileBasedParkingLotRepository, ConsoleNotificationService,
    ConsoleParkingLotObserver
)


class ParkingApplicationService:
    """
    Main application service that coordinates parking operations.
    This is the entry point for all parking-related business operations.
    """
    
    def __init__(self, 
                 parking_service: Optional[ParkingLotService] = None,
                 vehicle_factory: Optional[VehicleFactory] = None,
                 notification_service: Optional[NotificationService] = None):
        """Initialize with dependency injection or defaults"""
        
        # Use dependency injection or create defaults
        self.notification_service = notification_service or ConsoleNotificationService()
        self.vehicle_factory = vehicle_factory or StandardVehicleFactory()
        
        if parking_service:
            self.parking_service = parking_service
        else:
            # Create default infrastructure
            repository = FileBasedParkingLotRepository()
            observer = ConsoleParkingLotObserver()
            self.parking_service = ConcreteParkingLotService(
                repository=repository,
                notification_service=self.notification_service,
                observers=[observer]
            )
    
    def create_parking_lot(self, name: str, levels: int, slots_per_level: int, 
                          electric_ratio: float = 0.2) -> bool:
        """
        Create a new parking lot with specified configuration.
        
        Args:
            name: Name of the parking lot
            levels: Number of levels in the parking lot
            slots_per_level: Number of parking slots per level
            electric_ratio: Ratio of electric charging slots (0.0 to 1.0)
        
        Returns:
            True if successful, False otherwise
        
        Raises:
            ValidationError: If input parameters are invalid
            OperationError: If creation fails
        """
        try:
            # Validate inputs
            if not name or not name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            if levels <= 0:
                raise ValidationError("Number of levels must be positive")
            
            if slots_per_level <= 0:
                raise ValidationError("Slots per level must be positive")
            
            if not 0 <= electric_ratio <= 1:
                raise ValidationError("Electric ratio must be between 0 and 1")
            
            return self.parking_service.create_parking_lot(
                name.strip(), levels, slots_per_level, electric_ratio
            )
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error creating parking lot: {str(e)}")
    
    def park_vehicle(self, lot_name: str, level: int, vehicle_data: Dict[str, Any]) -> Optional[int]:
        """
        Park a vehicle in the specified parking lot and level.
        
        Args:
            lot_name: Name of the parking lot
            level: Level to park in (0-based)
            vehicle_data: Dictionary containing vehicle information
        
        Returns:
            Slot number where vehicle was parked, or None if parking failed
        
        Raises:
            ValidationError: If input parameters are invalid
            OperationError: If parking operation fails
        """
        try:
            # Create vehicle from data
            vehicle = self.vehicle_factory.create_vehicle(vehicle_data)
            
            # Validate lot name and level
            if not lot_name or not lot_name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            if level < 0:
                raise ValidationError("Level must be non-negative")
            
            return self.parking_service.park_vehicle(lot_name.strip(), level, vehicle)
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error parking vehicle: {str(e)}")
    
    def remove_vehicle(self, lot_name: str, level: int, slot: int) -> Optional[Dict[str, Any]]:
        """
        Remove a vehicle from the specified location.
        
        Args:
            lot_name: Name of the parking lot
            level: Level where vehicle is parked
            slot: Slot number where vehicle is parked
        
        Returns:
            Dictionary containing removed vehicle data, or None if no vehicle found
        
        Raises:
            ValidationError: If input parameters are invalid
            OperationError: If removal operation fails
        """
        try:
            # Validate inputs
            if not lot_name or not lot_name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            if level < 0:
                raise ValidationError("Level must be non-negative")
            
            if slot <= 0:
                raise ValidationError("Slot number must be positive")
            
            vehicle = self.parking_service.remove_vehicle(lot_name.strip(), level, slot)
            
            if vehicle:
                return {
                    'license_plate': vehicle.license_plate,
                    'vehicle_type': vehicle.vehicle_type.value,
                    'is_electric': vehicle.is_electric,
                    'owner_name': vehicle.owner_name
                }
            
            return None
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error removing vehicle: {str(e)}")
    
    def find_vehicles(self, lot_name: str, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find vehicles in the parking lot matching the search criteria.
        
        Args:
            lot_name: Name of the parking lot to search
            search_params: Dictionary containing search criteria
        
        Returns:
            List of dictionaries containing search results
        
        Raises:
            ValidationError: If input parameters are invalid
            OperationError: If search operation fails
        """
        try:
            if not lot_name or not lot_name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            # Create search criteria
            criteria = SearchCriteria(
                license_plate=search_params.get('license_plate'),
                vehicle_type=VehicleType(search_params['vehicle_type']) if search_params.get('vehicle_type') else None,
                owner_name=search_params.get('owner_name'),
                is_electric=search_params.get('is_electric'),
                slot_type=SlotType(search_params['slot_type']) if search_params.get('slot_type') else None
            )
            
            results = self.parking_service.find_vehicles(lot_name.strip(), criteria)
            
            # Convert results to dictionaries
            result_dicts = []
            for result in results:
                result_dict = {
                    'lot_name': result.lot_name,
                    'level': result.level,
                    'slot_number': result.slot,
                    'vehicle': {
                        'license_plate': result.vehicle.license_plate,
                        'vehicle_type': result.vehicle.vehicle_type.value,
                        'is_electric': result.vehicle.is_electric,
                        'owner_name': result.vehicle.owner_name
                    }
                }
                result_dicts.append(result_dict)
            
            return result_dicts
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error searching vehicles: {str(e)}")
    
    def get_parking_lot_info(self, lot_name: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a parking lot.
        
        Args:
            lot_name: Name of the parking lot
        
        Returns:
            Dictionary containing parking lot information
        
        Raises:
            ValidationError: If lot name is invalid
            OperationError: If operation fails
        """
        try:
            if not lot_name or not lot_name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            lot_status = self.parking_service.get_lot_status(lot_name.strip())
            
            # Calculate statistics
            total_slots = 0
            occupied_slots = 0
            electric_slots = 0
            regular_slots = 0
            
            level_info = []
            
            for level_num, level_slots in lot_status.items():
                level_total = len(level_slots)
                level_occupied = sum(1 for slot in level_slots if slot.is_occupied)
                level_electric = sum(1 for slot in level_slots if slot.slot_type == SlotType.ELECTRIC)
                level_regular = level_total - level_electric
                
                level_info.append({
                    'level': level_num,
                    'total_slots': level_total,
                    'occupied_slots': level_occupied,
                    'available_slots': level_total - level_occupied,
                    'electric_slots': level_electric,
                    'regular_slots': level_regular,
                    'occupancy_rate': level_occupied / level_total if level_total > 0 else 0
                })
                
                total_slots += level_total
                occupied_slots += level_occupied
                electric_slots += level_electric
                regular_slots += level_regular
            
            return {
                'lot_name': lot_name.strip(),
                'total_levels': len(lot_status),
                'total_slots': total_slots,
                'occupied_slots': occupied_slots,
                'available_slots': total_slots - occupied_slots,
                'electric_slots': electric_slots,
                'regular_slots': regular_slots,
                'overall_occupancy_rate': occupied_slots / total_slots if total_slots > 0 else 0,
                'levels': level_info
            }
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error getting lot info: {str(e)}")
    
    def get_available_parking_lots(self) -> List[str]:
        """
        Get a list of all available parking lots.
        
        Returns:
            List of parking lot names
        
        Raises:
            OperationError: If operation fails
        """
        try:
            return self.parking_service.get_available_lots()
        except Exception as e:
            raise OperationError(f"Unexpected error getting available lots: {str(e)}")
    
    def get_level_details(self, lot_name: str, level: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific level in a parking lot.
        
        Args:
            lot_name: Name of the parking lot
            level: Level number
        
        Returns:
            Dictionary containing level details
        
        Raises:
            ValidationError: If input parameters are invalid
            OperationError: If operation fails
        """
        try:
            if not lot_name or not lot_name.strip():
                raise ValidationError("Parking lot name cannot be empty")
            
            if level < 0:
                raise ValidationError("Level must be non-negative")
            
            lot_status = self.parking_service.get_lot_status(lot_name.strip())
            
            if level not in lot_status:
                raise ValidationError(f"Level {level} not found in parking lot '{lot_name}'")
            
            level_slots = lot_status[level]
            
            slots_info = []
            for slot in level_slots:
                slot_info = {
                    'slot_number': slot.slot_number,
                    'slot_type': slot.slot_type.value,
                    'is_occupied': slot.is_occupied,
                    'vehicle': None
                }
                
                if slot.vehicle:
                    slot_info['vehicle'] = {
                        'license_plate': slot.vehicle.license_plate,
                        'vehicle_type': slot.vehicle.vehicle_type.value,
                        'is_electric': slot.vehicle.is_electric,
                        'owner_name': slot.vehicle.owner_name
                    }
                
                slots_info.append(slot_info)
            
            # Calculate level statistics
            total_slots = len(level_slots)
            occupied_slots = sum(1 for slot in level_slots if slot.is_occupied)
            electric_slots = sum(1 for slot in level_slots if slot.slot_type == SlotType.ELECTRIC)
            
            return {
                'lot_name': lot_name.strip(),
                'level': level,
                'total_slots': total_slots,
                'occupied_slots': occupied_slots,
                'available_slots': total_slots - occupied_slots,
                'electric_slots': electric_slots,
                'regular_slots': total_slots - electric_slots,
                'occupancy_rate': occupied_slots / total_slots if total_slots > 0 else 0,
                'slots': slots_info
            }
            
        except (ValidationError, OperationError):
            raise
        except Exception as e:
            raise OperationError(f"Unexpected error getting level details: {str(e)}")


class VehicleManagementService:
    """Service for vehicle-related operations"""
    
    def __init__(self, vehicle_factory: Optional[VehicleFactory] = None):
        """Initialize with dependency injection or defaults"""
        self.vehicle_factory = vehicle_factory or StandardVehicleFactory()
    
    def validate_vehicle_data(self, vehicle_data: Dict[str, Any]) -> bool:
        """
        Validate vehicle data without creating a vehicle instance.
        
        Args:
            vehicle_data: Dictionary containing vehicle data
        
        Returns:
            True if valid, False otherwise
        """
        try:
            # Try to create vehicle - will raise ValidationError if invalid
            self.vehicle_factory.create_vehicle(vehicle_data)
            return True
        except ValidationError:
            return False
    
    def get_supported_vehicle_types(self) -> List[str]:
        """Get list of supported vehicle types"""
        return [vtype.value for vtype in VehicleType]
    
    def get_supported_slot_types(self) -> List[str]:
        """Get list of supported slot types"""
        return [stype.value for stype in SlotType]


# Convenience factory function for creating the main application service
def create_parking_application() -> ParkingApplicationService:
    """
    Factory function to create a fully configured parking application service.
    
    Returns:
        Configured ParkingApplicationService instance
    """
    return ParkingApplicationService()

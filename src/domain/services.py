"""
Domain Services Module

Contains pure business logic and domain services that encapsulate complex
business rules and operations. These services don't depend on infrastructure
concerns and focus purely on business logic.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

from domain.entities import Vehicle, VehicleType, SlotType
from domain.value_objects import ParkingSlot, SearchCriteria, SearchResult
from config.exceptions import ValidationError, OperationError


class ParkingStrategy(ABC):
    """Abstract strategy for parking allocation algorithms"""
    
    @abstractmethod
    def find_suitable_slot(self, slots: List[ParkingSlot], vehicle: Vehicle) -> Optional[ParkingSlot]:
        """Find a suitable parking slot for the vehicle"""
        pass


class FirstAvailableStrategy(ParkingStrategy):
    """Find the first available suitable slot"""
    
    def find_suitable_slot(self, slots: List[ParkingSlot], vehicle: Vehicle) -> Optional[ParkingSlot]:
        """Find the first available slot that matches vehicle requirements"""
        for slot in slots:
            if not slot.is_occupied and vehicle.can_park_in_slot_type(slot.slot_type):
                return slot
        return None


class PreferredSlotTypeStrategy(ParkingStrategy):
    """Prefer slots of specific type (e.g., electric vehicles prefer electric slots)"""
    
    def find_suitable_slot(self, slots: List[ParkingSlot], vehicle: Vehicle) -> Optional[ParkingSlot]:
        """Find slot preferring vehicle's preferred slot type"""
        # First pass: look for preferred slot type
        preferred_slots = []
        fallback_slots = []
        
        for slot in slots:
            if slot.is_occupied:
                continue
                
            if vehicle.can_park_in_slot_type(slot.slot_type):
                if self._is_preferred_slot(vehicle, slot.slot_type):
                    preferred_slots.append(slot)
                else:
                    fallback_slots.append(slot)
        
        # Return preferred slot if available, otherwise fallback
        if preferred_slots:
            return preferred_slots[0]
        elif fallback_slots:
            return fallback_slots[0]
        
        return None
    
    def _is_preferred_slot(self, vehicle: Vehicle, slot_type: SlotType) -> bool:
        """Check if slot type is preferred for the vehicle"""
        if vehicle.is_electric and slot_type == SlotType.ELECTRIC:
            return True
        if vehicle.vehicle_type == VehicleType.MOTORCYCLE and slot_type == SlotType.COMPACT:
            return True
        return False


class ParkingCapacityService:
    """Service for managing parking capacity and availability"""
    
    @staticmethod
    def calculate_capacity_metrics(slots: List[ParkingSlot]) -> Dict[str, int]:
        """Calculate capacity metrics for a list of slots"""
        total_slots = len(slots)
        occupied_slots = sum(1 for slot in slots if slot.is_occupied)
        available_slots = total_slots - occupied_slots
        
        regular_slots = sum(1 for slot in slots if slot.slot_type == SlotType.REGULAR)
        electric_slots = sum(1 for slot in slots if slot.slot_type == SlotType.ELECTRIC)
        handicapped_slots = sum(1 for slot in slots if slot.slot_type == SlotType.HANDICAPPED)
        compact_slots = sum(1 for slot in slots if slot.slot_type == SlotType.COMPACT)
        
        occupied_regular = sum(1 for slot in slots 
                              if slot.is_occupied and slot.slot_type == SlotType.REGULAR)
        occupied_electric = sum(1 for slot in slots 
                               if slot.is_occupied and slot.slot_type == SlotType.ELECTRIC)
        occupied_handicapped = sum(1 for slot in slots 
                                  if slot.is_occupied and slot.slot_type == SlotType.HANDICAPPED)
        occupied_compact = sum(1 for slot in slots 
                              if slot.is_occupied and slot.slot_type == SlotType.COMPACT)
        
        return {
            'total_slots': total_slots,
            'occupied_slots': occupied_slots,
            'available_slots': available_slots,
            'occupancy_percentage': round((occupied_slots / total_slots * 100) if total_slots > 0 else 0, 2),
            'regular_slots': regular_slots,
            'electric_slots': electric_slots,
            'handicapped_slots': handicapped_slots,
            'compact_slots': compact_slots,
            'occupied_regular': occupied_regular,
            'occupied_electric': occupied_electric,
            'occupied_handicapped': occupied_handicapped,
            'occupied_compact': occupied_compact,
            'available_regular': regular_slots - occupied_regular,
            'available_electric': electric_slots - occupied_electric,
            'available_handicapped': handicapped_slots - occupied_handicapped,
            'available_compact': compact_slots - occupied_compact,
        }
    
    @staticmethod
    def check_availability_for_vehicle(slots: List[ParkingSlot], vehicle: Vehicle) -> bool:
        """Check if there are available slots for a specific vehicle type"""
        for slot in slots:
            if not slot.is_occupied and vehicle.can_park_in_slot_type(slot.slot_type):
                return True
        return False


class VehicleSearchService:
    """Service for vehicle search operations"""
    
    @staticmethod
    def find_vehicles_by_criteria(
        lot_name: str,
        levels: Dict[int, List[ParkingSlot]], 
        criteria: SearchCriteria
    ) -> List[SearchResult]:
        """Find vehicles matching search criteria"""
        results = []
        
        for level_num, slots in levels.items():
            for slot in slots:
                if slot.is_occupied and slot.vehicle:
                    if VehicleSearchService._matches_criteria(slot.vehicle, criteria):
                        result = SearchResult(
                            lot_name=lot_name,
                            level=level_num,
                            slot=slot.slot_number,
                            vehicle=slot.vehicle
                        )
                        results.append(result)
        
        return results
    
    @staticmethod
    def _matches_criteria(vehicle: Vehicle, criteria: SearchCriteria) -> bool:
        """Check if vehicle matches search criteria"""
        return criteria.matches(vehicle)


class ParkingValidationService:
    """Service for parking business rule validation"""
    
    @staticmethod
    def validate_parking_lot_creation(
        name: str, 
        levels: int, 
        slots_per_level: int, 
        electric_ratio: float
    ) -> None:
        """Validate parking lot creation parameters"""
        if not name or not name.strip():
            raise ValidationError("Parking lot name is required")
        
        if levels <= 0:
            raise ValidationError("Number of levels must be positive")
        
        if slots_per_level <= 0:
            raise ValidationError("Number of slots per level must be positive")
        
        if not 0 <= electric_ratio <= 1:
            raise ValidationError("Electric slot ratio must be between 0 and 1")
        
        if levels > 50:  # Business rule: max 50 levels
            raise ValidationError("Maximum 50 levels allowed per parking lot")
        
        if slots_per_level > 1000:  # Business rule: max 1000 slots per level
            raise ValidationError("Maximum 1000 slots allowed per level")
    
    @staticmethod
    def validate_vehicle_parking(vehicle: Vehicle, available_slots: List[ParkingSlot]) -> None:
        """Validate that vehicle can be parked"""
        if not available_slots:
            raise OperationError("No available parking slots")
        
        # Check if any slot is suitable for this vehicle type
        suitable_slots = [
            slot for slot in available_slots 
            if not slot.is_occupied and vehicle.can_park_in_slot_type(slot.slot_type)
        ]
        
        if not suitable_slots:
            vehicle_desc = f"{vehicle.vehicle_type.value}"
            if vehicle.is_electric:
                vehicle_desc += " electric"
            raise OperationError(f"No suitable slots available for {vehicle_desc} vehicle")
    
    @staticmethod
    def validate_vehicle_removal(slot: ParkingSlot) -> None:
        """Validate that vehicle can be removed from slot"""
        if not slot.is_occupied:
            raise OperationError("Cannot remove vehicle from empty slot")
        
        if slot.vehicle is None:
            raise OperationError("Slot marked as occupied but no vehicle data found")


class ParkingLotLayoutService:
    """Service for parking lot layout and slot arrangement"""
    
    @staticmethod
    def create_level_layout(
        level: int,
        regular_slots: int, 
        electric_slots: int,
        handicapped_slots: int = 0,
        compact_slots: int = 0
    ) -> List[ParkingSlot]:
        """Create a parking level layout with specified slot types"""
        if any(count < 0 for count in [regular_slots, electric_slots, handicapped_slots, compact_slots]):
            raise ValidationError("Slot counts cannot be negative")
        
        total_slots = regular_slots + electric_slots + handicapped_slots + compact_slots
        if total_slots == 0:
            raise ValidationError("At least one slot is required per level")
        
        slots = []
        slot_number = 1
        
        # Create slots in a specific order for better layout
        # 1. Handicapped slots first (closest to entrance)
        for _ in range(handicapped_slots):
            slots.append(ParkingSlot(
                slot_number=slot_number,
                slot_type=SlotType.HANDICAPPED,
                is_occupied=False,
                vehicle=None
            ))
            slot_number += 1
        
        # 2. Electric slots (grouped together for charging infrastructure)
        for _ in range(electric_slots):
            slots.append(ParkingSlot(
                slot_number=slot_number,
                slot_type=SlotType.ELECTRIC,
                is_occupied=False,
                vehicle=None
            ))
            slot_number += 1
        
        # 3. Compact slots
        for _ in range(compact_slots):
            slots.append(ParkingSlot(
                slot_number=slot_number,
                slot_type=SlotType.COMPACT,
                is_occupied=False,
                vehicle=None
            ))
            slot_number += 1
        
        # 4. Regular slots (fill the rest)
        for _ in range(regular_slots):
            slots.append(ParkingSlot(
                slot_number=slot_number,
                slot_type=SlotType.REGULAR,
                is_occupied=False,
                vehicle=None
            ))
            slot_number += 1
        
        return slots
    
    @staticmethod
    def optimize_slot_distribution(total_slots: int, electric_ratio: float = 0.3) -> Dict[str, int]:
        """Calculate optimal slot distribution for a level"""
        if total_slots <= 0:
            raise ValidationError("Total slots must be positive")
        
        if not 0 <= electric_ratio <= 1:
            raise ValidationError("Electric ratio must be between 0 and 1")
        
        # Calculate slot distribution based on typical usage patterns
        electric_slots = max(1, int(total_slots * electric_ratio))
        handicapped_slots = max(1, int(total_slots * 0.05))  # 5% for handicapped
        compact_slots = max(0, int(total_slots * 0.1))  # 10% for compact vehicles
        
        # Ensure we don't exceed total slots
        reserved_slots = electric_slots + handicapped_slots + compact_slots
        if reserved_slots > total_slots:
            # Adjust proportionally
            scale_factor = (total_slots - 1) / reserved_slots  # Leave at least 1 regular slot
            electric_slots = max(1, int(electric_slots * scale_factor))
            handicapped_slots = max(1, int(handicapped_slots * scale_factor))
            compact_slots = max(0, int(compact_slots * scale_factor))
        
        regular_slots = total_slots - electric_slots - handicapped_slots - compact_slots
        regular_slots = max(0, regular_slots)
        
        return {
            'regular_slots': regular_slots,
            'electric_slots': electric_slots,
            'handicapped_slots': handicapped_slots,
            'compact_slots': compact_slots
        }


@dataclass
class ParkingOperation:
    """Represents a parking operation result"""
    success: bool
    slot_number: Optional[int] = None
    message: str = ""
    vehicle: Optional[Vehicle] = None


class ParkingBusinessService:
    """Core business service that orchestrates parking operations"""
    
    def __init__(self, parking_strategy: ParkingStrategy = None):
        """Initialize with a parking strategy"""
        self.parking_strategy = parking_strategy or PreferredSlotTypeStrategy()
        self.capacity_service = ParkingCapacityService()
        self.search_service = VehicleSearchService()
        self.validation_service = ParkingValidationService()
        self.layout_service = ParkingLotLayoutService()
    
    def park_vehicle(self, slots: List[ParkingSlot], vehicle: Vehicle) -> ParkingOperation:
        """Park a vehicle using business rules"""
        try:
            # Validate parking operation
            available_slots = [slot for slot in slots if not slot.is_occupied]
            self.validation_service.validate_vehicle_parking(vehicle, available_slots)
            
            # Find suitable slot using strategy
            suitable_slot = self.parking_strategy.find_suitable_slot(slots, vehicle)
            
            if not suitable_slot:
                return ParkingOperation(
                    success=False,
                    message="No suitable parking slot available"
                )
            
            # Park the vehicle (this would be handled by the infrastructure layer)
            return ParkingOperation(
                success=True,
                slot_number=suitable_slot.slot_number,
                message=f"Vehicle parked successfully in slot {suitable_slot.slot_number}",
                vehicle=vehicle
            )
            
        except (ValidationError, OperationError) as e:
            return ParkingOperation(
                success=False,
                message=str(e)
            )
    
    def remove_vehicle(self, slot: ParkingSlot) -> ParkingOperation:
        """Remove a vehicle using business rules"""
        try:
            # Validate removal operation
            self.validation_service.validate_vehicle_removal(slot)
            
            vehicle = slot.vehicle
            return ParkingOperation(
                success=True,
                slot_number=slot.slot_number,
                message=f"Vehicle {vehicle.license_plate} removed successfully",
                vehicle=vehicle
            )
            
        except (ValidationError, OperationError) as e:
            return ParkingOperation(
                success=False,
                message=str(e)
            )
    
    def find_vehicles(
        self, 
        lot_name: str,
        levels: Dict[int, List[ParkingSlot]], 
        criteria: SearchCriteria
    ) -> List[SearchResult]:
        """Find vehicles using search service"""
        return self.search_service.find_vehicles_by_criteria(lot_name, levels, criteria)
    
    def get_capacity_metrics(self, slots: List[ParkingSlot]) -> Dict[str, int]:
        """Get capacity metrics for slots"""
        return self.capacity_service.calculate_capacity_metrics(slots)
    
    def create_parking_level(
        self,
        level: int,
        total_slots: int, 
        electric_ratio: float = 0.3,
        include_handicapped: bool = True,
        include_compact: bool = True
    ) -> List[ParkingSlot]:
        """Create a parking level with optimal slot distribution"""
        # Get optimal distribution
        distribution = self.layout_service.optimize_slot_distribution(total_slots, electric_ratio)
        
        # Adjust based on options
        if not include_handicapped:
            distribution['regular_slots'] += distribution['handicapped_slots']
            distribution['handicapped_slots'] = 0
        
        if not include_compact:
            distribution['regular_slots'] += distribution['compact_slots']
            distribution['compact_slots'] = 0
        
        # Create the level layout
        return self.layout_service.create_level_layout(
            level=level,
            regular_slots=distribution['regular_slots'],
            electric_slots=distribution['electric_slots'],
            handicapped_slots=distribution['handicapped_slots'],
            compact_slots=distribution['compact_slots']
        )

from dataclasses import dataclass
from typing import List, Optional
from src.Vehicle import Vehicle
from src.ElectricVehicle import ElectricVehicle

@dataclass
class VehicleInfo:
    slot: int
    floor: int
    reg_no: str
    color: str
    make: str
    model: str

@dataclass
class EVChargeInfo:
    slot: int
    floor: int
    reg_no: str
    charge: str

@dataclass
class ParkingStatus:
    regular_vehicles: List[VehicleInfo]
    ev_vehicles: List[VehicleInfo]

@dataclass
class ChargeStatus:
    vehicles: List[EVChargeInfo]

@dataclass
class SearchResult:
    result_type: str  # 'slot' or 'registration'
    items: List[str]
    is_ev: bool
    error: Optional[str] = None

@dataclass
class ParkingResult:
    success: bool
    slot_number: Optional[int] = None
    message: str = ""

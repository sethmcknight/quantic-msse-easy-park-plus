import tkinter as tk
from typing import List, Optional, Union
from src.Vehicle import Vehicle, Car, Motorcycle
from src.ElectricVehicle import ElectricVehicle, ElectricCar, ElectricBike
from src.parking_data import ParkingStatus, ChargeStatus, SearchResult, VehicleInfo, EVChargeInfo

# Type aliases for clarity
VehicleType = Union[Vehicle, ElectricVehicle]
VehicleList = List[Optional[Vehicle]]
EVList = List[Optional[ElectricVehicle]]

# Global UI elements
root = tk.Tk()
root.geometry("650x850")
root.resizable(False, False)
root.title("Parking Lot Manager")

# Input values
command_value = tk.StringVar()
num_value = tk.StringVar()
ev_value = tk.StringVar()
make_value = tk.StringVar()
model_value = tk.StringVar()
color_value = tk.StringVar()
reg_value = tk.StringVar()
level_value = tk.StringVar()
ev_car_value = tk.IntVar()
ev_car2_value = tk.IntVar()
slot1_value = tk.StringVar()
slot2_value = tk.StringVar()
reg1_value = tk.StringVar()
slot_value = tk.StringVar()
ev_motor_value = tk.IntVar()
level_remove_value = tk.StringVar()
    
tfield = tk.Text(root, width=70, height=15)

class ParkingLot:
    def __init__(self):
        self.capacity: int = 0
        self.evCapacity: int = 0
        self.level: int = 0
        self.slotid: int = 0
        self.slotEvId: int = 0
        self.numOfOccupiedSlots: int = 0
        self.numOfOccupiedEvSlots: int = 0
        self.slots: VehicleList = []
        self.evSlots: EVList = []
    
    def createParkingLot(self, capacity: int, evcapacity: int, level: int) -> int:
        self.slots = [None] * capacity
        self.evSlots = [None] * evcapacity
        self.level = level
        self.capacity = capacity
        self.evCapacity = evcapacity
        return self.level

    def getEmptySlot(self) -> Optional[int]:
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                return i
        return None

    def getEmptyEvSlot(self) -> Optional[int]:
        for i in range(len(self.evSlots)):
            if self.evSlots[i] is None:
                return i
        return None

    def getEmptyLevel(self):
        # TODO: Remove unused method. See anti-patterns.md.
        if (self.numOfOccupiedEvSlots == 0 and self.numOfOccupiedSlots == 0):
            return self.level

    def _create_ev_vehicle(self, registrationNumber: str, make: str, model: str, color: str, motor: bool) -> ElectricVehicle:
        """Create an electric vehicle instance"""
        if motor:
            return ElectricBike(registrationNumber, make, model, color)
        else:
            return ElectricCar(registrationNumber, make, model, color)

    def _create_regular_vehicle(self, registrationNumber: str, make: str, model: str, color: str, motor: bool) -> Vehicle:
        """Create a regular vehicle instance"""
        if motor:
            return Motorcycle(registrationNumber, make, model, color)
        else:
            return Car(registrationNumber, make, model, color)

    def park(self, registrationNumber: str, make: str, model: str, color: str, ev: int, motor: int) -> int:
        """Park a vehicle and return its slot number"""
        ev_bool = bool(ev)
        motor_bool = bool(motor)

        if ev_bool:
            if self.numOfOccupiedEvSlots >= self.evCapacity:
                return -1
            slot_index = self.getEmptyEvSlot()
            if slot_index is None:
                return -1
            vehicle = self._create_ev_vehicle(registrationNumber, make, model, color, motor_bool)
            self.evSlots[slot_index] = vehicle
            self.numOfOccupiedEvSlots += 1
            return slot_index + 1
        else:
            if self.numOfOccupiedSlots >= self.capacity:
                return -1  # Regular lot is full
            slot_index = self.getEmptySlot()
            if slot_index is None:
                return -1  # No available regular slot
            vehicle = self._create_regular_vehicle(registrationNumber, make, model, color, motor_bool)
            self.slots[slot_index] = vehicle
            self.numOfOccupiedSlots += 1
            return slot_index + 1  # Return 1-based slot ID

    def leave(self, slotid: int, ev: int):
        if (ev == 1):
            if self.numOfOccupiedEvSlots > 0 and self.evSlots[slotid-1] is not None:
                self.evSlots[slotid-1] = None
                self.numOfOccupiedEvSlots = self.numOfOccupiedEvSlots - 1
                return True
            else:
                return False
        else:
            if self.numOfOccupiedSlots > 0 and self.slots[slotid-1] is not None:
                self.slots[slotid-1] = None
                self.numOfOccupiedSlots = self.numOfOccupiedSlots - 1
                return True
            else:
                return False

    def edit(self, slotid: int, registrationNumber: str, make: str, model: str, color: str, ev: int, motor: int) -> bool:
        if ev == 1:
            motor_bool = bool(motor)
            self.evSlots[slotid-1] = self._create_ev_vehicle(registrationNumber, make, model, color, motor_bool)
            return True
        else:
            motor_bool = bool(motor)
            self.slots[slotid-1] = Motorcycle(registrationNumber, make, model, color) if motor_bool else Car(registrationNumber, make, model, color)
            return True
        return False        

    def status(self) -> ParkingStatus:
        """Get the current status of the parking lot"""
        regular_vehicles: List[VehicleInfo] = []
        ev_vehicles: List[VehicleInfo] = []

        for i, vehicle in enumerate(self.slots):
            if vehicle:
                regular_vehicles.append(VehicleInfo(
                    slot=i+1,
                    floor=self.level,
                    reg_no=vehicle.registrationNumber,
                    color=vehicle.color,
                    make=vehicle.make,
                    model=vehicle.model
                ))

        for i, vehicle in enumerate(self.evSlots):
            if vehicle:
                ev_vehicles.append(VehicleInfo(
                    slot=i+1,
                    floor=self.level,
                    reg_no=vehicle.registrationNumber,
                    color=vehicle.color,
                    make=vehicle.make,
                    model=vehicle.model
                ))

        return ParkingStatus(regular_vehicles=regular_vehicles, ev_vehicles=ev_vehicles)

    def chargeStatus(self) -> ChargeStatus:
        """Get the charging status of electric vehicles"""
        charging_vehicles: List[EVChargeInfo] = []

        for i, vehicle in enumerate(self.evSlots):
            if vehicle:
                charging_vehicles.append(EVChargeInfo(
                    slot=i+1,
                    floor=self.level,
                    reg_no=vehicle.registrationNumber,
                    charge=str(vehicle.charge)
                ))

        return ChargeStatus(vehicles=charging_vehicles)

# Search functions

    def getRegNumFromColor(self, color: str) -> list[str]:
        return [str(i.registrationNumber) for i in self.slots if i is not None and i.color == color]
    
    def getSlotNumFromRegNum(self, registrationNumber: str) -> int:
        for idx, slot in enumerate(self.slots):
            if slot is not None and str(slot.registrationNumber) == str(registrationNumber):
                return idx + 1
        return -1
            
    def getSlotNumFromColor(self, color: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.slots) if i is not None and i.color == color]

    def getSlotNumFromMake(self, make: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.slots) if i is not None and i.make == make]

    def getSlotNumFromModel(self, model: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.slots) if i is not None and i.model == model]

    def getRegNumFromColorEv(self, color: str) -> list[str]:
        return [str(i.registrationNumber) for i in self.evSlots if i is not None and i.color == color]
            
    def getSlotNumFromRegNumEv(self, registrationNumber: str) -> int:
        for idx, slot in enumerate(self.evSlots):
            if slot is not None and str(slot.registrationNumber) == str(registrationNumber):
                return idx + 1
        return -1

    def getSlotNumFromColorEv(self, color: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.evSlots) if i is not None and i.color == color]

    def getSlotNumFromMakeEv(self, make: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.evSlots) if i is not None and i.make == make]

    def getSlotNumFromModelEv(self, model: str) -> list[str]: 
        return [str(index + 1) for index, i in enumerate(self.evSlots) if i is not None and i.model == model]

    def slotNumByReg(self, reg_no: str) -> SearchResult:
        """Returns slot numbers for vehicles with the given registration number."""
        slotnum = self.getSlotNumFromRegNum(reg_no)
        slotnum2 = self.getSlotNumFromRegNumEv(reg_no)
        
        if slotnum >= 0:
            return SearchResult(
                result_type='slot',
                items=[str(slotnum)],
                is_ev=False
            )
        elif slotnum2 >= 0:
            return SearchResult(
                result_type='slot',
                items=[str(slotnum2)],
                is_ev=True
            )
        else:
            return SearchResult(
                result_type='slot',
                items=[],
                is_ev=False,
                error="Not found"
            )

    def slotNumByColor(self, color: str) -> SearchResult:
        """Returns slot numbers for vehicles with the given color."""
        regular_slots = self.getSlotNumFromColor(color)
        ev_slots = self.getSlotNumFromColorEv(color)
        
        return SearchResult(
            result_type='slot',
            items=regular_slots + ev_slots,
            is_ev=False  # Combined results, so we don't distinguish
        )

    def regNumByColor(self, color: str) -> SearchResult:
        """Returns registration numbers for vehicles with the given color."""
        regular_regs = self.getRegNumFromColor(color)
        ev_regs = self.getRegNumFromColorEv(color)
        
        return SearchResult(
            result_type='registration',
            items=regular_regs + ev_regs,
            is_ev=False  # Combined results, so we don't distinguish
        )
        
# Slot Management Functions

    def makeLot(self) -> None:
        # Input validation and exception handling added.
        try:
            num = int(num_value.get())
            ev = int(ev_value.get())
            level = int(level_value.get())
            if num < 0 or ev < 0 or level < 1:
                tfield.insert(tk.INSERT, "Invalid input: All values must be positive integers.\n")
                return
        except ValueError:
            tfield.insert(tk.INSERT, "Invalid input: Please enter valid numbers for all fields.\n")
            return
        try:
            self.createParkingLot(num, ev, level)
            output = f'Created a parking lot with {num} regular slots and {ev} ev slots on level: {level}\n'
            tfield.insert(tk.INSERT, output)
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error creating parking lot: {e}\n")

    def parkCar(self) -> None:  
        # Input validation and exception handling added.
        try:
            reg = reg_value.get().strip()
            make = make_value.get().strip()
            model = model_value.get().strip()
            color = color_value.get().strip()
            ev = ev_car_value.get()
            motor = ev_motor_value.get()
            if not reg or not make or not model or not color:
                tfield.insert(tk.INSERT, "Invalid input: All fields must be filled.\n")
                return
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error reading input: {e}\n")
            return
        try:
            res = self.park(reg, make, model, color, ev, motor)
            if res == -1:
                tfield.insert(tk.INSERT, "Sorry, parking lot is full\n")
            else:
                output = 'Allocated slot number: '+str(res)+ "\n"
                tfield.insert(tk.INSERT, output)
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error parking car: {e}\n")

    def removeCar(self) -> None:
        # Input validation and exception handling added.
        try:
            slot_str = slot_value.get()
            ev_str = ev_car2_value.get()
            slot_num = int(slot_str)
            ev_flag = int(ev_str)
            if slot_num < 1:
                tfield.insert(tk.INSERT, "Invalid input: Slot number must be a positive integer.\n")
                return
            # Out-of-range check for slot number
            if ev_flag == 1:
                if slot_num > len(self.evSlots):
                    tfield.insert(tk.INSERT, f"Invalid input: Slot number {slot_num} is out of range for EV slots.\n")
                    return
            else:
                if slot_num > len(self.slots):
                    tfield.insert(tk.INSERT, f"Invalid input: Slot number {slot_num} is out of range for regular slots.\n")
                    return
        except ValueError:
            tfield.insert(tk.INSERT, "Invalid input: Please enter a valid slot number.\n")
            return
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error reading input: {e}\n")
            return
        try:
            status = self.leave(slot_num, ev_flag)
            if status:
                output = f'Slot number {slot_num} is free\n'
                tfield.insert(tk.INSERT, output)
            else:
                tfield.insert(tk.INSERT, f"Unable to remove a car from slot: {slot_num}\n")
        except Exception as e:
            tfield.insert(tk.INSERT, f"Error removing car: {e}\n")


# Main App
# TODO: Refactor to separate UI and business logic. See anti-patterns.md.             
def main():
    class ParkingLotUI:
        # ParkingLotUI acts as the interface between the UI and the business logic.
        # All UI actions (such as search, status, and charge status display) call methods on ParkingLotUI,
        # which then call the appropriate business logic methods on the ParkingLot instance.
        # This ensures that the UI does not directly access or depend on the internal implementation of ParkingLot.
        # Example: show_slot_by_reg, show_slots_by_color, and show_reg_by_color call slotNumByReg, slotNumByColor, and regNumByColor.
        def __init__(self, parking_lot: ParkingLot):
            self.parking_lot = parking_lot

        def _clear_text_field(self) -> None:
            """Clear the text field for fresh output"""
            tfield.delete("1.0", tk.END)

        def display_search_result(self, result: SearchResult) -> None:
            """Display search results in the text field"""
            self._clear_text_field()
            
            if result.error:
                tfield.insert(tk.END, f"Error: {result.error}\n")
                return

            if result.result_type == 'slot':
                if result.is_ev:
                    prefix = "EV "
                else:
                    prefix = ""
                if len(result.items) == 1:
                    tfield.insert(tk.END, f"{prefix}Slot Number: {result.items[0]}\n")
                else:
                    slots = ", ".join(result.items)
                    tfield.insert(tk.END, f"{prefix}Slot Numbers: {slots}\n")
            else:  # registration numbers
                reg_numbers = ", ".join(result.items)
                tfield.insert(tk.END, f"Registration Numbers: {reg_numbers}\n")

        def show_slot_by_reg(self, reg_no: str) -> None:
            """Display the slot number for a given registration number"""
            # Updated to use business logic method slotNumByReg instead of non-existent search_slot_by_reg
            result = self.parking_lot.slotNumByReg(reg_no)
            self.display_search_result(result)

        def show_slots_by_color(self, color: str) -> None:
            """Display slot numbers for vehicles of given color"""
            # Updated to use business logic method slotNumByColor instead of non-existent search_slots_by_color
            result = self.parking_lot.slotNumByColor(color)
            self.display_search_result(result)

        def show_reg_by_color(self, color: str) -> None:
            """Display registration numbers of vehicles with given color"""
            # Already uses correct business logic method regNumByColor
            result = self.parking_lot.regNumByColor(color)
            self.display_search_result(result)

        def show_status(self) -> None:
            """Display current parking lot status"""
            status = self.parking_lot.status()
            self._clear_text_field()
            
            if not status.regular_vehicles and not status.ev_vehicles:
                tfield.insert(tk.END, "Parking lot is empty\n")
                return

            if status.regular_vehicles:
                tfield.insert(tk.END, "Regular Vehicles:\n")
                tfield.insert(tk.END, "Slot\tFloor\tReg No.\t\tColor\t\tMake\t\tModel\n")
                for vehicle in status.regular_vehicles:
                    tfield.insert(tk.END, f"{vehicle.slot}\t{vehicle.floor}\t{vehicle.reg_no}\t{vehicle.color}\t"
                                f"{vehicle.make}\t{vehicle.model}\n")
            
            if status.ev_vehicles:
                tfield.insert(tk.END, "\nElectric Vehicles:\n")
                tfield.insert(tk.END, "Slot\tFloor\tReg No.\t\tColor\t\tMake\t\tModel\n")
                for vehicle in status.ev_vehicles:
                    tfield.insert(tk.END, f"{vehicle.slot}\t{vehicle.floor}\t{vehicle.reg_no}\t{vehicle.color}\t"
                                f"{vehicle.make}\t{vehicle.model}\n")

        def show_charge_status(self) -> None:
            """Display charging status of electric vehicles"""
            charge_status = self.parking_lot.chargeStatus()
            self._clear_text_field()

            if not charge_status.vehicles:
                tfield.insert(tk.END, "No electric vehicles are currently charging\n")
                return

            tfield.insert(tk.END, "Electric Vehicle Charging Status:\n")
            tfield.insert(tk.END, "Slot\tFloor\tReg No.\t\tCharge %\n")
            for vehicle in charge_status.vehicles:
                tfield.insert(tk.END, f"{vehicle.slot}\t{vehicle.floor}\t{vehicle.reg_no}\t"
                            f"{vehicle.charge}%\n")

    parkinglot = ParkingLot()
    parking_ui = ParkingLotUI(parkinglot)
    
    #input boxes and GUI
    label_head= tk.Label(root, text = 'Parking Lot Manager', font = 'Arial 14 bold')
    label_head.grid(row=0, column=0, padx = 10, columnspan = 4)

    label_head= tk.Label(root, text = 'Lot Creation', font = 'Arial 12 bold')
    label_head.grid(row=1, column=0, padx = 10, columnspan = 4)

    lbl_num = tk.Label(root, text = 'Number of Regular Spaces', font = 'Arial 12')
    lbl_num.grid(row=2, column=0, padx = 5)

    num_entry = tk.Entry(root, textvariable = num_value,  width = 6, font='Arial 12')
    num_entry.grid(row = 2, column=1,  padx = 4, pady = 2)

    lbl_ev = tk.Label(root, text = 'Number of EV Spaces', font = 'Arial 12')
    lbl_ev.grid(row=2, column=2, padx = 5)

    num_entry = tk.Entry(root, textvariable = ev_value,  width = 6, font='Arial 12')
    num_entry.grid(row = 2, column=3,  padx = 4, pady = 4)

    lbl_level = tk.Label(root, text = 'Floor Level', font = 'Arial 12')
    lbl_level.grid(row=3, column=0, padx = 5)
    
    level_entry = tk.Entry(root, textvariable = level_value,  width = 6, font='Arial 12')
    level_entry.grid(row = 3, column=1,  padx = 4, pady = 4)
    level_entry.insert(tk.INSERT, "1")

    parkMakeBtn = tk.Button(root, command = parkinglot.makeLot, text = "Create Parking Lot", font="Arial 12", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    parkMakeBtn.grid(row=4, column=0,  padx = 4, pady = 4)

    label_car= tk.Label(root, text = 'Car Management', font = 'Arial 12 bold')
    label_car.grid(row=5, column=0, padx = 10, columnspan = 4)

    lbl_make = tk.Label(root, text = 'Make', font = 'Arial 12')
    lbl_make.grid(row=6, column=0, padx = 5)

    make_entry = tk.Entry(root, textvariable = make_value,  width = 12, font='Arial 12')
    make_entry.grid(row=6, column=1,  padx = 4, pady = 4)

    lbl_model = tk.Label(root, text = 'Model', font = 'Arial 12')
    lbl_model.grid(row=6, column=2, padx = 5)

    model_entry = tk.Entry(root, textvariable = model_value,  width = 12, font='Arial 12')
    model_entry.grid(row=6, column=3,  padx = 4, pady = 4)
    
    lbl_color = tk.Label(root, text = 'Color', font = 'Arial 12')
    lbl_color.grid(row=7, column=0, padx = 5)

    color_entry = tk.Entry(root, textvariable = color_value,  width = 12, font='Arial 12')
    color_entry.grid(row=7, column=1,  padx = 4, pady = 4)

    lbl_reg = tk.Label(root, text = 'Registration #', font = 'Arial 12')
    lbl_reg.grid(row=7, column=2, padx = 5)
    
    reg_entry = tk.Entry(root, textvariable = reg_value,  width = 12, font='Arial 12')
    reg_entry.grid(row=7, column=3,  padx = 4, pady = 4)

    evToggle = tk.Checkbutton(root, text='Electric',variable=ev_car_value, onvalue=1, offvalue=0, font='Arial 12')
    evToggle.grid(column=0, row=8,  padx = 4, pady = 4)

    motorToggle = tk.Checkbutton(root, text='Motorcycle',variable=ev_motor_value, onvalue=1, offvalue=0, font='Arial 12')
    motorToggle.grid(column=1, row=8,  padx = 4, pady = 4)

    parkBtn = tk.Button(root, command = parkinglot.parkCar, text = "Park Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    parkBtn.grid(column=0, row=9,  padx = 4, pady = 4)

    lbl_slot = tk.Label(root, text = 'Slot #', font = 'Arial 12')
    lbl_slot.grid(row=10, column=0, padx = 5)

    slot_entry = tk.Entry(root, textvariable = slot_value,  width = 12, font='Arial 12')
    slot_entry.grid(row=10, column=1,  padx = 4, pady = 4)

    evToggle = tk.Checkbutton(root, text='Remove EV?',variable=ev_car2_value, onvalue=1, offvalue=0, font='Arial 12')
    evToggle.grid(column=2, row=10,  padx = 4, pady = 4)

    removeBtn = tk.Button(root, command = parkinglot.removeCar, text = "Remove Car", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    removeBtn.grid(column=0, row=11,  padx = 4, pady = 4)

    spacer1 = tk.Label(root, text="")
    spacer1.grid(row=12, column=0)

    slotRegBtn = tk.Button(root, command=lambda: parking_ui.show_slot_by_reg(slot1_value.get()), text = "Get Slot ID by Registration #", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotRegBtn.grid(column=0, row=13,  padx = 4, pady = 4)

    slot1_entry = tk.Entry(root, textvariable = slot1_value,  width = 12, font='Arial 12')
    slot1_entry.grid(row=13, column=1,  padx = 4, pady = 4)

    slotColorBtn = tk.Button(root, command=lambda: parking_ui.show_slots_by_color(slot2_value.get()), text = "Get Slot ID by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotColorBtn.grid(column=2, row=13,  padx = 4, pady = 4)

    slot2_entry = tk.Entry(root, textvariable = slot2_value,  width = 12, font='Arial 12')
    slot2_entry.grid(row=13, column=3,  padx = 4, pady = 4)
    
    regColorBtn = tk.Button(root, command=lambda: parking_ui.show_reg_by_color(reg1_value.get()), text = "Get Registration # by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    regColorBtn.grid(column=0, row=14,  padx = 4, pady = 4)

    reg1_entry = tk.Entry(root, textvariable = reg1_value,  width = 12, font='Arial 12')
    reg1_entry.grid(row=14, column=1,  padx = 4, pady = 4)

    chargeStatusBtn = tk.Button(root, command=parking_ui.show_charge_status, text="EV Charge Status", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    chargeStatusBtn.grid(column=2, row=14,  padx = 4, pady = 4)
    
    statusBtn = tk.Button(root, command=parking_ui.show_status, text="Current Lot Status", font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5 )
    statusBtn.grid(column=0, row=15,  padx = 4, pady = 4)

    tfield.grid(column=0, row=16, padx = 10, pady = 10, columnspan = 4)
    
    root.mainloop()


if __name__ == '__main__':
    main()

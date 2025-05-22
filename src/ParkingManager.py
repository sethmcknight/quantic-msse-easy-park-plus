import src.Vehicle as Vehicle
import src.ElectricVehicle as ElectricVehicle
import tkinter as tk
from typing import Optional

root = tk.Tk()
root.geometry("650x850")
root.resizable(False, False)
root.title("Parking Lot Manager")

#input values
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
    
#Parking Lot class
class ParkingLot:
    def __init__(self):
        self.capacity: int = 0
        self.evCapacity: int = 0
        self.level: int = 0
        self.slotid: int = 0
        self.slotEvId: int = 0
        self.numOfOccupiedSlots: int = 0
        self.numOfOccupiedEvSlots: int = 0
        self.slots: list[Optional[Vehicle.Vehicle]] = []
        self.evSlots: list[Optional[ElectricVehicle.ElectricVehicle]] = []

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

    def _create_ev_vehicle(self, registrationNumber: str, make: str, model: str, color: str, motor: bool):
        """Helper to create an EV vehicle (car or bike)"""
        if motor:
            return ElectricVehicle.ElectricBike(registrationNumber, make, model, color)
        else:
            return ElectricVehicle.ElectricCar(registrationNumber, make, model, color)

    def _create_regular_vehicle(self, registrationNumber: str, make: str, model: str, color: str, motor: bool):
        """Helper to create a regular vehicle (car or motorcycle)"""
        if motor:
            return Vehicle.Motorcycle(registrationNumber, make, model, color)
        else:
            return Vehicle.Car(registrationNumber, make, model, color)

    def park(self, registrationNumber: str, make: str, model: str, color: str, ev: int, motor: int) -> int:
        """Parks a vehicle and returns the 1-based slot number, or -1 if full."""
        ev_bool = bool(ev)
        motor_bool = bool(motor)

        if ev_bool:
            if self.numOfOccupiedEvSlots >= self.evCapacity:
                return -1  # EV lot is full
            slot_index = self.getEmptyEvSlot()
            if slot_index is None:
                return -1  # No available EV slot
            vehicle_to_park = self._create_ev_vehicle(registrationNumber, make, model, color, motor_bool)
            self.evSlots[slot_index] = vehicle_to_park
            self.numOfOccupiedEvSlots += 1
            return slot_index + 1  # Return 1-based slot ID
        else:
            if self.numOfOccupiedSlots >= self.capacity:
                return -1  # Regular lot is full
            slot_index = self.getEmptySlot()
            if slot_index is None:
                return -1  # No available regular slot
            vehicle_to_park = self._create_regular_vehicle(registrationNumber, make, model, color, motor_bool)
            self.slots[slot_index] = vehicle_to_park
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
            self.slots[slotid-1] = Vehicle.Car(str(registrationNumber), str(make), str(model), str(color))
            return True
        return False     

    def status(self):
        # TODO: Decouple UI logic from business logic. Return data instead of directly updating tfield. See anti-patterns.md.
        output = "Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.slots)):
            slot = self.slots[i]
            if slot is not None:
                output = f"{i+1}\t{self.level}\t{slot.registrationNumber}\t\t{slot.color}\t\t{slot.make}\t\t{slot.model}\n"
                tfield.insert(tk.INSERT, output)
        output = "\nElectric Vehicles\nSlot\tFloor\tReg No.\t\tColor \t\tMake \t\tModel\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.evSlots)):
            slot = self.evSlots[i]
            if slot is not None:
                output = f"{i+1}\t{self.level}\t{slot.registrationNumber}\t\t{slot.color}\t\t{slot.make}\t\t{slot.model}\n"
                tfield.insert(tk.INSERT, output)

    def chargeStatus(self):
        # TODO: Decouple UI logic from business logic. Return data instead of directly updating tfield. See anti-patterns.md.
        output = "Electric Vehicle Charge Levels\nSlot\tFloor\tReg No.\t\tCharge %\n"
        tfield.insert(tk.INSERT, output)
        for i in range(len(self.evSlots)):
            slot = self.evSlots[i]
            if slot is not None:
                charge = getattr(slot, 'charge', 'N/A')
                output = f"{i+1}\t{self.level}\t{slot.registrationNumber}\t\t{charge}\n"
                tfield.insert(tk.INSERT, output)

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

    def slotNumByReg(self):
        # TODO: Decouple UI logic from business logic. See anti-patterns.md.
        slot_val = slot1_value.get()
        slotnum = self.getSlotNumFromRegNum(slot_val)
        slotnum2 = self.getSlotNumFromRegNumEv(slot_val)
        output = ""
        if slotnum >= 0:
            output = "Identified slot: " + str(slotnum) + "\n"
        elif slotnum2 >= 0:
            output = "Identified slot (EV): " + str(slotnum2) + "\n"
        else:
            output = "Not found\n"

        tfield.insert(tk.INSERT, output)

    def slotNumByColor(self):
        # TODO: Decouple UI logic from business logic. See anti-patterns.md.
        slotnums = self.getSlotNumFromColor(slot2_value.get())
        slotnums2 = self.getSlotNumFromColorEv(slot2_value.get())
        output = "Identified slots: " + ', '.join(slotnums) + "\n"
        tfield.insert(tk.INSERT, output)
        output = "Identified slots (EV): " + ', '.join(slotnums2) + "\n"
        tfield.insert(tk.INSERT, output)

    def regNumByColor(self):
        # TODO: Decouple UI logic from business logic. See anti-patterns.md.
        regnums = self.getRegNumFromColor(reg1_value.get())
        regnums2 = self.getRegNumFromColorEv(reg1_value.get())
        output = "Registation Numbers: "+', '.join(regnums) + "\n"        
        tfield.insert(tk.INSERT, output)
        output = "Registation Numbers (EV): "+', '.join(regnums2) + "\n"        
        tfield.insert(tk.INSERT, output)

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

    parkinglot = ParkingLot()
    
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

    slotRegBtn = tk.Button(root, command = parkinglot.slotNumByReg, text = "Get Slot ID by Registration #", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotRegBtn.grid(column=0, row=13,  padx = 4, pady = 4)

    slot1_entry = tk.Entry(root, textvariable = slot1_value,  width = 12, font='Arial 12')
    slot1_entry.grid(row=13, column=1,  padx = 4, pady = 4)

    slotColorBtn = tk.Button(root, command = parkinglot.slotNumByColor, text = "Get Slot ID by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    slotColorBtn.grid(column=2, row=13,  padx = 4, pady = 4)

    slot2_entry = tk.Entry(root, textvariable = slot2_value,  width = 12, font='Arial 12')
    slot2_entry.grid(row=13, column=3,  padx = 4, pady = 4)
    
    regColorBtn = tk.Button(root, command = parkinglot.regNumByColor, text = "Get Registration # by Color", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    regColorBtn.grid(column=0, row=14,  padx = 4, pady = 4)

    reg1_entry = tk.Entry(root, textvariable = reg1_value,  width = 12, font='Arial 12')
    reg1_entry.grid(row=14, column=1,  padx = 4, pady = 4)

    chargeStatusBtn = tk.Button(root, command = parkinglot.chargeStatus, text = "EV Charge Status", font="Arial 11", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 )
    chargeStatusBtn.grid(column=2, row=14,  padx = 4, pady = 4)

    statusBtn = tk.Button(root, command = parkinglot.status, text = "Current Lot Status", font="Arial 11", bg='PaleGreen1', fg='black', activebackground="PaleGreen3", padx=5, pady=5 )
    statusBtn.grid(column=0, row=15,  padx = 4, pady = 4)

    tfield.grid(column=0, row=16, padx = 10, pady = 10, columnspan = 4)
    
    root.mainloop()


if __name__ == '__main__':
    main()

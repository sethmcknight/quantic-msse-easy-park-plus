# Variable Names
## ParkingManager.py
- 'root' for the main Tkinter window?
    - this is a common convention but could be more descriptive
- short variable names
    - ev_value
    - num_value
    - make_value
    - model_value
    - color_value
    - reg_value
    - level_value
    - ev_car_value
    - ev_car2_value
    - slot1_value
    - slot2_value
    - reg1_value
    - slot_value
    - ev_motor_value
    - level_remove_value
    - tfield (text field for a confirmation message)
- local variables
    - consider being explicit in for loops instead of i for the iterator
    - ParkingLot init method
        - slotid
        - slotEvId
    - park Method
        - ev
        - motor
    - createParkingLot method
        - capacity
        - evcapacity
        - level
    - vehicle in multiple methods
        - used in different ways
        - clarify how it is being used

## Vehicle.py
- regnum
- make
- model
- color

## ElectricVehicle.py
- charge
- regnum
- make
- model
- color

# Comments
- basically non-existent
- a few headers that provide almost not additional value

# Passing Mutable Arguments

## ParkingManager.py
- createParkingLot method in ParkingLot Class
    - line 42
    - Analysis: The method initializes self.slots and self.evSlots as lists. While these lists are mutable, they are not passed as arguments to the method. Instead, they are created within the method, so there is no risk of unintended side effects from external modifications.
- park method in ParkingLot Class
    - line 64
    - Analysis: The self.slots and self.evSlots lists are modified within this method. While these are mutable, they are instance attributes, not passed as arguments. There is no direct passing of mutable arguments here.

## Summary
- In the current codebase, there are no instances where mutable arguments (e.g., lists, dictionaries) are passed directly to methods or functions. Most mutable objects are instance attributes (self.slots, self.evSlots) that are modified internally within methods.
- This is a good practice, as it avoids unintended side effects from external modifications to mutable objects.

# Different Types in Functions

## ParkingManager.py
- ParkingLot Class
    - getEmptySlot method
        - Returns: An integer (index i) if an empty slot is found.
        - Potential Issue: If no empty slot is found (i.e., the loop completes without a return), the function will implicitly return None.
        - Type Variation: Can return int or NoneType.
    - getEmptyEVSlot method
        - Returns: An integer (index i) if an empty slot is found.
        - Potential Issue: If no empty slot is found (i.e., the loop completes without a return), the function will implicitly return None.
        - Type Variation: Can return int or NoneType.
    - getEmptyLevel
        - Returns: self.level (an integer) if the level is empty.
        - Potential Issue: If the condition (self.numOfOccupiedEvSlots == 0 and self.numOfOccupiedSlots == 0) is false, the function implicitly returns None.
        - Type Variation: Can return int or NoneType.
    - park(self, regnum, make, model, color, ev, motor)
        - This method, as it's partially written in the provided context, doesn't have explicit return statements for all paths, but its primary purpose is to modify state. If it were to return a status, care would be needed. Currently, it implicitly returns None.
    - getSlotNumFromRegNum
        - If found: Returns i+1 (an integer, 1-based slot number).
        - If not found: Returns -1 (integer).
        - Consistency: Returns an integer. -1 is a magic number for "not found."
    - getSlotNumFromRegNumEV
        - If found: Returns i+1 (an integer, 1-based slot number).
        - If not found: Returns -1 (integer).
        - Consistency: Returns an integer. -1 is a magic number for "not found."

- If a search method (e.g., getSlotNumFromRegNum) doesn't find the item, it might return a special value like -1 (integer) or None (NoneType), or perhaps a string message. This could lead to type variation if not handled consistently. For example, returning None vs. an empty string "" vs. a message string "Not found".
- Implicit None Returns (Type Variation):
    - getEmptySlot(), getEmptyEvSlot(), getEmptyLevel() can return an int or None.
    - Recommendation: Decide on a consistent strategy.
        - Option A (Return -1): If you prefer integers, have them return -1 (or another suitable integer sentinel value) if not found/condition not met. This makes them consistent with park and getSlotNumFromRegNum.
        - Option B (Raise Exception): For "not found" scenarios, raising a custom exception (e.g., SlotNotFoundException) can be a cleaner way to handle exceptional cases.
        - Option C (Return None explicitly and document): If None is the preferred "not found" indicator, make the return None explicit and ensure all callers check for it.
- Magic Number -1:
    - park(), getSlotNumFromRegNum(), getSlotNumFromRegNumEv() use -1.
    - Recommendation: This is acceptable if used consistently and documented. Callers like parkCar() and slotNumByReg() already check for -1. However, using None or exceptions can sometimes be more Pythonic for "not found" or error states, as it avoids overloading a valid integer value (though -1 is unlikely to be a valid slot ID here).

## Vehicle.py and ElectricVehicle.py
- all good

## Summary
- Implicit None Returns: Methods like getEmptySlot, getEmptyEvSlot, and getEmptyLevel in ParkingLot can return an integer or None. Callers of these methods must be prepared to handle None to avoid TypeError if they expect an integer.
- Search/Query Methods (Hypothetical): If methods that search for vehicles or slots return different types based on whether an item is found (e.g., an object vs. None, or a number vs. a string message), this can make the calling code more complex and error-prone. It's generally better to return a consistent type (e.g., always an object or None, always a list which might be empty, always an int where a special value like -1 indicates "not found").

# Clumsy / Unnecessary Loop statements
## ParkingManager.py
- status & chargeStatus
    - consider using `enumerate`
    - use f-strings for formatting
- search methods (getRegNumFromColor, getSlotNumFromColor, etc)
    - Observation: The if self.slots[i] == -1: continue pattern is a bit clumsy. It can be inverted or, even better, these loops are prime candidates for list comprehensions.
- getSlotNumfromRegNum, getSlotNumFromRegNumEv
    - Observation: The else: continue is completely redundant. If the inner if is false, the loop naturally continues.
## Summary
- - Redundant else: continue: Remove these as they add no value (e.g., in getSlotNumFromRegNum).
- if ... == -1: continue pattern: Refactor these. List comprehensions are often the best solution for filtering and transforming, making the code more readable and concise (e.g., in getRegNumFromColor, getSlotNumFromColor).
- range(len(...)) for iteration: Consider using enumerate when both index and item are needed, especially for readability (e.g., in status, chargeStatus).
- String concatenation: Use f-strings for building strings as they are generally more readable and efficient than manual concatenation with + (e.g., in status, chargeStatus).

# Superfluous/Lengthy/Nested if statements
- ParkingLot.park method
    - 4 levels deep of nested if's
    - length combined conditions (slot + ev + motor)
    - superfluous == 1 vs bool (ie `if ev` vs `if ev == 1`)
    - recommendations
        - use guard clauses to return early if specific slots aren't available
        - use booleans
        - create helper methods for ev/regular to reduce nesting in the main park method
- ParkingLot.getSlotFromRegNum(Ev)
    - superfluous else: continue
- ParkingLot.getRegNumFromColor, etc.
    - use list comprehension instead

# Global Variables
- Tkinter variables
    - comon use for a single-file Tkinter app
    - but larger apps prefer encapsulation in classses
        - Create an App class (or a similar name like ParkingManagerApp):
            - The __init__ method of this class will set up the main Tkinter window (root).
            - The Tkinter control variables (command_value, num_value, etc.) will become instance attributes of this App class (e.g., self.command_value).
            - The tfield Text widget will also become an instance attribute (e.g., self.tfield).
            - An instance of your ParkingLot class will be an attribute of this App class (e.g., self.parking_lot).
        - Move GUI setup into methods of the App class:
            - The code that creates labels, entry fields, buttons, and the text field will be moved into methods within the App class (e.g., _create_widgets, _layout_widgets).
        - Adapt event handlers:
            - The functions currently acting as event handlers (like makeLot, parkCar, removeCar, etc.) will become methods of the App class.
            - When assigning commands to buttons, you'll use self.method_name.
            - These methods will access the control variables and the parking_lot instance via self.

# Try/Except Blocks wtihout Exception Handling
- no try/except blocks in use
- There are several places, particularly in the GUI handler functions in ParkingManager.py (like makeLot, removeCar, editCar) and within the ParkingLot.edit method, where operations prone to exceptions (specifically ValueError from int() conversions of user input) are performed without being enclosed in try...except blocks at all.
- the main concern is the absence of error handling for potential ValueError exceptions in parts of the original code structure, rather than the presence of try...except blocks that then fail to act on the caught exception.

# Broad Import Statements
- no major concerns

# Deprecated, unused code blocks
- Unused Global Variables in ParkingManager.py:
    - command_value = tk.StringVar():
        - This StringVar is defined at the global level.
        - Looking through the GUI setup in ParkingManager.py, there doesn't appear to be any tk.Entry or other widget that is explicitly configured with textvariable=command_value.
        - No function seems to get() or set() its value.
        - Conclusion: command_value appears to be an unused global variable. Potential dead code.
    - level_remove_value = tk.StringVar():
        - Similar to command_value, this StringVar is defined globally.
        - There's no widget in the provided GUI setup that uses it, nor any function that interacts with it.
        - Conclusion: level_remove_value appears to be an unused global variable. Potential dead code.
- Unused Methods:
    - ParkingLot.getEmptyLevel(self) in ParkingManager.py:
        - This method checks if the parking lot is completely empty and returns the level number.
        - this method does not appear to be called by any of the GUI handler functions or other methods within the ParkingLot class.
        - Conclusion: getEmptyLevel() seems to be an unused method. Potential dead code.
    - getType() methods in Vehicle.py and ElectricVehicle.py:
        - Vehicle.py defines getType() for Car, Truck, Motorcycle, and Bus.
        - ElectricVehicle.py defines getType() for ElectricCar and ElectricBike.
        - These methods return a string representing the specific type of the vehicle.
        - the specific type is determined at instantiation (e.g., Vehicle.Car(...), ElectricVehicle.ElectricBike(...)). The status() method accesses attributes like regnum, color, make, model directly.
        - There are no apparent calls to vehicle_instance.getType() anywhere in ParkingManager.py.
        - Conclusion: The getType() methods in all vehicle subclasses (Car, Truck, Motorcycle, Bus, ElectricCar, ElectricBike) appear to be unused. Potential dead code.  
    - ElectricVehicle.setCharge(self, charge) in ElectricVehicle.py:
        - the charge is initialized to 0 in ElectricVehicle.__init__().
        - The ParkingLot.chargeStatus() method calls ev_vehicle.getCharge().
        - no calls to ev_vehicle.setCharge() in ParkingManager.py or elsewhere in the provided snippets. This means that once an electric vehicle is created, its charge level (which starts at 0) is never updated.
        - Conclusion: ElectricVehicle.setCharge() appears to be an unused method. Potential dead code. (This also implies the charge feature is incomplete, as charges never change from 0).
- Potentially Redundant Instance Variables in ParkingLot (ParkingManager.py):
    - self.slotid and self.slotEvId initialized in ParkingLot.__init__:
        - In the ParkingLot.park() method, the actual slotid assigned to a vehicle comes from self.getEmptySlot() or self.getEmptyEvSlot(). If the lines self.slotid = self.slotid + 1 and self.slotEvId = self.slotEvId + 1 (which were commented out in some earlier suggestions but might be present in your code) are indeed present and uncommented, these variables would act as simple counters for the number of vehicles parked, or perhaps an attempt to generate unique IDs. However, if these variables are only incremented and their values are never read or used for any decision-making, ID assignment, or output, then the increment operations and potentially the variables themselves (if not used for any other purpose) could be considered dead or redundant in their current role. The actual slot index is determined by finding an empty slot. This is more nuanced: if they are intended to be a separate ID system or a count, they might not be "dead" but their purpose and interaction with the slot finding logic is unclear and potentially redundant. If they are not used for anything after being incremented, then the incrementing part is dead.
- Summary
    - Global variables in ParkingManager.py: command_value, level_remove_value.
    - Method in ParkingLot: getEmptyLevel().
    - Methods in Vehicle.py and ElectricVehicle.py: All getType() methods, ElectricVehicle.setCharge().

# Unnecessary abstractions
- 

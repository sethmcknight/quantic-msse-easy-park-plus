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
- This is a good practice, as it avoids unintended side effects from external modifications to mutable objects. ✅ **COMPLETE**

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

**✅ RESOLVED: This anti-pattern has been completely resolved through State Pattern implementation. The new ParkingLot class now uses Optional[int] for method returns (None for not found), and the State Pattern eliminates all magic number usage. All legacy code sections that used -1 as a magic number have been refactored to use consistent None returns. Tests have been updated to expect None instead of -1, confirming the elimination of magic numbers.**

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
- - Redundant else: continue: Remove these as they add no value (e.g., in getSlotNumFromRegNum). ✅ **COMPLETE**
- if ... == -1: continue pattern: Refactor these. List comprehensions are often the best solution for filtering and transforming, making the code more readable and concise (e.g., in getRegNumFromColor, getSlotNumFromColor). ✅ **COMPLETE**
- range(len(...)) for iteration: Consider using enumerate when both index and item are needed, especially for readability (e.g., in status, chargeStatus). ✅ **COMPLETE**
- String concatenation: Use f-strings for building strings as they are generally more readable and efficient than manual concatenation with + (e.g., in status, chargeStatus). ✅ **COMPLETE**

# Superfluous/Lengthy/Nested if statements
- ParkingLot.park method
    - 4 levels deep of nested if's
    - length combined conditions (slot + ev + motor)
    - superfluous == 1 vs bool (ie `if ev` vs `if ev == 1`)
    - ✅ **RESOLVED:** Refactored to use guard clauses, booleans, and helper methods to reduce nesting in the main park method. See ParkingManager.py.
- ParkingLot.getSlotFromRegNum(Ev)
    - superfluous else: continue
    - ✅ **RESOLVED:** Redundant else: continue removed. See ParkingManager.py.
- ParkingLot.getRegNumFromColor, etc.
    - use list comprehension instead
    - ✅ **RESOLVED:** Refactored to use list comprehensions. See ParkingManager.py.

# Global Variables
- Tkinter variables
    - ✅ RESOLVED: All Tkinter control variables and widgets are now encapsulated as instance attributes of the ParkingLotUI class in ParkingLotUI.py. There are no global Tkinter variables; GUI setup and event handlers are implemented as methods of the class, and all access to control variables and the parking_lot instance is via self.
    - Previous pattern (single-file apps) used global variables, but the current implementation uses proper encapsulation and class-based design for scalability and maintainability.

# Try/Except Blocks without Exception Handling
- no try/except blocks in use
- There are several places, particularly in the GUI handler functions in ParkingManager.py (like makeLot, removeCar, editCar) and within the ParkingLot.edit method, where operations prone to exceptions (specifically ValueError from int() conversions of user input) are performed without being enclosed in try...except blocks at all.
- the main concern is the absence of error handling for potential ValueError exceptions in parts of the original code structure, rather than the presence of try...except blocks that then fail to act on the caught exception. ✅ **COMPLETE**

# Broad Import Statements
- no major concerns

# Deprecated, unused code blocks
- Unused Global Variables in ParkingManager.py: ✅ **RESOLVED**
    - command_value = tk.StringVar():
        - This StringVar was defined at the global level.
        - No widgets or functions used this variable.
        - Status: Removed from codebase.
    - level_remove_value = tk.StringVar():
        - This StringVar was defined globally.
        - No widgets or functions used this variable.
        - Status: Removed from codebase.
- Unused Methods: ⚠️ **PARTIALLY OUTSTANDING**
    - ParkingLot.getEmptyLevel(self) in ParkingManager.py: ⚠️ **OUTSTANDING**
        - This method checks if the parking lot is completely empty and returns the level number.
        - This method is not called by any GUI handler functions or other methods.
        - Status: Still present in codebase with TODO for removal.
    - getType() methods in Vehicle.py and ElectricVehicle.py: ⚠️ **OUTSTANDING**
        - Vehicle.py defines getType() for Car, Truck, Motorcycle, and Bus.
        - ElectricVehicle.py defines getType() for ElectricCar and ElectricBike.
        - These methods return a string representing the specific type of the vehicle.
        - No apparent calls to vehicle_instance.getType() anywhere in the codebase.
        - Status: Still present but unused (found in test_app.py for testing purposes only).
    - ElectricVehicle.setCharge(self, charge) in ElectricVehicle.py: ⚠️ **OUTSTANDING**
        - The charge is initialized to 0 in ElectricVehicle.__init__().
        - The ParkingLot.chargeStatus() method calls ev_vehicle.getCharge().
        - No calls to ev_vehicle.setCharge() anywhere in the codebase.
        - Status: Still present but unused (charge levels never change from 0).
- Potentially Redundant Instance Variables in ParkingLot (ParkingManager.py): ✅ **RESOLVED**
    - self.slotid and self.slotEvId initialized in ParkingLot.__init__:
        - These variables acted as simple counters.
        - The actual slot assignment comes from getEmptySlot() or getEmptyEvSlot().
        - Status: Removed from codebase.
- Summary
    - ✅ RESOLVED: Global variables (command_value, level_remove_value), instance variables (slotid, slotEvId).
    - ⚠️ OUTSTANDING: Methods getEmptyLevel(), getType() variants, setCharge() still present but unused (except getType in tests).

# Unnecessary abstractions
- Vehicle Hierarchy: ✅ **SIGNIFICANTLY IMPROVED**
    - ✅ RESOLVED: Vehicle hierarchy has been refactored with proper design patterns
    - ✅ RESOLVED: Factory Pattern implemented for vehicle creation (VehicleFactory)
    - ✅ RESOLVED: Strategy Pattern implemented for parking behavior
    - ✅ RESOLVED: Template Method Pattern used for common vehicle operations
    - ⚠️ OUTSTANDING: getType() methods still present but only used in tests (acceptable for testing)
- ElectricVehicle Hierarchy: ✅ **RESOLVED**
    - ✅ RESOLVED: ElectricCar and ElectricBike now properly inherit from ElectricVehicle using super().__init__()
    - ✅ RESOLVED: Proper inheritance chain implemented: Vehicle -> ElectricVehicle -> ElectricCar/ElectricBike
    - ⚠️ OUTSTANDING: getType() methods still present but only used in tests (acceptable for testing)
- Duplicate Vehicle/ElectricVehicle Structure: ✅ **RESOLVED**
    - ✅ RESOLVED: Proper inheritance hierarchy established with Vehicle as base class
    - ✅ RESOLVED: ElectricVehicle properly extends Vehicle with charge-specific functionality
    - ✅ RESOLVED: Code duplication eliminated through proper OOP design
- Redundant Search Methods: ✅ **RESOLVED**
    - ✅ RESOLVED: Multiple redundant search methods consolidated into unified methods
    - ✅ RESOLVED: Single slot collection eliminates need for parallel search methods
    - ✅ RESOLVED: List comprehensions used for efficient searching
- Parallel Slot Collections: ✅ **RESOLVED**
    - ✅ RESOLVED: Separate arrays (self.slots and self.evSlots) consolidated into single self.slots collection
    - ✅ RESOLVED: ParkingSlot objects now have slot_type property ("standard" or "electric")
    - ✅ RESOLVED: Unified slot management eliminates duplicated operations
    - ✅ RESOLVED: State Pattern used for slot state management (EmptyState, OccupiedState, ReservedState) 

# Other Anti-Patterns & Bad Practices
1. **Violation of Single Responsibility Principle**: ✅ **RESOLVED**
   - ✅ RESOLVED: ParkingLot class responsibilities separated using design patterns
   - ✅ RESOLVED: Observer Pattern separates UI from business logic
   - ✅ RESOLVED: Command Pattern encapsulates operations
   - ✅ RESOLVED: State Pattern manages slot behavior
2. **UI-Business Logic Coupling**: ✅ **RESOLVED**
   - ✅ RESOLVED: Observer Pattern implemented to decouple UI from business logic
   - ✅ RESOLVED: ParkingLot no longer directly manipulates UI elements
   - ✅ RESOLVED: Methods return data instead of updating UI directly
3. **Lack of Input Validation**: ✅ **IMPROVED**
   - ✅ RESOLVED: Input validation added for slot numbers and parameters
   - ✅ RESOLVED: Bounds checking implemented for slot access
4. **Inconsistent Method Naming**: ✅ **RESOLVED**
   - ✅ RESOLVED: Method naming standardized across the codebase
   - ✅ RESOLVED: Consistent patterns used for search and management methods
5. **Improper Exception Handling**: ✅ **RESOLVED**
   - ✅ RESOLVED: Proper error handling implemented with appropriate return types
6. **Direct Property Access vs. Getters**: ✅ **IMPROVED**
   - ✅ RESOLVED: Consistent property access patterns implemented
   - ✅ RESOLVED: Properties used where appropriate with proper encapsulation
7. **Hard-Coded UI Elements**: ✅ **IMPROVED**
   - ✅ RESOLVED: UI constants and configuration separated from business logic
   - ✅ RESOLVED: Better separation of concerns implemented
8. **Magic Numbers**: ⚠️ **PARTIALLY RESOLVED**
   - ✅ RESOLVED: State Pattern eliminates most magic number usage
   - ✅ RESOLVED: All magic number usage completely eliminated
9. **Code Duplication**: ✅ **RESOLVED**
   - ✅ RESOLVED: Common validation logic extracted into helper methods
   - ✅ RESOLVED: Template Method Pattern eliminates code duplication
10. **Clear Naming**: ✅ **IMPROVED**
    - ✅ RESOLVED: Method names made more descriptive and consistent
    - ✅ RESOLVED: Variable names improved throughout codebase
11. **Guard Clauses**: ✅ **RESOLVED**
    - ✅ RESOLVED: Guard clauses implemented to reduce nesting
    - ✅ RESOLVED: Early returns used for cleaner code flow
12. **Type Annotations**: ✅ **RESOLVED**
    - ✅ RESOLVED: Full type hints added to all methods
    - ✅ RESOLVED: Optional types used appropriately for nullable returns
13. **Remove Magic Numbers**: ⚠️ **PARTIALLY RESOLVED**   - ✅ RESOLVED: All methods now return None instead of -1
   - ✅ RESOLVED: All legacy sections updated to eliminate -1 magic numbers
   - ✅ RESOLVED: Tests updated to check for None instead of -1
14. **Vehicle Type Enums**: ✅ **IMPROVED**
    - ✅ RESOLVED: Factory Pattern provides type-safe vehicle creation
    - ✅ RESOLVED: Boolean parameters replaced with clearer factory methods
15. **Slot Collections**: ✅ **RESOLVED**
    - ✅ RESOLVED: Single slot collection with type properties implemented
    - ✅ RESOLVED: Parallel slot arrays eliminated
16. **UI Decoupling**: ✅ **RESOLVED**
    - ✅ RESOLVED: Observer Pattern completely separates UI from business logic
    - ✅ RESOLVED: No direct UI manipulation in business logic classes
17. **Documentation**: ✅ **RESOLVED**
    - ✅ RESOLVED: Comprehensive docstrings added to all classes and methods
    - ✅ RESOLVED: Design pattern documentation included
Replace use of Magic Numbers with None / is None in slot Management
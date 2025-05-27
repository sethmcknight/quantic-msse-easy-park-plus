import unittest
from Vehicle import VehicleFactory
from ParkingManager import ParkingLot

class TestVehicle(unittest.TestCase):
    def test_vehicle_attributes(self):
        v = VehicleFactory.create_car("ABC123", "Toyota", "Camry", "Red")
        self.assertEqual(v.make, "Toyota")
        self.assertEqual(v.model, "Camry")
        self.assertEqual(v.color, "Red")
        self.assertEqual(v.registration_number, "ABC123")

    def test_car_type(self):
        c = VehicleFactory.create_car("DEF456", "Honda", "Civic", "Blue")
        self.assertEqual(c.get_type(), "Car")

    def test_truck_type(self):
        t = VehicleFactory.create_truck("GHI789", "Ford", "F-150", "Black")
        self.assertEqual(t.get_type(), "Truck")

    def test_motorcycle_type(self):
        m = VehicleFactory.create_motorcycle("JKL012", "Yamaha", "YZF", "Yellow")
        self.assertEqual(m.get_type(), "Motorcycle")

    def test_bus_type(self):
        b = VehicleFactory.create_bus("MNO345", "Mercedes", "Sprinter", "White")
        self.assertEqual(b.get_type(), "Bus")

class TestElectricVehicle(unittest.TestCase):
    def test_electric_car_attributes(self):
        ev = VehicleFactory.create_electric_car("EV123", "Tesla", "Model 3", "White")
        self.assertEqual(ev.make, "Tesla")
        self.assertEqual(ev.model, "Model 3")
        self.assertEqual(ev.color, "White")
        self.assertEqual(ev.registration_number, "EV123")
        self.assertEqual(ev.charge, 0)
        ev.set_charge(80)
        self.assertEqual(ev.charge, 80)

    def test_electric_car_type(self):
        ec = VehicleFactory.create_electric_car("EV456", "Nissan", "Leaf", "Green")
        self.assertEqual(ec.get_type(), "Electric Car")

    def test_electric_motorcycle_type(self):
        em = VehicleFactory.create_electric_motorcycle("EV789", "Zero", "SR/F", "Black")
        self.assertEqual(em.get_type(), "Electric Motorcycle")

class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.lot = ParkingLot()
        self.lot.create_parking_lot(3, 1, 1)  # 3 regular slots + 1 EV slot = 4 total slots

    def test_park_regular_and_ev(self):
        # Park regular car
        slot = self.lot.park("REG1", "Toyota", "Corolla", "Red", False, False)
        self.assertEqual(slot, 1)
        # Park EV car - should go to next available slot
        slot_ev = self.lot.park("EV1", "Tesla", "Model S", "Blue", True, False)
        self.assertEqual(slot_ev, 2)
        # Park regular motorcycle
        slot2 = self.lot.park("REG2", "Honda", "CBR", "Black", False, True)
        self.assertEqual(slot2, 3)
        # Park another electric car - should go to the electric slot (slot 4)
        slot3 = self.lot.park("EV2", "Nissan", "Leaf", "Green", True, False)
        self.assertEqual(slot3, 4)
        # Try to park regular car when all regular slots are full - should return None instead of -1
        slot4 = self.lot.park("REG3", "Ford", "Focus", "White", False, False)
        self.assertIsNone(slot4)

    def test_leave(self):
        slot = self.lot.park("REG1", "Toyota", "Corolla", "Red", False, False)
        self.assertIsNotNone(slot)  # Ensure parking succeeded
        if slot is not None:  # Type guard for safety
            left = self.lot.leave(slot)
            self.assertTrue(left)
            left_again = self.lot.leave(slot)
            self.assertFalse(left_again)

    def test_search_by_color(self):
        self.lot.park("REG1", "Toyota", "Corolla", "Red", False, False)
        self.lot.park("EV1", "Tesla", "Model S", "Red", True, False)
        result = self.lot.get_slots_by_color("Red")
        self.assertIn(1, result)
        self.assertIn(2, result)

    def test_search_by_registration(self):
        self.lot.park("REG1", "Toyota", "Corolla", "Red", False, False)
        result = self.lot.get_slot_by_registration("REG1")
        self.assertEqual(result, 1)

    def test_status_and_charge_status(self):
        # Park a regular car and an electric car
        reg_slot = self.lot.park("REG1", "Toyota", "Corolla", "Red", False, False)
        ev_slot = self.lot.park("EV1", "Tesla", "Model S", "Blue", True, False)
        
        # Test that both vehicles are parked
        self.assertEqual(reg_slot, 1)
        self.assertEqual(ev_slot, 2)
        
        # Test status functionality by checking vehicles are in slots
        reg_vehicle = self.lot.get_vehicle(1)
        ev_vehicle = self.lot.get_vehicle(2)
        
        self.assertIsNotNone(reg_vehicle)
        self.assertIsNotNone(ev_vehicle)
        
        if reg_vehicle is not None:
            self.assertEqual(reg_vehicle.registration_number, "REG1")
        if ev_vehicle is not None:
            self.assertEqual(ev_vehicle.registration_number, "EV1")

if __name__ == "__main__":
    unittest.main()

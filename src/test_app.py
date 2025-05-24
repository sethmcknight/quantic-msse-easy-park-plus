import unittest
from src.Vehicle import Vehicle, Car, Truck, Motorcycle, Bus
from src.ElectricVehicle import ElectricVehicle, ElectricCar, ElectricBike
from src.ParkingManager import ParkingLot

class TestVehicle(unittest.TestCase):
    def test_vehicle_attributes(self):
        v = Vehicle("ABC123", "Toyota", "Camry", "Red")
        self.assertEqual(v.getMake(), "Toyota")
        self.assertEqual(v.getModel(), "Camry")
        self.assertEqual(v.getColor(), "Red")
        self.assertEqual(v.getRegistrationNumber(), "ABC123")

    def test_car_type(self):
        c = Car("DEF456", "Honda", "Civic", "Blue")
        self.assertEqual(c.getType(), "Car")

    def test_truck_type(self):
        t = Truck("GHI789", "Ford", "F-150", "Black")
        self.assertEqual(t.getType(), "Truck")

    def test_motorcycle_type(self):
        m = Motorcycle("JKL012", "Yamaha", "YZF", "Yellow")
        self.assertEqual(m.getType(), "Motorcycle")

    def test_bus_type(self):
        b = Bus("MNO345", "Mercedes", "Sprinter", "White")
        self.assertEqual(b.getType(), "Bus")

class TestElectricVehicle(unittest.TestCase):
    def test_electric_vehicle_attributes(self):
        ev = ElectricVehicle("EV123", "Tesla", "Model 3", "White")
        self.assertEqual(ev.getMake(), "Tesla")
        self.assertEqual(ev.getModel(), "Model 3")
        self.assertEqual(ev.getColor(), "White")
        self.assertEqual(ev.getRegistrationNumber(), "EV123")
        self.assertEqual(ev.getCharge(), 0)
        ev.setCharge(80)
        self.assertEqual(ev.getCharge(), 80)

    def test_electric_car_type(self):
        ec = ElectricCar("EV456", "Nissan", "Leaf", "Green")
        self.assertEqual(ec.getType(), "Car")

    def test_electric_bike_type(self):
        eb = ElectricBike("EV789", "Zero", "SR/F", "Black")
        self.assertEqual(eb.getType(), "Motorcycle")

class TestParkingLot(unittest.TestCase):
    def setUp(self):
        self.lot = ParkingLot()
        self.lot.createParkingLot(2, 1, 1)

    def test_park_regular_and_ev(self):
        # Park regular car
        slot = self.lot.park("REG1", "Toyota", "Corolla", "Red", 0, 0)
        self.assertEqual(slot, 1)
        # Park EV car
        slot_ev = self.lot.park("EV1", "Tesla", "Model S", "Blue", 1, 0)
        self.assertEqual(slot_ev, 1)
        # Park regular motorcycle
        slot2 = self.lot.park("REG2", "Honda", "CBR", "Black", 0, 1)
        self.assertEqual(slot2, 2)
        # Try to park when full
        slot3 = self.lot.park("REG3", "Ford", "Focus", "White", 0, 0)
        self.assertEqual(slot3, -1)

    def test_leave(self):
        slot = self.lot.park("REG1", "Toyota", "Corolla", "Red", 0, 0)
        left = self.lot.leave(slot, 0)
        self.assertTrue(left)
        left_again = self.lot.leave(slot, 0)
        self.assertFalse(left_again)

    def test_search_by_color(self):
        self.lot.park("REG1", "Toyota", "Corolla", "Red", 0, 0)
        self.lot.park("EV1", "Tesla", "Model S", "Red", 1, 0)
        result = self.lot.slotNumByColor("Red")
        self.assertIn("1", result.items)
        self.assertEqual(result.result_type, "slot")

    def test_search_by_registration(self):
        self.lot.park("REG1", "Toyota", "Corolla", "Red", 0, 0)
        result = self.lot.slotNumByReg("REG1")
        self.assertEqual(result.items, ["1"])
        self.assertEqual(result.result_type, "slot")

    def test_status_and_charge_status(self):
        self.lot.park("REG1", "Toyota", "Corolla", "Red", 0, 0)
        self.lot.park("EV1", "Tesla", "Model S", "Blue", 1, 0)
        status = self.lot.status()
        self.assertEqual(len(status.regular_vehicles), 1)
        self.assertEqual(len(status.ev_vehicles), 1)
        charge_status = self.lot.chargeStatus()
        self.assertEqual(len(charge_status.vehicles), 1)

if __name__ == "__main__":
    unittest.main()

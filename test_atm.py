import unittest

from atm import ATM, find_min_notes


class TestDispense(unittest.TestCase):

    def test_example_from_task(self):
        atm = ATM({500: 8, 200: 10, 100: 20})
        result = atm.dispense(2700)
        self.assertEqual(result, {500: 5, 200: 1})
        self.assertEqual(sum(result.values()), 6)
        self.assertEqual(atm.inventory, {500: 3, 200: 9, 100: 20})

    def test_greedy_would_fail(self):
        atm = ATM({4: 1, 3: 2})
        self.assertEqual(atm.dispense(6), {3: 2})
        self.assertEqual(atm.inventory, {4: 1, 3: 0})

    def test_minimum_notes_not_just_any_answer(self):
        # 6 can be 3+3 or 2+2+2, 3+3 uses fewer notes
        result = find_min_notes({3: 5, 2: 5}, 6)
        self.assertEqual(result, {3: 2})

    def test_limited_inventory_forces_more_notes(self):
        # only one 500, so the rest has to come from 100s
        atm = ATM({500: 1, 100: 10})
        self.assertEqual(atm.dispense(900), {500: 1, 100: 4})

    def test_exact_inventory_used_up(self):
        atm = ATM({500: 2, 100: 1})
        self.assertEqual(atm.dispense(1100), {500: 2, 100: 1})
        self.assertEqual(atm.inventory, {500: 0, 100: 0})

    def test_cannot_dispense_returns_none(self):
        atm = ATM({500: 8, 200: 10, 100: 20})
        self.assertIsNone(atm.dispense(50))

    def test_amount_more_than_cash_in_atm(self):
        atm = ATM({500: 1, 100: 2})
        self.assertIsNone(atm.dispense(1000))

    def test_failed_withdrawal_leaves_inventory_unchanged(self):
        inv = {4: 1, 3: 1}
        atm = ATM(inv)
        self.assertIsNone(atm.dispense(6))
        self.assertEqual(atm.inventory, {4: 1, 3: 1})

    def test_two_withdrawals_in_a_row(self):
        atm = ATM({500: 2, 200: 2})
        self.assertEqual(atm.dispense(700), {500: 1, 200: 1})
        self.assertEqual(atm.dispense(700), {500: 1, 200: 1})
        self.assertIsNone(atm.dispense(200))

    def test_other_denominations(self):
        atm = ATM({50: 4, 20: 4, 10: 4})
        self.assertEqual(atm.dispense(130), {50: 2, 20: 1, 10: 1})

    def test_single_denomination(self):
        atm = ATM({100: 3})
        self.assertEqual(atm.dispense(300), {100: 3})
        self.assertIsNone(atm.dispense(100))

    def test_zero_count_denomination_is_ignored(self):
        atm = ATM({500: 0, 100: 5})
        self.assertEqual(atm.dispense(300), {100: 3})

    def test_all_notes_zero(self):
        atm = ATM({500: 0, 100: 0})
        self.assertIsNone(atm.dispense(100))

    def test_caller_dict_not_modified(self):
        inv = {500: 2, 100: 2}
        atm = ATM(inv)
        atm.dispense(600)
        self.assertEqual(inv, {500: 2, 100: 2})

    def test_inventory_property_is_a_copy(self):
        atm = ATM({500: 2})
        atm.inventory[500] = 99
        self.assertEqual(atm.inventory, {500: 2})


class TestAmountValidation(unittest.TestCase):

    def setUp(self):
        self.atm = ATM({500: 8, 200: 10, 100: 20})

    def test_zero(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(0)

    def test_negative(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(-500)

    def test_non_numeric_string(self):
        with self.assertRaises(ValueError):
            self.atm.dispense("abc")

    def test_none(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(None)

    def test_decimal(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(250.5)

    def test_bool(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(True)

    def test_inventory_untouched_after_bad_input(self):
        try:
            self.atm.dispense(-1)
        except ValueError:
            pass
        self.assertEqual(self.atm.inventory, {500: 8, 200: 10, 100: 20})


class TestInventoryValidation(unittest.TestCase):

    def test_empty_inventory(self):
        with self.assertRaises(ValueError):
            ATM({})

    def test_not_a_dict(self):
        with self.assertRaises(ValueError):
            ATM([500, 200])

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            ATM({500: -1})

    def test_non_integer_quantity(self):
        with self.assertRaises(ValueError):
            ATM({500: 2.5})

    def test_zero_denomination(self):
        with self.assertRaises(ValueError):
            ATM({0: 5})

    def test_negative_denomination(self):
        with self.assertRaises(ValueError):
            ATM({-100: 5})

    def test_non_numeric_denomination(self):
        with self.assertRaises(ValueError):
            ATM({"abc": 5})

    def test_decimal_denomination(self):
        with self.assertRaises(ValueError):
            ATM({10.5: 5})


if __name__ == "__main__":
    unittest.main()

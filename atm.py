"""ATM cash dispenser - gives the exact amount using the fewest notes."""

FAIL_MESSAGE = "Cannot dispense requested amount"


def is_whole_number(x):
    # True/False count as ints in Python, so rule them out
    return isinstance(x, int) and not isinstance(x, bool)


def validate_inventory(inventory):
    if not isinstance(inventory, dict) or len(inventory) == 0:
        raise ValueError("Inventory must be a non-empty dict like {500: 8, 200: 10}")
    for denom, count in inventory.items():
        if not is_whole_number(denom) or denom <= 0:
            raise ValueError(f"Invalid denomination: {denom!r}")
        if not is_whole_number(count) or count < 0:
            raise ValueError(f"Invalid note quantity for {denom}: {count!r}")


def validate_amount(amount):
    if not is_whole_number(amount):
        raise ValueError(f"Amount must be a whole number, got {amount!r}")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")


def find_min_notes(inventory, amount):
    """Return {denom: count} with the fewest notes, or None if not possible.

    Greedy can fail (e.g. {4: 1, 3: 2} for 6), so we build up the answer
    one denomination at a time.

    best[a] = the combination with the fewest notes that makes amount a,
    using only the denominations we have looked at so far.
    """
    best = {0: {}}  # amount 0 needs no notes

    for denom, count in inventory.items():
        new_best = dict(best)  # using 0 notes of this denomination
        for a, combo in best.items():
            for k in range(1, count + 1):  # try k notes of this denomination
                total = a + k * denom
                if total > amount:
                    break
                candidate = {**combo, denom: k}
                if total not in new_best or sum(candidate.values()) < sum(new_best[total].values()):
                    new_best[total] = candidate
        best = new_best

    return best.get(amount)  # None if the amount was never reached


class ATM:
    def __init__(self, inventory):
        validate_inventory(inventory)
        self._inventory = dict(inventory)

    @property
    def inventory(self):
        return dict(self._inventory)

    def dispense(self, amount):
        """Return {denom: count}, or None if it can't be dispensed.

        Invalid input raises ValueError. The inventory changes only if the
        full amount was found.
        """
        validate_amount(amount)

        notes = find_min_notes(self._inventory, amount)
        if notes is None:
            return None

        for denom, count in notes.items():
            self._inventory[denom] -= count
        return notes


def main():
    atm = ATM({500: 8, 200: 10, 100: 20})
    print("Inventory:", atm.inventory)

    while True:
        raw = input("Amount to withdraw (q to quit): ").strip()
        if raw.lower() == "q":
            break
        try:
            amount = int(raw)
        except ValueError:
            print(f"Error: Amount must be a whole number, got {raw!r}")
            continue

        try:
            notes = atm.dispense(amount)
        except ValueError as err:
            print("Error:", err)
            continue

        if notes is None:
            print(FAIL_MESSAGE)
        else:
            print(notes, "- total notes:", sum(notes.values()))
            print("Updated inventory:", atm.inventory)


if __name__ == "__main__":
    main()

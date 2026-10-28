# ATM Cash Dispenser

Python program that dispenses an exact amount using the fewest notes, from a
limited ATM inventory. Standard library only.

## Run

```
python atm.py
```

Use it from code:

```python
from atm import ATM

atm = ATM({500: 8, 200: 10, 100: 20})
print(atm.dispense(2700))   # {500: 5, 200: 1}
print(atm.inventory)        # {500: 3, 200: 9, 100: 20}
print(atm.dispense(50))     # None  -> "Cannot dispense requested amount"
```

## Run the tests

```
python -m unittest -v
```

## Behaviour

- Can be dispensed: returns `{denomination: count}` and reduces the inventory.
- Cannot be dispensed: returns `None`, inventory unchanged.
- Invalid input (zero, negative, non-numeric amount; negative quantity; bad
  denomination; empty inventory): raises `ValueError` with a clear message.

## Approach

Taking the largest note first (greedy) can fail. Example: `{4: 1, 3: 2}` for 6
- greedy takes 4, is stuck with 2, but 3 + 3 works.

So the program uses dynamic programming, like the coin change problem with a
limit on each note:

1. Keep `best[a]` = the fewest-notes combination that makes amount `a`.
   Start with `best[0] = {}` (zero notes for zero money).
2. Go through the denominations one at a time. For every amount already
   reachable, try adding 1, 2, ... up to the available number of that note.
3. If that gives a new amount, or a combination with fewer notes than the one
   stored, save it.
4. At the end, `best[amount]` is the answer, or the amount was not reachable.

The inventory is only reduced after the full answer is found, so a failed
withdrawal never changes it.

Code layout: validation functions, `find_min_notes` (just calculates, changes
nothing), and the `ATM` class (holds the inventory and applies the result).

## Complexity

`A` = amount, `D` = number of denominations, `C` = most notes of any one denomination.

- Time: O(D * A * C)
- Space: O(A * D)

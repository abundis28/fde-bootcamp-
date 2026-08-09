# Cart — Specification (the source of truth)

The code in `discount_cart.py` must behave exactly as described here. Where the
code and this spec disagree, the **spec is right and the code is buggy**.

## `Cart(items=None)`
- A brand-new `Cart()` starts **empty**.
- Two separate `Cart()` instances are **independent**: adding an item to one must
  NOT affect the other. (Each cart has its own items.)

## `add_item(name, price, qty=1)`
- Appends an item with the given name, price, and quantity to *this* cart only.

## `subtotal()`
- Returns the sum of `price * qty` across all items.
- An empty cart has a subtotal of `0`.

## `apply_discount(percent)`
- `percent` is a number from 0 to 100.
- Returns the cart total **after** the discount is applied.
  - Example: subtotal `100`, `apply_discount(10)` → **`90.0`** (you pay 90, not 10).
  - `apply_discount(0)` → the full subtotal.
  - `apply_discount(100)` → `0`.
- Raises `ValueError` if `percent` is below 0 or above 100.

## `is_eligible_for_free_shipping(threshold=50)`
- Free shipping applies when the subtotal is **at least** the threshold
  (i.e. subtotal **>=** threshold).
  - Subtotal exactly equal to the threshold **qualifies**.

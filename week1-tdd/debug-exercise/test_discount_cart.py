"""
Partial test suite for the Cart module.

The tests below already PASS — they establish the harness and show the AAA
style. They do NOT cover the buggy behaviour. Your job (see README.md) is to
ADD failing tests that expose each planted bug, watch them go red, then fix
discount_cart.py until they go green.
"""

import pytest
from discount_cart import Cart


def test_subtotal_of_empty_cart_is_zero():
    # Arrange
    cart = Cart()
    # Act / Assert
    assert cart.subtotal() == 0


def test_subtotal_sums_price_times_quantity():
    # Arrange
    cart = Cart()
    cart.add_item("apple", 2.0, qty=3)   # 6.0
    cart.add_item("bread", 4.0, qty=1)   # 4.0
    # Act / Assert
    assert cart.subtotal() == 10.0


def test_discount_rejects_out_of_range_percent():
    # Arrange
    cart = Cart()
    cart.add_item("apple", 10.0)
    # Act / Assert
    with pytest.raises(ValueError):
        cart.apply_discount(150)


# --- TODO (you): add tests that expose the three planted bugs ---

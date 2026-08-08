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
def test_two_carts_are_independent():
    # Arrange
    cart1 = Cart()
    cart2 = Cart()
    cart1.add_item("apple", 10.0)
    cart2.add_item("bread", 5.0)
    # Act / Assert
    assert cart1.subtotal() == 10.0
    assert cart2.subtotal() == 5.0


def test_subtotal_with_zero_quantity():
    # Arrange
    cart = Cart()
    cart.add_item("apple", 10.0, qty=0)
    # Act / Assert
    assert cart.subtotal() == 0.0


def test_discount_zero_percent_returns_full_price():
    # Arrange
    cart = Cart()
    cart.add_item("apple", 10.0)
    # Act / Assert
    assert cart.apply_discount(0) == 10.0
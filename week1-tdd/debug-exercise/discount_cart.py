"""
A small shopping-cart module for the Day 4 debugging exercise.

It LOOKS reasonable and some tests already pass — but it has THREE planted
bugs. The behaviour it is SUPPOSED to have is written in SPEC.md. Your job is
to make the code match the spec, test-first.

Do NOT rewrite the module from scratch. Diagnose, isolate, and fix.
"""


class Cart:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def add_item(self, name, price, qty=1):
        self.items.append({"name": name, "price": price, "qty": qty})

    def subtotal(self):
        """Total price of everything in the cart (price * qty, summed)."""
        return sum(item["price"] * item["qty"] for item in self.items)

    def apply_discount(self, percent):
        """Return the cart total AFTER applying a percentage discount.

        `percent` is a number from 0 to 100. See SPEC.md for exact behaviour.
        """
        if percent < 0 or percent > 100:
            raise ValueError("percent must be between 0 and 100")
        elif percent == 0:
            return self.subtotal()

        return self.subtotal() * (percent / 100)

    def is_eligible_for_free_shipping(self, threshold=50):
        """True if the cart qualifies for free shipping. See SPEC.md."""
        return self.subtotal() > threshold

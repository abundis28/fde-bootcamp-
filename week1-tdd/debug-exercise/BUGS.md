### Bug 1
- Symptom (what failed / wrong output): Shopping carts were not independent one from the other.
- Root cause (the actual defect in the code): Mutable object list was passed as argument and therefore shared between the shopping cart instances.
- Fix (what you changed): I changed the initialization of the class and the mutable object.
- Which test catches it: test_two_carts_are_independent()

### Bug 2
- Symptom (what failed / wrong output): If discount was 0, the returned subtotal was 0 instead of full price.
- Root cause (the actual defect in the code): There was no condition for 0 as input for discount. Mutiplying subtotal times 0, always returned 0.
- Fix (what you changed): Added condition to catch 0 discount scenario.
- Which test catches it: test_discount_zero_percent_returns_full_price()

### Bug 3
- Symptom (what failed / wrong output): If subtotal was equal to threshold, free shipping was rejected.
- Root cause (the actual defect in the code): Subtotal was being compared only to be greater than free shipping threshold. It was not compared to be at least equal to.
- Fix (what you changed): Changed the comparation from bigger than to bigger than or equal to.
- Which test catches it: test_free_shipping_threshold()
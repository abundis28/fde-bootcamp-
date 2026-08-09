### Bug 1
- Symptom (what failed / wrong output): Shopping carts were not independent one from the other.
- Root cause (the actual defect in the code): Mutable object list was passed as argument and therefore shared between the shopping cart instances.
- Fix (what you changed): I changed the initialization of the class and the mutable object.
- Which test catches it: test_two_carts_are_independent()

### Bug 2
- Symptom (what failed / wrong output): If discount was 0, the returned subtotal was 0 instead of full price.
- Root cause (the actual defect in the code): The calculation was wrong and was only multiplying the subtotal instead of the remaining part.
- Fix (what you changed): Corrected the calculation of the remaining subtotal after the discount.
- Which test catches it: test_discount_zero_percent_returns_full_price()

### Bug 3
- Symptom (what failed / wrong output): If subtotal was equal to threshold, free shipping was rejected.
- Root cause (the actual defect in the code): Subtotal was being compared only to be greater than free shipping threshold. It was not compared to be at least equal to.
- Fix (what you changed): Changed the comparation from bigger than to bigger than or equal to.
- Which test catches it: test_free_shipping_threshold()
# What I asked

1) First, analyze the new unstaged tests in test_main.py.
2) Second, provide feedback if any gap is identified.
3) Third, in main.py, implement the GET /orders/summary endpoint to meet and fulfill all the failing-unstaged tests.

# What it produced

It implemented the GET /orders/summary endpoint and identified a missing test for summary verification after patch.
I implemented the test and verified it was passing the provided implementation.

# What I changed/rejected

I did not change the implementation, but I verified two specific risks before accepting it:

1. **Zero-count statuses** — The summary endpoint could have used `collections.Counter`, which only produces keys for statuses that actually appear, silently dropping statuses with zero orders. I confirmed it instead seeds the dict from the `OrderStatus` enum (`{s.value: 0 for s in OrderStatus}`), guaranteeing all four keys are always present. This is what the tests assert.

2. **Route ordering** — FastAPI matches routes in declaration order. If `GET /orders/summary` had been placed after `GET /orders/{order_id}`, the string `"summary"` would be coerced to `int`, return 422, and the endpoint would never be reached. I confirmed the summary route is declared first in `main.py`.
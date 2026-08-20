# TransactionProcessor — intended behavior

This describes what `transaction_processor.py` is *supposed* to do. The code
already does it — your task is to critique the **design**, not fix bugs.

## `process(tx, customer_type, output_format, notify_channel)`
Given one transaction `tx` (a dict with at least `amount` and `description`):
1. **Validate** it has `amount` and `description` (else `ValueError`).
2. **Fee** by customer tier: free 3%, pro 2%, enterprise 1% (unknown → 3%).
3. **Tax set-aside** by category, inferred from the description prefix:
   `INV...` (invoice income) → 25%, `EXP...` (expense) → 0%, otherwise 15%.
4. **net = amount − fee − tax**; store the enriched record.
5. **Persist** the record to the database.
6. **Format** the record for the caller: `json`, `csv`, or `text`.
7. **Notify** the user via `email`, `sms`, or `slack`.
Returns the formatted string.

## `monthly_report(fmt)`
Returns the sum of `net` across all processed transactions, formatted as
`json`, `csv`, or `text`.

## Things the client says are coming soon (relevant to your critique)
- New customer tiers will be added over time.
- New output formats (e.g. PDF, XML) will be requested.
- New notification channels (e.g. push, webhook) are on the roadmap.
- They want to unit-test the fee/tax math **without** touching a real database
  or sending real emails.

# Day 4 — Debugging Exercise: the Buggy Cart

`discount_cart.py` has **three planted bugs**. It looks fine and the starter
tests pass, but its behaviour disagrees with `SPEC.md` in three places.

## Your job (test-first debugging)

For **each** of the three bugs:

1. **Reproduce** — write a test that encodes the *spec's* expected behaviour.
   Run it and watch it **fail (red)**. The failure output is your evidence the
   bug is real and that your test detects it.
2. **Isolate** — find the root cause. Read the traceback. Use `pytest -x`
   (stop at first failure), `pytest -k <name>` (run one test), and a
   breakpoint (`breakpoint()` in the code, or `pytest --pdb`) if you need to
   inspect state.
3. **Fix** — change `discount_cart.py` so the test passes (**green**). Make the
   smallest fix that satisfies the spec. Do not rewrite the module.
4. **Record** — add a one-line root-cause note to `BUGS.md` (template below).

## Rules
- The **spec is the source of truth**. If code and spec disagree, the code is wrong.
- One test per bug, minimum. Visible Arrange / Act / Assert.
- Commit per bug: the failing test + its fix together is fine, but your
  `BUGS.md` note should make the diagnosis clear.
- Keep the three starter tests passing.

## How to run
```bash
cd week1-tdd/debug-exercise
pytest -v
```

## BUGS.md template
Create `BUGS.md` and fill in one entry per bug:

```
### Bug 1
- Symptom (what failed / wrong output):
- Root cause (the actual defect in the code):
- Fix (what you changed):
- Which test catches it:
```

There are exactly three. When all your tests are green and `BUGS.md` has three
entries, push and tell me the branch.

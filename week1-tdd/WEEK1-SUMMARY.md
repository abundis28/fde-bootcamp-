# Week 1 — Test-Driven Development: In-Depth Summary

A complete reference for everything covered in Days 1–7, with the concepts, the
code idioms, the design decisions, and the recurring habits that turned into
muscle memory. Written against the actual work in this folder (`calculator`,
`task_store`, `debug-exercise`, `1_5_api_testing`, `udatracker`).

---

## The through-line

TDD inverts the usual order: **write a failing test that specifies the behavior,
then write the minimum code to pass it, then refactor under the test's
protection.** For a Forward Deployed Engineer this is how you earn trust — a
passing suite is your evidence that code works in a client's environment — and
it's how you use AI safely: **the test is the objective contract the AI (or you)
must satisfy.** You stop asking "does this look right?" and start asking "does it
pass the spec I wrote?"

The meta-lesson of the whole week, proven repeatedly on real code:
> **"Looks right" is not "works."** Green tests, plausible AI output, a CI file
> copied from a template — all can look correct and be wrong. The cure is to
> *run it and check the thing that could plausibly be wrong.*

---

## Day 1 — Why TDD & the Testing Pyramid

**Red → Green → Refactor.**
- **Red:** write a test for behavior that doesn't exist; run it; watch it fail.
  Red proves two things — the behavior is absent *and* the test can actually
  detect it. A test that passes the moment you write it is a yellow flag: it
  never demonstrated the red step, so you don't know it works.
- **Green:** the *minimum* code to pass. Not elegant — passing.
- **Refactor:** clean up with the test holding the line.

**The testing pyramid** (ratios, not just types):
- **Unit** (wide base) — one function/class in isolation; fast, numerous,
  pinpoint failures.
- **Integration** (middle) — pieces working together (code + DB, code + API).
- **End-to-end** (tip) — the whole system like a user; high confidence, slow,
  few. Inverting this (many E2E, few unit) is the "ice-cream-cone" anti-pattern.

Why TDD earns its place: it pushes bug detection as far *left* (early) as
possible, and the cost of a bug grows the later it's caught — seconds in a unit
test, an emergency call in a client's production.

---

## Day 2 — pytest & Arrange–Act–Assert; mapping tests to CRUD

**Every test has three visible phases:**
```python
def test_withdraw_reduces_balance():
    account = Account(balance=100)   # Arrange — set up known state
    account.withdraw(30)             # Act — the ONE action under test
    assert account.balance == 70     # Assert — check the outcome
```
One **Act** per test → one reason to fail → unambiguous diagnosis. If Arrange is
huge, the object is hard to construct (a design smell). If you can't isolate one
Act, the method does too much.

**CRUD as a test checklist** (Create/Read/Update/Delete). The happy path is easy;
the **edge cases are where client incidents live** — especially "what happens on
a missing id?" That's a *design decision you make on purpose*: return `None`, or
raise? In `task_store.py` the choice was **raise `KeyError`** with a clear,
self-authored message, applied *consistently* across get/update/delete.

**pytest essentials:** plain `assert` (rich failure output), `pytest.raises` for
exceptions, `-k <name>` to run a subset, `-x` to stop at first failure, `-v`
verbose.

**Key bug caught this day:** the first `TaskStore` kept redundant parallel state
(`tasks` list + `descriptions` set + `ids` set). `update_task` changed the task
but forgot to sync the `descriptions` set → the uniqueness invariant silently
broke, and no test caught it because the test only asserted the *visible field*,
not the *invariant*. Lesson: **assert the whole state is consistent after a
mutation, not just the thing you touched.** The fix was to back the store with a
single `dict[id → task]` (less redundant state = fewer bugs) and drop the
unjustified uniqueness rule entirely.

---

## Day 3 — Fixtures, Parameterization & Mocking

**Fixtures** — reusable Arrange, injected by name; fresh per test so nothing
leaks between tests:
```python
@pytest.fixture
def store():
    return TaskStore()

def test_add(store):          # pytest runs the fixture and passes it in
    ...
```
Composable (`store_with_task` builds on `store`), and support teardown via
`yield`.

**Parameterization** — one test, a table of cases; each row reported as its own
pass/fail:
```python
@pytest.mark.parametrize("description, completed", [
    (123, False),        # bad description
    ("ok", 12),          # bad completed
    (None, False),
])
def test_add_rejects_bad_types(store, description, completed):
    with pytest.raises(TypeError):
        store.add_task(Task(description, completed))
```
Adding a case is one line, so you cover more edge cases. **Gotcha learned:** a
single test can only trigger the *first* guard that fails — to cover each
validation guard to 100% you need a case that makes *only that guard* fire.

**Mocking** — replace what you don't control (clock, network, an injected
collaborator) with a controllable stand-in:
```python
gen = Mock(return_value=42)
store = TaskStore(id_generator=gen)
store.add_task(Task("x", False))
gen.assert_called_once()     # assert the INTERACTION, not just a return value
```
Two rules learned the hard way:
- **Mock what you don't own, not what you're testing.** Over-mocking (injecting a
  `Mock` into *every* test) meant the real default code path stopped being
  exercised — coverage silently dropped. Keep at least one test on the real path.
- **A mock without an assertion is pointless** — you have to assert it was used.

Mockability depends on **dependency injection** (passing dependencies in vs.
hard-coding them) — a direct preview of Week 2.

---

## Day 4 — Diagnosing Failures & Debugging

**The method (don't guess):** Reproduce → Isolate → Diagnose → Fix → Verify.
- **Reproduce** as a failing test — a bug you can't reproduce, you can't fix.
- **Isolate** — read the traceback *bottom-up* (last line = what blew up), shrink
  inputs, use `pytest -x`, `pytest -k`, `breakpoint()` / `pytest --pdb`.
- **Diagnose the root cause, not the symptom.** "Returns 10 instead of 90" is a
  symptom; "computes the discount *amount* instead of the discounted *total*" is
  the cause.
- **Fix** the smallest change that satisfies the spec; **Verify** the target goes
  green *and* nothing else regressed.

**The big lesson (learned by falling into the trap):** in `discount_cart.py` the
first fix special-cased `percent == 0` — patching the one input where the wrong
formula looked obviously broken, while the real defect (wrong formula for *all*
inputs) stayed live. The test was too narrow (only `percent=0`), so it went green
and confirmed nothing. **If the spec gives you a worked example (`10% off 100 =
90`), that example *is* a test — write it.** Also: **keep the written record
true** — a correct fix with a stale postmortem is a real hazard for whoever reads
it next.

---

## Day 5 — API Deep-Dive I: Integration Testing Real APIs

**HTTP vocabulary:**
- **Verbs & idempotency:** `GET` (safe, idempotent), `POST` (not idempotent —
  two POSTs = two resources), `PUT`/`PATCH` (replace/partial), `DELETE`
  (idempotent). Idempotent requests are safe to *retry* after a timeout; a naive
  `POST` is not (you might double-charge).
- **Status codes:** `2xx` success, `4xx` **caller's** fault (don't retry — fix
  the request; `404`, `422`, `429`), `5xx` **server's** fault (may retry). The
  4xx/5xx split *is* a design principle.
- **Auth** via headers (`Authorization: Bearer <key>`), never in URLs or code —
  from `.env`. **Pagination** and **rate limits** (`429`, `X-RateLimit-*`) are
  the things beginners forget.

**Real vs. mocked — you want both:**
- **Real integration test** proves the actual URL/auth/response-shape works; slow,
  networked, non-deterministic → run occasionally.
- **Mocked test** (`httpx` + `respx`) is fast, offline, deterministic, and can
  simulate `404`/`429`/`500` you can't trigger on demand → run always.
```python
@respx.mock
def test_handles_404():
    respx.get("https://api.github.com/users/ghost").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"}))
    ...
# real one marked so CI can skip it:
@pytest.mark.integration
def test_get_user_real(): ...
```
Split via `pytest -m "not integration"`.

**Bugs caught in `github_client.py`:**
- An `else` bound to the wrong `if` printed a fake "API Error" on every **200**.
  Tests didn't assert output, so it hid. → **assert side effects too.**
- A `try/except httpx.HTTPStatusError` that could never fire because
  `raise_for_status()` was never called — **dead error-handling that looks
  robust.**
- Returning the raw `Response` instead of parsed data — the "client" wasn't
  abstracting anything. Return `response.json()`.
- **404 and 500 raised the same exception type**, so a caller couldn't handle them
  differently — the *stated* design ("treat them differently") wasn't realized in
  code. Fixed with distinct `UserNotFoundError` / `GitHubServerError`.

---

## Day 6–7 — Udatracker (the milestone): building & testing an API

**FastAPI + Pydantic.** Validation lives in the *model*, declaratively — no
hand-rolled `isinstance` guards:
```python
class OrderItem(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int   = Field(gt=0)
    unit_price: float = Field(ge=0)     # >= 0: a free item is valid
```
**Separate the input model from the stored/returned model.** `ClientOrder` has
*only* the client-supplied fields (`customer_name`, `items`) — so the client
*cannot* set `id`, `total`, `status`, or `created_at`. That's how you enforce
"total is always server-computed": there's nowhere for the client to put it.
Verified by test — POSTing a bogus `total_amount`/`order_id`/`status` is ignored.

**Testing an API** with `TestClient` — in-process, no network, deterministic:
```python
client = TestClient(app)
resp = client.post("/orders", json=payload)
assert resp.status_code == 201
assert resp.json()["total_amount"] == 10.0   # server computed it
```

**Enums as one source of truth.** `OrderStatus(str, Enum)` used in the `status`
field, the `?status=` query param, and the PATCH body. Typing the query param as
the enum gives an automatic `422` for garbage **and** the default error body lists
the valid values — no custom handler needed.

**Error codes, precisely:**
- `404` — resource doesn't exist.
- `422` — malformed input (Pydantic handles it).
- `409 Conflict` — request is well-formed and the resource exists, but conflicts
  with its **current state**. Used for the business rule: **`cancelled` is
  terminal** — a cancelled order can't transition to anything else. This lives in
  the *handler* (it depends on stored state), not the model. Input validation vs.
  business-rule validation are two different layers.

**Design decisions made on purpose (with a "why" a client can hear):**
- `DELETE` → **soft delete** (mark `cancelled`) over hard delete, to preserve the
  audit trail merchants may need.
- `GET /orders/summary` returns **every status including zero counts**, because an
  omitted status is ambiguous (zero, or nonexistent?).

**Bugs & gotchas caught building it:**
- **The app depended on its test harness** — state was initialized only in
  fixtures, so `uvicorn main:app` crashed on the first request. Fix: the app owns
  its state (`app.state.orders = {}` at load); tests only *reset* it.
- **A fixture that only looked like it reset state** — `def client_restore(autouse=True)`
  put `autouse` in the function signature, not the `@pytest.fixture(autouse=True)`
  decorator, so it never ran. Signature vs. behavior again.
- **`?status=` was accidentally required**, breaking "list all orders." 100% *line*
  coverage still missed it because coverage measures lines executed, not
  *behaviors specified*. → **Test-drive from the spec's list of behaviors, not
  from "did I run every line."**
- **FastAPI route ordering:** `GET /orders/summary` must be declared *before*
  `GET /orders/{order_id}`, or `"summary"` gets coerced to `int` → 422.
- **Boundary consistency:** loosening `unit_price` to `ge=0` while `total_amount`
  stayed `gt=0` made an all-free order (total 0) crash with a 500. Two constraints
  touching the same value must agree at the edge.

**CI (the pre-flight checklist, automated):** `.github/workflows/ci.yml` runs the
suite on every push. Key fix — it must run `pytest -m "not integration"` so it
doesn't execute network-dependent tests that flake on CI rate limits. A CI that
reliably fails is worse than none: it trains the team to ignore red. And the file
"looking right" (copied from a template) didn't mean it *worked* for this repo —
you have to run it.

**TDD with AI (the finale):** you wrote strict, whole-dict tests for
`GET /orders/summary` *first* (red), then had Claude Code implement it. The strict
`assert body == {all four statuses...}` set a trap: a lazy `Counter` would drop
zero-count statuses and fail. The AI, held to that contract, seeded zeros
correctly. Crucially, you **verified the specific risks** (Counter vs. seeding;
route ordering) instead of accepting because it "looked right." That is the job.

---

## The habits (resurfacing tracker — all closed by end of Week 1)

1. **Commit granularity** — failing test and implementation as separate steps, so
   history proves test-first.
2. **Assert the invariant**, not just the visible field — after a mutation, the
   whole state must still be consistent.
3. **Fail for the right reason** — when you write/refactor a test, confirm it goes
   red for the cause you intend (not an unrelated arity or import error).
4. **Don't over-mock** — mock what you don't own; keep a test on the real path.
5. **Symptom vs. root cause** — fix the defect, not the loudest instance of it.
6. **The app owns its state** — tests verify behavior; they must never be a
   *dependency* of it.
7. **Boundary values** — when a spec says `≥`/`≤`, write the equals-case test.
8. **Signature vs. behavior** — make the code deliver what the interface promises
   (partial-update, exception types, `autouse`, CI command).
9. **"Looks right" ≠ "works"** — the umbrella lesson. Run it, probe the edge,
   check the thing that could plausibly be wrong. This is the core skill for
   working alongside AI, and the bridge to Week 4.

---

## Quick command reference

```bash
pytest -v                     # verbose: each test name + status
pytest -x                     # stop at first failure
pytest -k summary             # run tests matching "summary"
pytest --cov=main --cov-report=term-missing   # coverage + uncovered lines
pytest -m "not integration"   # skip network-dependent tests (CI)
pytest --pdb                  # drop into debugger at point of failure
uvicorn main:app --reload     # run the FastAPI app locally (/docs for Swagger)
```

## Tools introduced

`pytest` · `pytest-cov` · fixtures / parameterize / `monkeypatch` / `unittest.mock`
· `httpx` · `respx` · FastAPI · Pydantic · `TestClient` · Enums for validation ·
GitHub Actions CI.

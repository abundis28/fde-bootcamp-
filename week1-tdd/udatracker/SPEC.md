# Udatracker — Order Management System (Project Spec)

You are the forward-deployed engineer. A small merchant ("the client") needs an
order-management API. This document is the **contract** — the source of truth.
Build it **test-first**: write the tests that encode this spec, watch them fail,
then implement until they pass.

Stack: **FastAPI** + **Pydantic**, tested with FastAPI's **TestClient**.
Storage is **in-memory** for now (a dict, like your TaskStore) — no database.

---

## Domain

### Order
| Field         | Type              | Notes                                            |
|---------------|-------------------|--------------------------------------------------|
| `id`          | int               | Server-assigned. Starts at 1, increments.        |
| `customer_name` | str             | Required, non-empty.                             |
| `items`       | list[OrderItem]   | Required, **at least one** item.                 |
| `status`      | str               | One of: `pending`, `paid`, `shipped`, `cancelled`. New orders start `pending`. |
| `total`       | float             | **Server-computed**: sum of `quantity * unit_price` across items. Never trusted from the client. |
| `created_at`  | ISO 8601 datetime | Server-assigned at creation.                     |

### OrderItem
| Field        | Type  | Notes                          |
|--------------|-------|--------------------------------|
| `product`    | str   | Required, non-empty.           |
| `quantity`   | int   | Required, **> 0**.             |
| `unit_price` | float | Required, **>= 0**.            |

---

## Endpoints

### `POST /orders`  — create an order   *(Day 6)*
- Request body: `customer_name` and `items` (list of `{product, quantity, unit_price}`).
  The client does **not** send `id`, `status`, `total`, or `created_at`.
- On success → **201 Created**, returns the full order including the
  server-assigned `id`, `status="pending"`, computed `total`, and `created_at`.
- Validation failures → **422** (empty customer_name, empty items list,
  quantity <= 0, negative unit_price, missing fields). Pydantic gives you this.

### `GET /orders/{id}`  — fetch one order   *(Day 6)*
- Found → **200 OK** with the order.
- Not found → **404** with a clear error body.

### `GET /orders`  — list orders   *(Day 7)*
- Returns all orders. Supports optional `?status=` filter (e.g. `?status=pending`).
- Empty store, or a valid status with no matches → `200` with an empty list (not a 404).
- **Invalid status value** (e.g. `?status=123`) → **422**, with a body listing the
  valid statuses. Rationale: an unknown status is the caller's error (a 4xx), and
  must be distinguished from a valid-but-empty result. Enforce this by typing the
  query param as the `OrderStatus` enum so FastAPI validates it automatically —
  the same enum used for the order's `status` field and the PATCH endpoint.

### `PATCH /orders/{id}`  — update status   *(Day 7)*
- Body: `{"status": "<new status>"}`. Only `status` is mutable.
- Valid transition → **200** with the updated order.
- Unknown id → **404**. Invalid status value → **422**.
- **Business rule:** a `cancelled` order is terminal — it cannot move to any
  other status. Attempting to do so → **409 Conflict**.

### `DELETE /orders/{id}`  — cancel/remove   *(Day 7)*
- Removes the order (or marks it cancelled — your design choice, justify it).
- Unknown id → **404**.

---

## Rules that will be graded
- **`total` is always computed server-side.** If a client sends a `total`, ignore it.
- **Validation lives in the model**, not scattered through handlers.
- **The right status code for the right situation** (201 vs 200, 404 vs 422 vs 409).
- Storage is in-memory; a fresh app starts empty.
- Every endpoint is covered by tests written **before** its implementation.

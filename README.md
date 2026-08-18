# FDE 4-Week Bootcamp

---

## Udatracker — Order Management API

An in-memory REST API for managing customer orders, built with **FastAPI** and **Pydantic** following a test-first (TDD) approach.

---

### Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework and routing |
| `uvicorn` | ASGI server to run the app |
| `pydantic` | Request/response validation |
| `httpx` | HTTP client (used by FastAPI's TestClient) |
| `pytest` | Test runner |
| `pytest-cov` | Test coverage reporting |

---

### Installation

```bash
pip install -r requirements.txt
```

---

### Running the server

From the `week1-tdd/udatracker/` directory:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs are auto-generated at `http://127.0.0.1:8000/docs`.

---

### Running the tests

```bash
pytest week1-tdd/udatracker/test_main.py -v
```

With coverage:

```bash
pytest week1-tdd/udatracker/test_main.py --cov=week1-tdd/udatracker -v
```

---

### API Usage Guide

All examples assume the server is running at `http://127.0.0.1:8000`.

#### Create an order — `POST /orders`

```bash
curl -s -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "items": [
      {"product_id": "SKU-001", "quantity": 2, "unit_price": 15.00},
      {"product_id": "SKU-002", "quantity": 1, "unit_price": 30.00}
    ]
  }'
```

Returns **201** with the created order. `total_amount` and `order_id` are server-assigned — any values sent by the client are ignored.

---

#### Get a single order — `GET /orders/{id}`

```bash
curl -s http://127.0.0.1:8000/orders/1
```

Returns **200** with the order, or **404** if not found.

---

#### List orders — `GET /orders`

```bash
# All orders
curl -s http://127.0.0.1:8000/orders

# Filter by status (pending | paid | shipped | cancelled)
curl -s "http://127.0.0.1:8000/orders?status=pending"
```

Returns **200** with a list (empty list if no matches). An invalid status value returns **422**.

---

#### Update order status — `PATCH /orders/{id}`

```bash
curl -s -X PATCH http://127.0.0.1:8000/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

Valid statuses: `pending`, `paid`, `shipped`, `cancelled`.  
Returns **200** with the updated order, **404** if not found, **422** for an invalid status, or **409** if the order is already `cancelled` (terminal state).

---

#### Cancel an order — `DELETE /orders/{id}`

```bash
curl -s -X DELETE http://127.0.0.1:8000/orders/1
```

Marks the order as `cancelled` rather than removing it from storage — soft-delete preserves the audit trail so merchants can always look up what happened to a past order. Returns **200** on success or **404** if not found.

---

#### Order summary — `GET /orders/summary`

```bash
curl -s http://127.0.0.1:8000/orders/summary
```

Returns **200** with a count of orders per status:

```json
{"pending": 3, "paid": 1, "shipped": 2, "cancelled": 0}
```

All four statuses are always present, even when their count is zero.

---

### AI Usage

Claude Code was used to generate the `GET /orders/summary` implementation and flag the route-ordering risk. All output was reviewed before acceptance: the enum-seeding approach and route declaration order were verified manually against the test assertions.

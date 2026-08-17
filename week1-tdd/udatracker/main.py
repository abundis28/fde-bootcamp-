from enum import Enum
from fastapi import Body, FastAPI, HTTPException, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime, timezone

app = FastAPI()

app.state.orders = {}
app.state.next_order_id = 1

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"

class StatusModel(BaseModel):
    status: OrderStatus = Field(...)

class OrderItem(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=100, description="The unique identifier for the product")
    quantity: int = Field(..., gt=0, description="The quantity of the product ordered")
    unit_price: float = Field(..., ge=0, description="The price per unit of the product")

class Order(BaseModel):
    order_id: int = Field(..., ge=1, description="The unique identifier for the order")
    customer_name: str = Field(..., min_length=1, max_length=100, description="The name of the customer")
    items: list[OrderItem] = Field(..., min_length=1, description="The items in the order")
    status: OrderStatus = Field(..., description="The current status of the order")
    total_amount: float = Field(..., ge=0, description="The total amount for the order")
    created_at: str = Field(..., description="The date and time when the order was created")

class ClientOrder(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100, description="The name of the customer")
    items: list[OrderItem] = Field(..., min_length=1, description="The items in the order")

def calculate_total_amount(items: list[OrderItem]) -> float:
    return sum(item.quantity * item.unit_price for item in items)

@app.get("/orders/{order_id}")
def get_order(order_id: int = Path(..., ge=1)):
    orders = app.state.orders
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

@app.get("/orders")
def get_order_query(status: OrderStatus):
    orders = app.state.orders
    return [order for order in orders.values() if order["status"] == status]

@app.post("/orders")
def create_order(client_order: ClientOrder):
    orders = app.state.orders
    next_id = app.state.next_order_id
    app.state.next_order_id += 1

    total_amount = calculate_total_amount(client_order.items)
    order = Order(
        order_id=next_id,
        customer_name=client_order.customer_name,
        items=client_order.items,
        status="pending",
        total_amount=total_amount,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    orders[order.order_id] = order.model_dump()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=order.model_dump())

@app.patch("/orders/{order_id}")
def update_order_status(order_id: int = Path(..., ge=1), payload: StatusModel = Body(...)):
    new_status = payload.status
    orders = app.state.orders
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    if orders[order_id]["status"] == OrderStatus.cancelled:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Cannot update a cancelled order"})
    orders[order_id]["status"] = new_status
    return orders[order_id]

@app.delete("/orders/{order_id}")
def delete_order(order_id: int = Path(..., ge=1)):
    orders = app.state.orders
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    orders[order_id]["status"] = OrderStatus.cancelled
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Order cancelled successfully"})
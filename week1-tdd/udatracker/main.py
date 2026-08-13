from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

app = FastAPI()

class OrderItem(BaseModel):
    product_id: int = Field(..., description="The unique identifier for the product")
    quantity: int = Field(..., gt=0, description="The quantity of the product ordered")
    unit_price: float = Field(..., gt=0, description="The price per unit of the product")

class Order(BaseModel):
    order_id: int = Field(..., ge=1, description="The unique identifier for the order")
    customer_name: str = Field(..., min_length=1, max_length=100, description="The name of the customer")
    items: list[OrderItem] = Field(..., description="The items in the order")
    status: str = Field(..., min_length=2, max_length=100, description="The current status of the order")
    total_amount: float = Field(..., gt=0, description="The total amount for the order")
    created_at: str = Field(..., description="The date and time when the order was created")

@app.get("/orders/{order_id}")
def get_order(order_id: int = Path(..., ge=1)):
    orders = app.state.orders
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

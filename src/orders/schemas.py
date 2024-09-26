from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class OrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


class SOrderAdd(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: OrderStatus = OrderStatus.IN_PROCESS


class SOrderItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

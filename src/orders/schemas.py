from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class SOrderStatus(str, Enum):
    IN_PROCESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


class SOrderItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class SOrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class SOrderAdd(BaseModel):
    order_items: List[SOrderItemAdd]

    model_config = ConfigDict(from_attributes=True)


class SOrder(BaseModel):
    id: int
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: SOrderStatus = SOrderStatus.IN_PROCESS
    order_items: List[SOrderItem]

    model_config = ConfigDict(from_attributes=True)

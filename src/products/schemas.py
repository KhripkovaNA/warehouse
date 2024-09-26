from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SProductAdd(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class SProduct(SProductAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

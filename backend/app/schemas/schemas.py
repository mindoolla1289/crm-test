from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.models import OrderStatus


# ─── Client ────────────────────────────────────────────────────────────────

class ClientBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ClientOut(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Equipment ─────────────────────────────────────────────────────────────

class EquipmentBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class EquipmentOut(EquipmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Order ──────────────────────────────────────────────────────────────────

class OrderBase(BaseModel):
    client_id: int
    equipment_id: int
    comment: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class OrderUpdate(BaseModel):
    client_id: Optional[int] = None
    equipment_id: Optional[int] = None
    comment: Optional[str] = None
    status: Optional[OrderStatus] = None

class OrderOut(BaseModel):
    id: int
    comment: Optional[str]
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime]
    client: ClientOut
    equipment: EquipmentOut

    class Config:
        from_attributes = True


# ─── Pagination ─────────────────────────────────────────────────────────────

class PaginatedOrders(BaseModel):
    items: List[OrderOut]
    total: int
    page: int
    page_size: int
    pages: int
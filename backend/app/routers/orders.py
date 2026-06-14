from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
import math
from app.database import get_db
from app.models.models import Order, OrderStatus
from app.schemas.schemas import OrderCreate, OrderOut, OrderUpdate, PaginatedOrders

router = APIRouter()


@router.get("/", response_model=PaginatedOrders)
def get_orders(
    status: Optional[OrderStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    query = db.query(Order).options(
        joinedload(Order.client),
        joinedload(Order.equipment),
    )

    if status:
        query = query.filter(Order.status == status)

    if sort_order == "asc":
        query = query.order_by(Order.created_at.asc())
    else:
        query = query.order_by(Order.created_at.desc())

    total = query.count()
    pages = math.ceil(total / page_size) if total > 0 else 1
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedOrders(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .options(joinedload(Order.client), joinedload(Order.equipment))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return order


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return (
        db.query(Order)
        .options(joinedload(Order.client), joinedload(Order.equipment))
        .filter(Order.id == order.id)
        .first()
    )


@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return (
        db.query(Order)
        .options(joinedload(Order.client), joinedload(Order.equipment))
        .filter(Order.id == order.id)
        .first()
    )


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(order)
    db.commit()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Equipment
from app.schemas.schemas import EquipmentCreate, EquipmentOut, EquipmentUpdate

router = APIRouter()


@router.get("/", response_model=List[EquipmentOut])
def get_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).order_by(Equipment.name).all()


@router.get("/{equipment_id}", response_model=EquipmentOut)
def get_one(equipment_id: int, db: Session = Depends(get_db)):
    item = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Техника не найдена")
    return item


@router.post("/", response_model=EquipmentOut, status_code=201)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db)):
    item = Equipment(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{equipment_id}", response_model=EquipmentOut)
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    item = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Техника не найдена")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    item = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Техника не найдена")
    db.delete(item)
    db.commit()
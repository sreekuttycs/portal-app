from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member_address import MemberAddress
from app.admin.schemas.member_address import (
    MemberAddressCreate, MemberAddressUpdate, MemberAddressOut
)
from typing import List

router = APIRouter(prefix="/member_addresses")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MemberAddressOut)
def create_member_address(address: MemberAddressCreate, db: Session = Depends(get_db)):
    new_address = MemberAddress(**address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@router.get("/", response_model=List[MemberAddressOut])
def list_member_addresses(db: Session = Depends(get_db)):
    return db.query(MemberAddress).all()

@router.get("/{address_id}", response_model=MemberAddressOut)
def get_member_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(MemberAddress).filter(MemberAddress.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=MemberAddressOut)
def update_member_address(address_id: int, address_data: MemberAddressUpdate, db: Session = Depends(get_db)):
    address = db.query(MemberAddress).filter(MemberAddress.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address_data.dict(exclude_unset=True).items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address

@router.delete("/{address_id}")
def delete_member_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(MemberAddress).filter(MemberAddress.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return {"message": "Address deleted successfully"}

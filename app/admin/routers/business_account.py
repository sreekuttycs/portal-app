from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.business_account import BusinessAccount
from app.admin.schemas.business_account import (
    BusinessAccountCreate,
    BusinessAccountUpdate,
    BusinessAccountOut,
    BusinessAccountIdRequest
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/list", response_model=list[BusinessAccountOut])
def list_business_accounts(db: Session = Depends(get_db)):
    return db.query(BusinessAccount).all()


@router.post("/create", response_model=BusinessAccountOut)
def create_business_account(data: BusinessAccountCreate, db: Session = Depends(get_db)):
    new_account = BusinessAccount(**data.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.post("/details", response_model=BusinessAccountOut)
def get_business_account(data: BusinessAccountIdRequest, db: Session = Depends(get_db)):
    account = db.query(BusinessAccount).filter(BusinessAccount.id == data.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Business account not found")
    return account
    

@router.post("/update", response_model=BusinessAccountOut)
def update_business_account(data: BusinessAccountUpdate, db: Session = Depends(get_db)):
    account = db.query(BusinessAccount).filter(BusinessAccount.id == data.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Business account not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account

@router.delete("/delete")
def delete_business_account(data: BusinessAccountIdRequest, db: Session = Depends(get_db)):
    account = db.query(BusinessAccount).filter(BusinessAccount.id == data.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Business account not found")
    db.delete(account)
    db.commit()
    return {"message": "Business account deleted successfully"}

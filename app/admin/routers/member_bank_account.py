from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from typing import List
from app.admin.models.member_bank_account import MemberBankAccount
from app.admin.schemas.member_bank_account import (
    MemberBankAccountCreate,
    MemberBankAccountUpdate,
    MemberBankAccountOut,
)

router = APIRouter(prefix="/bank-accounts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MemberBankAccountOut)
def create_bank_account(data: MemberBankAccountCreate, db: Session = Depends(get_db)):
    bank_account = MemberBankAccount(**data.dict())
    db.add(bank_account)
    db.commit()
    db.refresh(bank_account)
    return bank_account


@router.get("/", response_model=List[MemberBankAccountOut])
def list_bank_accounts(db: Session = Depends(get_db)):
    return db.query(MemberBankAccount).all()


@router.get("/{account_id}", response_model=MemberBankAccountOut)
def get_bank_account(account_id: int, db: Session = Depends(get_db)):
    bank_account = db.query(MemberBankAccount).filter(MemberBankAccount.id == account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return bank_account


@router.put("/{account_id}", response_model=MemberBankAccountOut)
def update_bank_account(
    account_id: int,
    data: MemberBankAccountUpdate,
    db: Session = Depends(get_db),
):
    bank_account = db.query(MemberBankAccount).filter(MemberBankAccount.id == account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(bank_account, field, value)

    db.commit()
    db.refresh(bank_account)
    return bank_account


@router.delete("/{account_id}")
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    bank_account = db.query(MemberBankAccount).filter(MemberBankAccount.id == account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db.delete(bank_account)
    db.commit()
    return {"detail": "Bank account deleted"}

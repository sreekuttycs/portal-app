from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member_type import MemberType
from app.admin.schemas.member_type import (
    MemberTypeCreate,
    MemberTypeUpdate,
    MemberTypeOut,
    MemberTypeIdRequest
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/list", response_model=list[MemberTypeOut])
def list_member_types(db: Session = Depends(get_db)):
    return db.query(MemberType).all()


@router.post("/create", response_model=MemberTypeOut)
def create_member_type(data: MemberTypeCreate, db: Session = Depends(get_db)):
    new_type = MemberType(**data.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.post("/details", response_model=MemberTypeOut)
def get_member_type(data: MemberTypeIdRequest, db: Session = Depends(get_db)):
    member_type = db.query(MemberType).filter(MemberType.id == data.id).first()
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    return member_type


@router.post("/update", response_model=MemberTypeOut)
def update_member_type(data: MemberTypeUpdate, db: Session = Depends(get_db)):
    member_type = db.query(MemberType).filter(MemberType.id == data.id).first()
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(member_type, key, value)
    db.commit()
    db.refresh(member_type)
    return member_type


@router.delete("/delete")
def delete_member_type(data: MemberTypeIdRequest, db: Session = Depends(get_db)):
    member_type = db.query(MemberType).filter(MemberType.id == data.id).first()
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    db.delete(member_type)
    db.commit()
    return {"message": "Member type deleted successfully"}

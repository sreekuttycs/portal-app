from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member_role import MemberRole
from app.admin.schemas.member_role import (
    MemberRoleCreate,
    MemberRoleUpdate,
    MemberRoleOut,
    MemberRoleIdRequest
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/list", response_model=list[MemberRoleOut])
def list_member_roles(db: Session = Depends(get_db)):
    return db.query(MemberRole).all()


@router.post("/create", response_model=MemberRoleOut)
def create_member_role(data: MemberRoleCreate, db: Session = Depends(get_db)):
    existing = db.query(MemberRole).filter(MemberRole.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    new_role = MemberRole(**data.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.post("/details", response_model=MemberRoleOut)
def get_member_role(data: MemberRoleIdRequest, db: Session = Depends(get_db)):
    role = db.query(MemberRole).filter(MemberRole.id == data.id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/update", response_model=MemberRoleOut)
def update_member_role(data: MemberRoleUpdate, db: Session = Depends(get_db)):
    role = db.query(MemberRole).filter(MemberRole.id == data.id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return role


@router.delete("/delete")
def delete_member_role(data: MemberRoleIdRequest, db: Session = Depends(get_db)):
    role = db.query(MemberRole).filter(MemberRole.id == data.id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
    return {"message": "Member role deleted successfully"}

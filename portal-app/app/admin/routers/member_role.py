from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member_role import MemberRole
from app.admin.schemas.member_role import (
    MemberRoleCreate, MemberRoleUpdate, MemberRoleOut
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create
@router.post("/", response_model=MemberRoleOut)
def create_member_role(data: MemberRoleCreate, db: Session = Depends(get_db)):
    existing = db.query(MemberRole).filter(MemberRole.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    new_role = MemberRole(**data.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# List all
@router.get("/", response_model=list[MemberRoleOut])
def list_member_roles(db: Session = Depends(get_db)):
    return db.query(MemberRole).all()

# Get one
@router.get("/{role_id}", response_model=MemberRoleOut)
def get_member_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(MemberRole).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Update
@router.put("/{role_id}", response_model=MemberRoleOut)
def update_member_role(role_id: int, data: MemberRoleUpdate, db: Session = Depends(get_db)):
    role = db.query(MemberRole).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return role

# Delete
@router.delete("/{role_id}", status_code=204)
def delete_member_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(MemberRole).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
    return

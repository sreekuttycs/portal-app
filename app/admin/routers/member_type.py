from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member_type import MemberType
from app.admin.schemas.member_type import (
    MemberTypeCreate, MemberTypeUpdate, MemberTypeOut
)

router = APIRouter(
    prefix="/admin/member-types",
    tags=["Member Types"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Create a new member type
@router.post("/", response_model=MemberTypeOut)
def create_member_type(data: MemberTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(MemberType).filter(MemberType.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    new_type = MemberType(**data.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

# 🔹 List all member types
@router.get("/", response_model=list[MemberTypeOut])
def list_member_types(db: Session = Depends(get_db)):
    return db.query(MemberType).all()

# 🔹 Get a specific member type by ID
@router.get("/{member_type_id}", response_model=MemberTypeOut)
def get_member_type(member_type_id: int, db: Session = Depends(get_db)):
    member_type = db.query(MemberType).get(member_type_id)
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")
    return member_type

# 🔹 Update a member type
@router.put("/{member_type_id}", response_model=MemberTypeOut)
def update_member_type(
    member_type_id: int,
    data: MemberTypeUpdate,
    db: Session = Depends(get_db)
):
    member_type = db.query(MemberType).get(member_type_id)
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(member_type, key, value)

    db.commit()
    db.refresh(member_type)
    return member_type

# 🔹 Delete a member type
@router.delete("/{member_type_id}", status_code=204)
def delete_member_type(member_type_id: int, db: Session = Depends(get_db)):
    member_type = db.query(MemberType).get(member_type_id)
    if not member_type:
        raise HTTPException(status_code=404, detail="Member type not found")

    db.delete(member_type)
    db.commit()
    return

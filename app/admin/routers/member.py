from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.member import Member
from app.admin.schemas.member import MemberCreate, MemberUpdate, MemberOut

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create member
@router.post("/", response_model=MemberOut)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


# Get all members
@router.get("/", response_model=list[MemberOut])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()


# Get member by ID
@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


# Update member
@router.put("/{member_id}", response_model=MemberOut)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Update fields
    for key, value in member_update.dict(exclude_unset=True).items():
        setattr(db_member, key, value)

    db.commit()
    db.refresh(db_member)
    return db_member

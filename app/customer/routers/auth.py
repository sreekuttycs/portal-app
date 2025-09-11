from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.admin.models.member import Member
from app.database import SessionLocal
from app.admin.models.member_type import MemberType
from app.customer.models.user import User
from app.utils.auth_utils import create_access_token, verify_password
from app.customer.schemas.auth import LoginRequest, LoginResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == payload.email).first()

    if not db_user or not verify_password(payload.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if db_user.email_verified_at is None:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    # fetch member + join with member_types
    member = (
        db.query(Member)
        .filter(Member.user_id == db_user.id)
        .join(MemberType, Member.member_type_id == MemberType.id)
        .first()
    )

    role_slug = member.member_type.slug if member and member.member_type else None
    first_name = member.first_name if member else None
    last_name = member.last_name if member else None

    # issue JWT with role slug
    access_token = create_access_token(data={"sub": db_user.email, "role": role_slug})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_slug,
        "first_name": first_name,
        "last_name": last_name,
    }


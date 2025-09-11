from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.customer.models.user import User
from app.customer.models.user_email_verification import UserEmailVerification
from app.customer.schemas.user import UserCreate, UserResponse
from typing import List
from passlib.context import CryptContext
from app.customer.schemas.user_email_verification import UserEmailVerificationOut
from datetime import datetime, timedelta
import uuid
from app.utils.email_service import send_verification_email, send_password_reset_email

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        username=user.username,
        mobile_number=user.mobile_number,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token
    token = str(uuid.uuid4())
    verification_entry = UserEmailVerification(
        user_id=new_user.id,
        email_address=new_user.email,
        verification_token=token,
        created_at=datetime.utcnow()
    )
    db.add(verification_entry)
    db.commit()

    # Send verification email in background
    background_tasks.add_task(
        send_verification_email,
        to_email=new_user.email,
        username=new_user.username,
        token=token
    )

    return new_user

# verify token

@router.post("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    verification = db.query(UserEmailVerification).filter(
        UserEmailVerification.verification_token == token
    ).first()

    if not verification:
        raise HTTPException(status_code=400, detail="Invalid token")

    if verification.verified_at:
        raise HTTPException(status_code=400, detail="Token already used")

    # Expiry check (12 hours from created_at)
    expiry_time = verification.created_at + timedelta(hours=12)
    if datetime.utcnow() > expiry_time:
        raise HTTPException(status_code=400, detail="Verification link expired")    

    user = db.query(User).filter(User.id == verification.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update both tables
    now = datetime.utcnow()
    verification.verified_at = now
    user.email_verified_at = now   

    db.commit()

    return {"message": "Email verified successfully"}

    #forgot password

@router.post("/forgot-password")
def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    reset_entry = UserEmailVerification(
        user_id=user.id,
        email_address=user.email,
        verification_token=token,
        created_at=datetime.utcnow()
    )
    db.add(reset_entry)
    db.commit()

    background_tasks.add_task(
        send_password_reset_email,
        to_email=user.email,
        username=user.username,
        token=token
    )

    return {"message": "Password reset link sent"}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # 1. Find token
    reset_entry = db.query(UserEmailVerification).filter(
        UserEmailVerification.verification_token == token
    ).first()

    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid token")

    # 2. Check expiry
    expiry_time = reset_entry.created_at + timedelta(hours=12)
    if datetime.utcnow() > expiry_time:
        raise HTTPException(status_code=400, detail="Verification link expired")   

    # 3. Get user
    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 4. Update password (hash it!)
    user.password = hash_password(new_password)
    db.commit()

    # 5. Invalidate token (delete it so it can’t be reused)
    db.delete(reset_entry)
    db.commit()

    return {"message": "Password reset successful"}


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

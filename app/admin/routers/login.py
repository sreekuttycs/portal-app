from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
# from app.admin.models.user import User
from passlib.context import CryptContext # for hashed passwords
from app.admin.schemas.login import (
    LoginRequest, LoginResponse
)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency for DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/login", response_model=LoginResponse)
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     # Find by username OR email
#     user = (
#         db.query(User)
#         .filter(
#             (User.username == request.username_or_email) |
#             (User.email == request.username_or_email)
#         )
#         .first()
#     )

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid username/email or password")

#     if not pwd_context.verify(request.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid username/email or password")

#     if not user.email_verified_at:
#         return LoginResponse(success=False, message="Please verify your email address.")

#     return LoginResponse(success=True, message="Login successful!")

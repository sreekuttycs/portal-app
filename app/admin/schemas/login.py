from pydantic import BaseModel, constr


# Request schema
class LoginRequest(BaseModel):
    username_or_email: str
    password: str


# Response schema
class LoginResponse(BaseModel):
    success: bool
    message: str
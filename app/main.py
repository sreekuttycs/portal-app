from fastapi import FastAPI
from app.admin.routers import user
from app.admin.routers import member_type
from app.admin.routers import member_role
from app.admin.routers import country
from app.admin.routers import currency
from app.admin.routers import member
from app.admin.routers import member_address


app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(member_type.router, prefix="/member-types", tags=["Member Types"])
app.include_router(member_role.router, prefix="/member-roles", tags=["Member Roles"])
app.include_router(country.router, prefix="/countries", tags=["Countries"])
app.include_router(currency.router, prefix="/currencies", tags=["Currencies"])
app.include_router(member.router, prefix="/members", tags=["Members"])
app.include_router(member_address.router, prefix="/member_address", tags=["Member Address"])

@app.get("/")
def root():
    return {"message": "FastAPI Portal is running!"}

from fastapi import FastAPI
from app.admin.routers import user
from app.admin.routers import member_type
from app.admin.routers import member_role
from app.admin.routers import country
from app.admin.routers import currency
from app.admin.routers import member
from app.admin.routers import member_address
from app.admin.routers import member_bank_account
from app.admin.routers import service_group
from app.admin.routers import service_category
from app.admin.routers import service
from app.admin.routers import plan
from app.admin.routers import plan_pricing

from app.customer.routers import subscription

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(member_type.router, prefix="/member-types", tags=["Member Types"])
app.include_router(member_role.router, prefix="/member-roles", tags=["Member Roles"])
app.include_router(country.router, prefix="/countries", tags=["Countries"])
app.include_router(currency.router, prefix="/currencies", tags=["Currencies"])
app.include_router(member.router, prefix="/members", tags=["Members"])
app.include_router(member_address.router, prefix="/member-address", tags=["Member Address"])
app.include_router(member_bank_account.router, prefix="/member-bank_account", tags=["Member Bank Account"])
app.include_router(service_group.router, prefix="/service-group", tags=["Service Group"])
app.include_router(service_category.router, prefix="/service-category", tags=["Service Category"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(plan.router, prefix="/plans", tags=["Plans"])
app.include_router(plan_pricing.router, prefix="/plan-pricing", tags=["Plan Pricing"])

app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])

@app.get("/")
def root():
    return {"message": "FastAPI Portal is running!"}

from fastapi import FastAPI
from app.customer.routers import user
from app.customer.routers import subscription
from app.customer.routers import auth


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
from app.admin.routers import business_account
from app.admin.routers import project_status
from app.admin.routers import project
from app.admin.routers import project_member
from app.admin.routers import login
from dotenv import load_dotenv
import os

# Go up one level to find .env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


app = FastAPI()

app.include_router(auth.router, prefix="/login", tags=["Login"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(member_type.router, prefix="/member-types", tags=["Member Types"])
app.include_router(member_role.router, prefix="/member-roles", tags=["Member Roles"])
app.include_router(country.router, prefix="/countries", tags=["Countries"])
app.include_router(currency.router, prefix="/currencies", tags=["Currencies"])
app.include_router(member.router, prefix="/members", tags=["Members"])
app.include_router(member_address.router, prefix="/member-address", tags=["Member Address"])
app.include_router(member_bank_account.router, prefix="/member-bank_accounts", tags=["Member Bank Account"])
app.include_router(service_group.router, prefix="/service-group", tags=["Service Group"])
app.include_router(service_category.router, prefix="/service-category", tags=["Service Category"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(plan.router, prefix="/plans", tags=["Plans"])
app.include_router(plan_pricing.router, prefix="/plan-pricing", tags=["Plan Pricing"])
app.include_router(business_account.router, prefix="/business-account", tags=["Business Account"])
app.include_router(project_status.router, prefix="/project-status", tags=["Project Status"])
app.include_router(project.router, prefix="/projects", tags=["Projects"])
app.include_router(project_member.router, prefix="/project-members", tags=["Project Members"])
app.include_router(login.router, prefix="/auth", tags=["auth"])


app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])


print("Loaded .env from:", BASE_DIR / ".env")
print("MAILGUN_API_KEY:", os.getenv("MAILGUN_API_KEY"))
print("MAILGUN_DOMAIN:", os.getenv("MAILGUN_DOMAIN"))

@app.get("/")
def root():
    return {"message": "FastAPI Portal is running!"}

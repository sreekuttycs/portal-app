from fastapi import FastAPI
from app.routers import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "FastAPI Portal is running!"}

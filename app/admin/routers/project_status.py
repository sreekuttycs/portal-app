from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.admin.models.project_status import ProjectStatus
from app.admin.schemas.project_status import ProjectStatusCreate, ProjectStatusUpdate, ProjectStatusOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProjectStatusOut)
def create_project_status(data: ProjectStatusCreate, db: Session = Depends(get_db)):
    new_status = ProjectStatus(**data.dict())
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

@router.get("/{status_id}", response_model=ProjectStatusOut)
def get_project_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(ProjectStatus).filter(ProjectStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Project status not found")
    return status

@router.put("/{status_id}", response_model=ProjectStatusOut)
def update_project_status(status_id: int, data: ProjectStatusUpdate, db: Session = Depends(get_db)):
    status = db.query(ProjectStatus).filter(ProjectStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Project status not found")
    for key, value in data.dict().items():
        setattr(status, key, value)
    db.commit()
    db.refresh(status)
    return status

@router.delete("/{status_id}")
def delete_project_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(ProjectStatus).filter(ProjectStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Project status not found")
    db.delete(status)
    db.commit()
    return {"message": "Project status deleted successfully"}

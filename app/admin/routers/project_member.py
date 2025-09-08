from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.admin.models.project_member import ProjectMember
from app.admin.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate, ProjectMemberOut

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=ProjectMemberOut)
def create_project_member(data: ProjectMemberCreate, db: Session = Depends(get_db)):
    new_member = ProjectMember(**data.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.get("/{project_id}", response_model=list[ProjectMemberOut])
def get_project_members(project_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.ProjectMember.id,
            models.ProjectMember.project_id,
            models.ProjectMember.member_role_id,
            models.ProjectMember.member_id,
            models.ProjectMember.created_at,
            models.Member.first_name,
            models.Member.last_name,
            models.Member.email
        )
        .join(models.Member, models.ProjectMember.member_id == models.Member.id)
        .filter(models.ProjectMember.project_id == project_id)
        .all()
    )

    return [ProjectMemberOut.from_orm(row) for row in results]


@router.get("/{member_id}", response_model=ProjectMemberOut)
def get_project_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(ProjectMember).filter(ProjectMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Project member not found")
    return member


@router.put("/{member_id}", response_model=ProjectMemberOut)
def update_project_member(member_id: int, data: ProjectMemberUpdate, db: Session = Depends(get_db)):
    member = db.query(ProjectMember).filter(ProjectMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Project member not found")

    for key, value in data.dict().items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}")
def delete_project_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(ProjectMember).filter(ProjectMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Project member not found")

    db.delete(member)
    db.commit()
    return {"detail": "Project member deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import SessionLocal
from app.admin.models.project import Project
from app.admin.models.project_member import ProjectMember
from app.admin.models.member import Member 
from app.admin.models.member_role import MemberRole
from app.admin.models.business_account import BusinessAccount
from app.customer.schemas.project import (
    ProjectOut, ProjectIDRequest, ProjectMemberOut, ProjectSlugRequest
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# List all projects

@router.get("/list", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    projects = (
        db.query(Project)
        .join(BusinessAccount, BusinessAccount.id == Project.business_account_id)
        .options(joinedload(Project.project_status))
        .add_columns(BusinessAccount.name.label("business_account_name"))
        .all()
    )

    return [
        ProjectOut(
            id=p.Project.id,
            business_account_id=p.Project.business_account_id,
            business_account_name=p.business_account_name,   # 👈 include name
            project_status_id=p.Project.project_status_id,
            slug=p.Project.slug,
            name=p.Project.name,
            short_description=p.Project.short_description,
            start_date=p.Project.start_date,
            created_at=p.Project.created_at,
            updated_at=p.Project.updated_at,
            status=p.Project.project_status.label if p.Project.project_status else None
        )
        for p in projects
    ]

# Get project detail (via body)
@router.post("/detail", response_model=ProjectOut)
def get_project(request: ProjectIDRequest, db: Session = Depends(get_db)):
    project = db.query(Project).options(joinedload(Project.project_status)).get(request.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectOut(
        id=project.id,
        business_account_id=project.business_account_id,
        project_status_id=project.project_status_id,
        slug=project.slug,
        name=project.name,
        short_description=project.short_description,
        start_date=project.start_date,
        created_at=project.created_at,
        updated_at=project.updated_at,
        status=project.project_status.label if project.project_status else None
    )

# List all project members

@router.post("/members/list", response_model=List[ProjectMemberOut])
def list_project_members(request: ProjectSlugRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.slug == request.slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = (
        db.query(ProjectMember)
        .join(Member, ProjectMember.member_id == Member.id)
        .join(MemberRole, ProjectMember.member_role_id == MemberRole.id)
        .filter(ProjectMember.project_id == project.id)
        .all()
    )

    return [
        ProjectMemberOut(
            id=pm.id,
            project_id=pm.project_id,
            member_id=pm.member_id,
            first_name=pm.member.first_name if pm.member else None,
            last_name=pm.member.last_name if pm.member else None,
            phone=pm.member.phone if pm.member else None,
            email=pm.member.email if pm.member else None,
            member_role=pm.member_role.label if pm.member_role else None
        )
        for pm in members
    ]


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import SessionLocal
from app.admin.models.project import Project
from app.admin.models.project_member import ProjectMember
from app.admin.models.member import Member 
from app.admin.models.member_role import MemberRole
from app.admin.models.business_account import BusinessAccount
from app.admin.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectOut, ProjectIDRequest, ProjectMemberOut, ProjectSlugRequest, ProjectMemberAdd
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create project
@router.post("/", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(**data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return ProjectOut(
        id=new_project.id,
        business_account_id=new_project.business_account_id,
        project_status_id=new_project.project_status_id,
        slug=new_project.slug,
        name=new_project.name,
        short_description=new_project.short_description,
        start_date=new_project.start_date,
        created_at=new_project.created_at,
        updated_at=new_project.updated_at,
        status=new_project.project_status.label if new_project.project_status else None
    )


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


# Update project (via body)
@router.put("/update", response_model=ProjectOut)
def update_project(
    request: ProjectIDRequest,
    data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).get(request.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

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


# Delete project (via body)
@router.delete("/", response_model=dict)
def delete_project(request: ProjectIDRequest, db: Session = Depends(get_db)):
    project = db.query(Project).get(request.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}

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

# Add a member to project

@router.post("/members/add", response_model=ProjectMemberOut)
def add_project_member(
    data: ProjectMemberAdd,
    db: Session = Depends(get_db)
):
    # Find project by slug
    project = db.query(Project).filter(Project.slug == data.slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if member already exists in this project
    existing = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id, ProjectMember.member_id == data.member_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Member already in project")

    # Create new ProjectMember
    new_member = ProjectMember(
        project_id=project.id,
        member_id=data.member_id,
        member_role_id=data.member_role_id
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return ProjectMemberOut(
        id=new_member.id,
        project_id=new_member.project_id,
        member_id=new_member.member_id,
        first_name=new_member.member.first_name if new_member.member else None,
        last_name=new_member.member.last_name if new_member.member else None,
        phone=new_member.member.phone if new_member.member else None,
        email=new_member.member.email if new_member.member else None,
        member_role=new_member.member_role.label if new_member.member_role else None
    )

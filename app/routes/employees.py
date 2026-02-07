from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/employees", tags=["Employees"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ➕ Add Employee
@router.post("/")
def create_employee(emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Check duplicate employee_id
    existing_emp = db.query(models.Employee).filter(
        (models.Employee.employee_id == emp.employee_id) |
        (models.Employee.email == emp.email)
    ).first()

    if existing_emp:
        raise HTTPException(status_code=400, detail="Employee ID or Email already exists")

    new_emp = models.Employee(**emp.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {"success": True, "message": "Employee created", "data": new_emp}


# 📋 Get All Employees
@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    return {"success": True, "data": employees}


# ❌ Delete Employee
@router.delete("/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()
    return {"success": True, "message": "Employee deleted"}

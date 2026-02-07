from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📝 Mark Attendance
@router.post("/")
def mark_attendance(att: schemas.AttendanceCreate, db: Session = Depends(get_db)):

    # Check employee exists
    emp = db.query(models.Employee).filter(models.Employee.id == att.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check duplicate attendance
    existing = db.query(models.Attendance).filter(
        models.Attendance.employee_id == att.employee_id,
        models.Attendance.date == att.date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")

    new_att = models.Attendance(**att.model_dump())
    db.add(new_att)
    db.commit()
    db.refresh(new_att)

    return {"success": True, "message": "Attendance marked", "data": new_att}


# 📊 Get Attendance of Employee
@router.get("/{employee_id}")
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    records = db.query(models.Attendance).filter(models.Attendance.employee_id == employee_id).all()
    return {"success": True, "data": records}

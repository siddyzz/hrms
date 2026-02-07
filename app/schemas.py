from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Literal

class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str

    @field_validator("employee_id", "full_name", "department")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: Literal["Present", "Absent"]

    @field_validator("status", mode="before")
    @classmethod
    def status_title(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import employees, attendance

app = FastAPI(title="HRMS Lite API")

# Allow frontend origin from env for deployment (e.g. Vercel URL)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
_cors_origin = os.getenv("CORS_ORIGIN")
if _cors_origin:
    origins.append(_cors_origin.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(employees.router)
app.include_router(attendance.router)

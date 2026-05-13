from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Ozon Job Clone API")

# Разрешаем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Модели данных ---

class Job(BaseModel):
    id: str
    title: str
    company: str
    salary_min: int
    salary_max: int
    description: str
    location: str
    type: str  # Full-time, Part-time, Remote
    created_at: datetime

class JobCreate(BaseModel):
    title: str
    company: str
    salary_min: int
    salary_max: int
    description: str
    location: str
    type: str

class Application(BaseModel):
    id: str
    job_id: str
    applicant_name: str
    applicant_contact: str
    resume_text: str
    status: str  # Pending, Reviewed, Accepted, Rejected
    applied_at: datetime

class ApplicationCreate(BaseModel):
    job_id: str
    applicant_name: str
    applicant_contact: str
    resume_text: str

# --- Имитация базы данных в памяти ---
jobs_db: List[Job] = [
    Job(
        id=str(uuid.uuid4()),
        title="Складской работник",
        company="Ozon Logistics",
        salary_min=60000,
        salary_max=90000,
        description="Сборка и упаковка товаров. Опыт не требуется.",
        location="Москва",
        type="Full-time",
        created_at=datetime.now()
    ),
    Job(
        id=str(uuid.uuid4()),
        title="Курьер",
        company="Ozon Express",
        salary_min=80000,
        salary_max=120000,
        description="Доставка заказов клиентам. Свой автомобиль или велосипед.",
        location="Санкт-Петербург",
        type="Part-time",
        created_at=datetime.now()
    ),
    Job(
        id=str(uuid.uuid4()),
        title="Python Разработчик",
        company="Tech Team",
        salary_min=150000,
        salary_max=250000,
        description="Разработка микросервисов, работа с FastAPI и PostgreSQL.",
        location="Удаленно",
        type="Remote",
        created_at=datetime.now()
    )
]

applications_db: List[Application] = []

# --- Эндпоинты ---

@app.get("/api/jobs", response_model=List[Job])
def get_jobs(location: Optional[str] = None, job_type: Optional[str] = None):
    filtered = jobs_db
    if location:
        filtered = [j for j in filtered if location.lower() in j.location.lower()]
    if job_type:
        filtered = [j for j in filtered if j.type == job_type]
    return filtered

@app.post("/api/jobs", response_model=Job)
def create_job(job: JobCreate):
    new_job = Job(
        id=str(uuid.uuid4()),
        **job.dict(),
        created_at=datetime.now()
    )
    jobs_db.append(new_job)
    return new_job

@app.get("/api/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    for job in jobs_db:
        if job.id == job_id:
            return job
    raise HTTPException(status_code=404, detail="Вакансия не найдена")

@app.post("/api/applications", response_model=Application)
def apply_to_job(application: ApplicationCreate):
    # Проверка существования вакансии
    job_exists = any(j.id == application.job_id for j in jobs_db)
    if not job_exists:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")

    new_app = Application(
        id=str(uuid.uuid4()),
        **application.dict(),
        status="Pending",
        applied_at=datetime.now()
    )
    applications_db.append(new_app)
    return new_app

@app.get("/api/applications", response_model=List[Application])
def get_applications(applicant_name: Optional[str] = None):
    # В реальном приложении здесь была бы авторизация
    filtered = applications_db
    if applicant_name:
        filtered = [a for a in filtered if applicant_name.lower() in a.applicant_name.lower()]
    return filtered

if __name__ == "__main__":
    import uvicorn
    print("Запуск сервера Ozon Job Clone на http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

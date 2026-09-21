import csv
import io

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationSummary,
    ApplicationUpdate,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Internship Application Tracker",
    description="A simple API for tracking internship applications.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Internship Application Tracker API is running"}


@app.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_application(db, application)


@app.get("/applications", response_model=list[ApplicationResponse])
def list_applications(
    status: str | None = None,
    company: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_applications(db, status, company)


@app.get("/applications/summary", response_model=ApplicationSummary)
def application_summary(db: Session = Depends(get_db)):
    return crud.get_summary(db)


@app.get("/applications/export")
def export_applications(db: Session = Depends(get_db)):
    applications = crud.get_applications(db)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "id",
            "company",
            "position",
            "location",
            "date_applied",
            "deadline",
            "status",
            "interview_stage",
            "job_url",
            "notes",
        ]
    )

    for application in applications:
        writer.writerow(
            [
                application.id,
                application.company,
                application.position,
                application.location or "",
                application.date_applied or "",
                application.deadline or "",
                application.status,
                application.interview_stage or "",
                application.job_url or "",
                application.notes or "",
            ]
        )

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; filename=internship_applications.csv"
            )
        },
    )


@app.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_one_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@app.put("/applications/{application_id}", response_model=ApplicationResponse)
def update_one_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.update_application(db, application, application_data)


@app.delete("/applications/{application_id}")
def delete_one_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = crud.get_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    crud.delete_application(db, application)
    return {"message": "Application deleted successfully"}

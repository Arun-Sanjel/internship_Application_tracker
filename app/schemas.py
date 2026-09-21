from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ApplicationBase(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    position: str = Field(min_length=1, max_length=150)
    location: str | None = Field(default=None, max_length=100)
    date_applied: date | None = None
    deadline: date | None = None
    status: str = Field(default="Applied", min_length=1, max_length=50)
    interview_stage: str | None = Field(default=None, max_length=100)
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=100)
    position: str | None = Field(default=None, min_length=1, max_length=150)
    location: str | None = Field(default=None, max_length=100)
    date_applied: date | None = None
    deadline: date | None = None
    status: str | None = Field(default=None, min_length=1, max_length=50)
    interview_stage: str | None = Field(default=None, max_length=100)
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class ApplicationResponse(ApplicationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatusTotal(BaseModel):
    status: str
    count: int


class ApplicationSummary(BaseModel):
    total_applications: int
    by_status: list[StatusTotal]

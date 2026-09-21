from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from .database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    position = Column(String(150), nullable=False)
    location = Column(String(100), nullable=True)
    date_applied = Column(Date, nullable=True)
    deadline = Column(Date, nullable=True)
    status = Column(String(50), default="Applied", nullable=False)
    interview_stage = Column(String(100), nullable=True)
    job_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

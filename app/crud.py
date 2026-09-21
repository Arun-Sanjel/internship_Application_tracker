from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Application
from .schemas import ApplicationCreate, ApplicationUpdate


def create_application(
    db: Session,
    application_data: ApplicationCreate,
) -> Application:
    application = Application(**application_data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def get_applications(
    db: Session,
    status: str | None = None,
    company: str | None = None,
) -> list[Application]:
    statement = select(Application).order_by(Application.created_at.desc())

    if status:
        statement = statement.where(Application.status == status)

    if company:
        statement = statement.where(Application.company == company)

    return list(db.scalars(statement).all())


def get_application(db: Session, application_id: int) -> Application | None:
    return db.get(Application, application_id)


def update_application(
    db: Session,
    application: Application,
    application_data: ApplicationUpdate,
) -> Application:
    changes = application_data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: Application) -> None:
    db.delete(application)
    db.commit()


def get_summary(db: Session) -> dict:
    count = db.scalar(select(func.count(Application.id)))

    status_rows = db.execute(
        select(Application.status, func.count(Application.id))
        .group_by(Application.status)
        .order_by(func.count(Application.id).desc())
    ).all()

    return {
        "total_applications": int(count or 0),
        "by_status": [
            {"status": status, "count": int(total)}
            for status, total in status_rows
        ],
    }

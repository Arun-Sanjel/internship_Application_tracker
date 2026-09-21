# Internship Application Tracker

A simple internship application tracker built with Python, FastAPI, SQLAlchemy, and SQLite.

## What it does

- Add an internship application
- View all applications
- View one application
- Update an application
- Delete an application
- Filter applications by status or company
- Track deadlines and interview stages
- View application counts by status
- Export applications as a CSV file

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

## Run locally

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Arun-Sanjel/internship_Application_tracker.git
cd internship_Application_tracker
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

```
http://127.0.0.1:8000/docs
```

## Example application

```json
{
  "company": "Example Company",
  "position": "Software Engineering Intern",
  "location": "Dallas, TX",
  "date_applied": "2026-09-21",
  "deadline": "2026-10-15",
  "status": "Applied",
  "interview_stage": null,
  "job_url": "https://example.com/jobs/123",
  "notes": "Applied through company website"
}
```

## Run tests

```bash
pytest
```

The SQLite database file is created automatically when the application starts.

# Professional-Progress-Tracker

## Steps to run program:

Create Virtual Environment

    Mac:
    python3 -m venv venv
    source venv/bin/activate

    Windows:
    python -m venv venv
    .\venv\Scripts\activate

Install Dependencies

    pip install -r requirements.txt

Run

    python -m src.main

## New: Docker SetupAdd commentMore actions

    docker-compose up --build

Add to .env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/progress_tracker_db - need to create a database on pgadmin call progress_tracker_db
SECRET_KEY=your_secret_key_here
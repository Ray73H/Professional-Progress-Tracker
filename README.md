# Professional-Progress-Tracker

## Run with docker:

Create a new database in pgAdmin. Add these to your .env file

    DB_USER=<postgres_user_name>
    DB_PASSWORD=<postgres_password>
    DB_HOST=host.docker.internal
    DB_PORT=5432
    DB_NAME=<postgres_database_name>

Run

    docker-compose up --build

## Run program locally:

Create Virtual Environment

    Mac:
    python3 -m venv venv
    source venv/bin/activate

    Windows:
    python -m venv venv
    .\venv\Scripts\activate

Install Dependencies

    pip install -r requirements.txt

Create a new database in pgAdmin. Add these to you .env file

    DB_USER=<postgres_user_name>
    DB_PASSWORD=<postgres_password>
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=<postgres_database_name>

Run

    python -m src.main

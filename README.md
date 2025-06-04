# Professional-Progress-Tracker

## Run with docker:

Create a new database in pgAdmin. Add these to your .env file

    DB_USER=<postgres_user_name>
    DB_PASSWORD=<postgres_password>
    DB_HOST=host.docker.internal
    DB_PORT=<postgres_port>
    DB_NAME=<postgres_database_name>

Run

    docker-compose up --build

There will be example data loaded into the system automatically under two accounts:

    Account 1:
        Username: demo
        Password: password
    Account 2:
        Username: demo2
        Password: 1234

## Information about the system
 
- User's have jobs. Within the jobs there are projects. Within the projects there are tasks
- You can add jobs, projects, and tasks
- You can access the job/project by clicking on the title of job/project in the list
- There is a search bar to search for tasks (regular expression pattern in views.py line 115)

### (Second option to run locally):

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

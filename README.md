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

## API Endpoints

### Jobs

-   `GET /api/jobs` - Get all jobs for current user
-   `POST /api/jobs` - Create new job
    ```json
    {
    	"name": "Job Title",
    	"description": "Job Description",
    	"position": "Job Position"
    }
    ```
-   `PUT /api/jobs/<id>` - Update job
-   `DELETE /api/jobs/<id>` - Delete job

### Projects

-   `GET /api/jobs/<job_id>/projects` - Get all projects for a job
-   `POST /api/jobs/<job_id>/projects` - Create new project
    ```json
    {
    	"name": "Project Name",
    	"description": "Project Description"
    }
    ```
-   `PUT /api/projects/<id>` - Update project
-   `DELETE /api/projects/<id>` - Delete project

### Tasks

-   `GET /api/tasks` - Get all tasks (optional query params: job_id, project_id)
-   `POST /api/tasks` - Create new task
    ```json
    {
    	"name": "Task Name",
    	"description": "Task Description",
    	"status": "pending",
    	"due_date": "2024-05-01T12:00:00",
    	"job_id": 1, // Optional if project_id is provided
    	"project_id": 1 // Optional if job_id is provided
    }
    ```
-   `PUT /api/tasks/<id>` - Update task
-   `DELETE /api/tasks/<id>` - Delete task

Note: All endpoints require authentication from the login system.

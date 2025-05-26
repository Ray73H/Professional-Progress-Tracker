from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)

dummy_job = {
        "id": 1,
        "title": "Software Development Job at Tech Solutions Inc."
    }

dummy_projects = [
        {
            "id": 101,
            "title": "Project Alpha",
            "description": "Develop the core authentication module."
        },
        {
            "id": 102,
            "title": "Project Beta",
            "description": "Integrate third-party payment gateway."
        },
        {
            "id": 103,
            "title": "Project Gamma",
            "description": "Design and implement the new UI/UX."
        }
    ]

dummy_tasks = [
        {
            "id": 201,
            "title": "Task: User registration feature",
            "description": "Completed user sign-up and login forms."
        },
        {
            "id": 202,
            "title": "Accomplishment: Optimized database queries",
            "description": "Reduced query time by 30% for key operations."
        },
        {
            "id": 203,
            "title": "Task: API documentation",
            "description": "Wrote comprehensive docs for all public API endpoints."
        }
    ]

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/job', methods=['GET','POST'])
def jobs():
    if request.method == 'POST':
        pass
    return render_template("job.html", job=dummy_job, projects=dummy_projects, tasks=dummy_tasks)

@views.route('/add_project/<int:job_id>', methods=['POST'])
def add_project(job_id):
    return redirect(url_for('views.jobs'))

@views.route('/add_task', methods=['POST'])
def add_task():
    job_id = request.args.get("job_id")
    project_id = request.args.get("project_id")
    if project_id:
        return redirect(url_for('views.view_project'))
    return redirect(url_for('views.jobs'))

@views.route('/project/<int:project_id>')
def view_project(project_id):
    project = next((p for p in dummy_projects if p["id"] == project_id), None)

    if project is None:
        return redirect(url_for('views.home'))
    
    return render_template("project.html", project=project, tasks=dummy_tasks)

@views.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    return redirect(url_for('views.jobs'))

@views.route('/delete_project/<int:project_id>', methods=['GET'])
def delete_project(project_id):
    return redirect(url_for('views.jobs'))

@views.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    return redirect(url_for('views.jobs'))

@views.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    return redirect(url_for('views.jobs'))
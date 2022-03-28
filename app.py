from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    description = db.Column(db.String(length=50))
    project = db.relationship("Project")



#ruta / (root o home)
@app.route("/")
#funcion que renderea el archivo html 
def show_projects():
	return render_template("index.html", projects=Project.query.all())

#generamos una nueva ruta /project/<project_id> que cargara diferentes proyectos
@app.route("/project/<project_id>")
def show_tasks(project_id):
	return render_template("project-tasks.html", project_id=project_id)

#ruta para añadir proyectos
@app.route("/add/project", methods=['POST'])
def add_project():
	#Add project
	return "Project added sucessfully"
#ruta tu ya sabes pa que
@app.route("/add/task/<project_id>", methods=['POST'])
def add_task(project_id):
	#Add task
	return "Task added successfully"

#correr la app en el localhost puerto 3000 (127.0.0.1:3000)
app.run(debug=True, host="127.0.0.1", port=3000)
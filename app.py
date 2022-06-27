from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#crear un secret para mantener las escrituras a la db seguras
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))
	#es un vinculo con la tabla task
    task = db.relationship("Task", cascade="all, delete-orphan")

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    description = db.Column(db.String(length=50))
    #es un vinculo con la tabla project
    project = db.relationship("Project", backref="project")



#ruta / (root o home)
@app.route("/")
#funcion que renderea el archivo html 
def show_projects():
	return render_template("index.html", projects=Project.query.all())

#generamos una nueva ruta /project/<project_id> que cargara diferentes proyectos
@app.route("/project/<project_id>")
def show_tasks(project_id):
	return render_template("project-tasks.html", 
		project=Project.query.filter_by(project_id=project_id).first(),
		tasks=Task.query.filter_by(project_id=project_id).all())
#ruta para añadir proyectos
@app.route("/add/project", methods=['POST'])
def add_project():
    #el nombre del formulario que revisamos tiene que coincidir con el del template
	if not request.form['project-title']:
        #mandamos alerta en caso que no tenga nada
		flash("Enter a title for your new project", "red")
	else:
        #creamos un nuevo projecto y lo insertamos en la tabla 
		project = Project(title=request.form['project-title'])
		db.session.add(project)
		db.session.commit()
		flash("Project added successfully", "green")
	return redirect(url_for('show_projects'))

#ruta tu ya sabes pa que
@app.route("/add/task/<project_id>", methods=['POST'])
def add_task(project_id):
	#Añade el codigo para insertar un  task en la db
	if not request.form['task-description']:
		flash("Enter a description for your new task", "red")
	else:
		task = Task(description=request.form['task-description'], project_id=project_id)
		db.session.add(task)
		db.session.commit()
		flash("Task added successfully", "green")
	return redirect(url_for('show_tasks', project_id=project_id))


@app.route("/delete/task/<task_id>", methods=['POST'])
def delete_task(task_id):
	#seleccionamos la task a borrar
	pending_delete_task = Task.query.filter_by(task_id=task_id).first()
	#obtenemos el proyecto al que pertenece la task y lo guardamos en original_project_id
	original_project_id = pending_delete_task.project.project_id
	#hacemos el borrado en la db 
	db.session.delete(pending_delete_task)
	db.session.commit()
	#nos vamos a show_task, la misma url donde estamos (y como necesita el project_id le mandamos original_project_id )
	return redirect(url_for('show_tasks', project_id=original_project_id))

@app.route("/delete/project/<project_id>", methods=['POST'])
def delete_project(project_id):
	pending_delete_project = Project.query.filter_by(project_id=project_id).first()
	db.session.delete(pending_delete_project)
	db.session.commit()
	return redirect(url_for('show_projects'))

	
#correr la app en el localhost puerto 3000 (127.0.0.1:3000)
app.run(debug=True, host="127.0.0.1", port=3000)
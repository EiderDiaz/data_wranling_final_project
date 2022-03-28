from flask import Flask, render_template

app = Flask(__name__)
#ruta / (root o home)
@app.route("/")

#funcion que renderea el archivo html 
def show_projects():
	return render_template("index.html")

#generamos una nueva ruta /project/<project_id> que cargara diferentes proyectos
@app.route("/project/<project_id>")
def show_tasks(project_id):
	return render_template("project-tasks.html", project_id=project_id)



#correr la app en el localhost puerto 3000 (127.0.0.1:3000)
app.run(debug=True, host="127.0.0.1", port=3000)
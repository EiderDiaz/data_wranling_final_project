from flask import Flask, render_template

app = Flask(__name__)
#ruta / (root o home)
@app.route("/")

#funcion que renderea el archivo html 
def show_projects():
	return render_template("index.html")

#correr la app en el localhost puerto 3000 (127.0.0.1:3000)
app.run(debug=True, host="127.0.0.1", port=3000)
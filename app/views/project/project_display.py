from app import app
from flask import abort,render_template
from app.model import project

@app.route("/project/<language>/<category>")
def project_display(language,category):
    pj = project.projects(language,category)
    if pj.isNone():
        abort(404)
    return render_template("project_display.html",project = pj)
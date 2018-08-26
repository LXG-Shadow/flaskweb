from app import app
from flask import redirect

@app.route("/show_project/javascript/<project_name>")
def project_javascript_redirect(project_name):
    return redirect("/static/projects/javascript/%s/index.html" % project_name)

@app.route("/show_project/python/<project_name>")
def project_python_redirect(project_name):
    return redirect("/projects/python/%s" % project_name)
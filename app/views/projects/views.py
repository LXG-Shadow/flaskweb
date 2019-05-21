from . import projects
from flask import abort,render_template,redirect
from app.model.projects import projects as projects_model
from app.decorator import get_user

@projects.route("/<language>/<category>")
@get_user
def projects_display(*args,**kwargs):
    pj = projects_model(kwargs.pop("language"),kwargs.pop("category"))
    if pj.isNone():
        abort(404)
    return render_template("/projects/projects_display.html",project = pj,**kwargs)

@projects.route("/redirect/<type>/<language>/<project_name>")
@get_user
def projects_redirect(*args,**kwargs):
    type, language, project_name = kwargs.pop("type"),kwargs.pop("language"),kwargs.pop("project_name")
    if type == "0":
        return redirect("/static/projects/%s/%s/index.html" % (language,project_name))
    elif type == "1":
        return redirect("/projects/dynamic/%s/%s" % (language,project_name))
    else:
        abort(404)

@projects.route("/dynamic/<language>/<project_name>")
@get_user
def dynamic_project_display(*args,**kwargs):
    language, project_name = kwargs.pop("language"), kwargs.pop("project_name")
    try:
        return render_template("projects/%s/%s.html" %(language,project_name),**kwargs)
    except:
        abort(404)



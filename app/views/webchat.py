from app.views import *

@app.route("/webchat")
def webchat():
    webcss = url_for("static", filename="style.css")
    if ("username" in request.cookies) and ("password" in request.cookies):
        resp = make_response(render_template("webchat.html",
                                             webcss=webcss,
                                             webtitle="CHATLOL", stats = "1",
                                             username = request.cookies.get("username")))
    else:
        resp = make_response(render_template("webchat.html",
                                             webcss=webcss,
                                             webtitle="CHATLOL",stats = "0"))
    return resp

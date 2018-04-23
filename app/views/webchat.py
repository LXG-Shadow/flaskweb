from app.views import *
from app.api import login
import datetime

@app.route("/webchat")
def webchat():
    webcss = url_for("static", filename="style.css")
    if ("username" in request.cookies) and ("password" in request.cookies):
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        dbdata = login.logindb(username,password)
        if dbdata["code"] == "1":
            resp = app.make_response(render_template("webchat.html",
                                                     webcss=webcss,
                                                     webtitle="CHATLOL", stats="1",
                                                     username=request.cookies.get("username")))
            #延长cookie时间
            expiredtime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            resp.set_cookie("username", username, expires=expiredtime)
            resp.set_cookie("password", password, expires=expiredtime)
        else:
            resp = app.make_response(render_template("webchat.html",
                                                     webcss=webcss,
                                                     webtitle="CHATLOL", stats="0"))
    else:
        resp = app.make_response(render_template("webchat.html",
                                             webcss=webcss,
                                             webtitle="CHATLOL",stats = "0"))
    return resp

from app.views import *
from app.api import login,database
import datetime


@app.route("/webchat/", methods = ["GET","POST"])
def webchat():
    webcss = url_for("static", filename="style.css")
    #是否登陆过
    if ("username" in request.cookies) and ("password" in request.cookies):
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        dbdata = login.logindb(username,password)
        #cookie内用户密码是否正确
        if dbdata["code"] == "1":
            try:
                # 获取用户id
                dbdata = database.get_user_id_by_name(username)
                # 获取用户信息
                dbdata = database.get_user_info(dbdata["data"]["user_id"])
                # 获取用户组
                user_group = str(dbdata["data"]["user_group"])
                resp = app.make_response(render_template("webchat.html",
                                                         webcss=webcss,
                                                         webtitle="CHATLOL", stats=user_group,
                                                         username=request.cookies.get("username")))
            except:
                # 等待更改成wrongpage
                resp = app.make_response(render_template("webchat.html",
                                                         webcss=webcss,
                                                         webtitle="CHATLOL", stats="0",
                                                         username=request.cookies.get("username")))
            # 延长cookie时间
            expiredtime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            resp.set_cookie("username", username, expires=expiredtime)
            resp.set_cookie("password", password, expires=expiredtime)
        # 不正确返回游客界面
        else:
            resp = app.make_response(render_template("webchat.html",
                                                     webcss=webcss,
                                                     webtitle="CHATLOL", stats="0"))
    # 返回游客界面
    else:
        resp = app.make_response(render_template("webchat.html",
                                             webcss=webcss,
                                             webtitle="CHATLOL",stats = "0"))
    return resp

from flask import request,current_app,redirect,flash
from app.api import *
from app.model import user
from app.decorator import get_user,login_auth_api
import datetime

#@api.route("/auth/login",methods=["GET","POST"])
def login_api(**kwargs):
    # 获取参数
    username = request.values.get("username")
    password = request.values.get("password")
    # 判断参数是否为空
    if bool(username is None or password is None) \
            or (len(username) < 4 or len(username) > 16) or (len(password) < 6 or len(password) > 16):
        return newjson("-1")
    usr = user.initFromName(username)
    if (usr.is_anonymous() or not usr.is_authenticate(password)):
        flash("登陆失败")
        return newjson("8")

    resp = current_app.make_response(newjson("9"))
    expiredtime = datetime.datetime.utcnow()
    expiredtime = expiredtime + datetime.timedelta(days=1)
    resp.set_cookie("auth", usr.getAuthString(password), expires=expiredtime)
    return resp


#@api.route("/auth/logout", methods=["GET","POST"])
#@login_auth_api
def logout_api(**kwargs):
    resp = current_app.make_response(redirect("/"))
    resp.delete_cookie("auth")
    return resp
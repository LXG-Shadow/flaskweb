from flask import render_template, redirect,current_app,flash
from app import codesmap,newjson
from . import auth
from .forms import LoginForm
from ...decorator import get_user,login_auth_view,get_siteInfo
from ...model import user
import datetime

@auth.route('/login',endpoint="login" ,methods=['GET'])
@get_user
@get_siteInfo("登陆-Login")
def login(*args,**kwargs):
    if not kwargs["user"].is_anonymous():
        return redirect("/")
    return render_template("/auth/login.html",form = LoginForm(),**kwargs)

@auth.route('/login',endpoint="login-verify",methods=['POST'])
@get_user
def login_verify(*args,**kwargs):
    if not kwargs["user"].is_anonymous():
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user0 = user.initFromName(username)
        if (user0.is_anonymous() or not user0.is_authenticate(password)):
            return render_template("/auth/login.html",form=form,message=("warning",codesmap["8"]),**kwargs)
        resp = current_app.make_response(redirect("/"))
        expiredtime = datetime.datetime.utcnow()
        expiredtime = expiredtime + datetime.timedelta(days=1)
        resp.set_cookie("auth", user0.getAuthString(password), expires=expiredtime)
        return resp
    else:
        return render_template("/auth/login.html", form=form,message=("danger",codesmap["-1"]), **kwargs)


@auth.route("/auth/logout",endpoint="logout", methods=["GET","POST"])
@login_auth_view
@get_siteInfo("登出")
def logout(**kwargs):
    resp = current_app.make_response(redirect("/"))
    resp.delete_cookie("auth")
    return resp
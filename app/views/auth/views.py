from flask import render_template, redirect,current_app,flash
from flask_babel import lazy_gettext as _l
from app import codesmap,newjson
from . import auth
from .forms import LoginForm
from ...decorator import get_user,login_auth_view,get_siteInfo
from ...model import user
import datetime

@auth.route('/login',endpoint="login" ,methods=['GET'])
@get_user
@get_siteInfo(_l("Login"))
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
        if (user0.is_anonymous() or not user0.checkPassword(password)):
            return render_template("/auth/login.html",form=form,message=("warning",codesmap["8"]),**kwargs)
        resp = current_app.make_response(redirect("/"))
        resp.set_cookie("_auth", user0.getAuthString())
        return resp
    else:
        return render_template("/auth/login.html", form=form,message=("danger",codesmap["-1"]), **kwargs)


@auth.route("/auth/logout",endpoint="logout", methods=["GET","POST"])
@login_auth_view
@get_siteInfo(_l("Logout"))
def logout(**kwargs):
    resp = current_app.make_response(redirect("/"))
    resp.delete_cookie("_auth")
    return resp
from . import main
from flask import render_template,flash,redirect,url_for,current_app
from app.model import errorpage,user
from app.decorator import get_user,get_siteInfo
from flask_babel import Babel,gettext as _
import jinja2.ext

@main.route("/",endpoint="index",methods=["GET","POST"])
@get_siteInfo("LXG_Shadow")
@get_user
def index(**kwargs):
    #print(user.register("admin","admin123","admin@lxgshadow.us"))
    #print(user.register("user1","123456","user1@lxgshadow.us"))
    #print(user.register("woshicab", "123456789", "cab@nmsl.com"))
    return render_template("index.html",**kwargs)

@main.route("/intro",endpoint="intro",methods=["GET","POST"])
@get_siteInfo("Intro")
@get_user
def index(**kwargs):
    return render_template("intro.html",**kwargs)

@main.app_errorhandler(404)
@get_user
def error_404(*args,**kwargs):
    return render_template('errorpage.html',errorpage = errorpage(404),**kwargs), 404

@main.app_errorhandler(500)
@get_user
def error_500(*args,**kwargs):
    return render_template('errorpage.html',errorpage = errorpage(500),**kwargs), 500

@main.app_errorhandler(405)
def error_500(*args,**kwargs):
    return render_template('errorpage.html',errorpage = errorpage(405),**kwargs), 405

@main.app_errorhandler(401)
def error_401(*args,**kwargs):
    return render_template('errorpage.html',errorpage = errorpage(401),**kwargs), 401

@main.app_errorhandler(403)
def error_403(*args,**kwargs):
    return render_template('errorpage.html',errorpage = errorpage(403),**kwargs), 403
from flask import render_template,url_for,make_response,request
from app import app



@app.route('/')
def index():
    webcss = url_for("static", filename="style.css")
    return render_template("index.html",webcss=webcss,webtitle ="LXG_Shadow's Website")

@app.route('/hello/<name>')
def hello(name):
    return "FKu %s" % name

from app.views import biligetfav
from app.views import webchat
from app.views import webchatadmin
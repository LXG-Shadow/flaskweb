from app import app
from flask import render_template
from app.model import errorpage

@app.errorhandler(404)
def error_404(e):
    return render_template('errorpage.html',errorpage = errorpage.errorpage(404)), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('errorpage.html',errorpage = errorpage.errorpage(500)), 500

@app.errorhandler(405)
def error_500(e):
    return render_template('errorpage.html',errorpage = errorpage.errorpage(405)), 405
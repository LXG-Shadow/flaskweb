from app import app
from flask import render_template

@app.route('/projects/python/favfolder', methods=['GET', 'POST'])
def bilibilitools_favfolder():
    return render_template('projects/bilibilitools/favfolder.html')
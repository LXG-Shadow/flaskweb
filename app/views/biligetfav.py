from app.views import *

@app.route("/myapp/bilifav", methods=["GET","POST"])
def bilifav() :
    webcss = url_for("static", filename="style.css")
    from app.myapp import BiliFavGet
    favlink = ""
    number = ""
    linkform = BiliFavGet.linkform()
    if linkform.validate_on_submit():
        favlink = linkform.favlink.data
        number = linkform.number.data
        linkform.favlink.data = ""
        linkform.number.data = ""
        avsc = BiliFavGet.outputdata(favlink,number)
        return render_template("bilifavget.html", webcss=webcss, webtitle="B站收藏夹获取器",
                               linkform=linkform, avsc=avsc)
    return render_template("bilifavget.html",webcss = webcss,webtitle = "B站收藏夹获取器",
                           linkform = linkform)
from flask import request,render_template
from app.api import *
from app.model.projects.quizlet import quizlet_words


@api.route("/quizlet/quizlet_words",methods=["GET","POST"])
def quizlet_quizlet_words_api():
    # 获取参数
    xxjlink = request.values.get("xxjlink")

    # 判断参数是否为空
    if xxjlink is None:
        return newjson("-1")

    words = quizlet_words.initFromLink(xxjlink)

    if (not words.isValid()):
        return newjson("2",data={"alert":render_template("component/alert.html",message=("warning",codesmap["2"]))})

    if words.isNone():
        return newjson("17",data={"alert":render_template("component/alert.html",message=("warning",codesmap["17"]))})

    return newjson("1",data={"alert":render_template("component/alert.html",message=("success",codesmap["1"])),"words":words.getData(ps=3000)})
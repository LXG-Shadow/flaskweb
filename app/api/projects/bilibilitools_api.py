from flask import request
from app.api import *
from app.model.projects.bilibilitools import favfolder


@api.route("/bilibilitools/favfolder", methods=["GET", "POST"])
def bilibilitools_favfolder_api():
    # 获取参数
    favlink = request.values.get("favlink")

    # 判断参数是否为空
    if favlink == None:
        return newjson("-1")

    fav = favfolder.initFromLink(favlink)

    if (not fav.isValid()):
        return newjson("2")

    if fav.isNone():
        return newjson("3")

    return newjson("1", data=fav.getData())

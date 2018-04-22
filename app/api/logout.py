from app.api import *

@app.route("/api/logout/", methods=["POST"])
def logout():
    # 判断提交方式是不是post
    if request.method == "POST":
        if ("username" in request.cookies) and ("password" in request.cookies):
            resp = app.make_response(newjson("9"))
            resp.delete_cookie("username")
            resp.delete_cookie("password")
            return resp
        else:
            #没有登陆则返回还未登陆的code
            return newjson("10")
    # 如果不是则返回错误
    else:
        return newjson("-2")
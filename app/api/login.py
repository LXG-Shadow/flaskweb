from app.api import *

@app.route("/api/login/",methods=["GET","POST"])
def login():
    #判断提交方式是不是post
    if request.method == "POST":
        #判断内容是不是application/json
        if bool(request.json):
            try:
                username = request.json["username"]
                password = request.json["password"]
                dbdata = logindb(username, password)
            except:
                return newjson("-1")
        #不是的话使用尝试使用form
        else:
            try:
                username = request.form.get("username")
                password = request.form.get("password")
                dbdata = logindb(username, password)
            except:
                return newjson("-1")
        #判断是否登陆成功
        if dbdata["code"] == "1":
            resp = app.make_response(newjson(dbdata["code"]))
            #设置cookie
            expiredtime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            resp.set_cookie("username", username, expires=expiredtime)
            resp.set_cookie("password", password, expires=expiredtime )
            return resp
        #登陆失败则返回信息
        else:
            return newjson(dbdata["code"])
    #如果不是则返回错误
    else:
        return newjson("-2")


def logindb(username,password):
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        # 查询用户名对应的密码
        cursor.execute('select password from usertable where username=%s',[username])
        # 获取所有的id
        values = cursor.fetchone()
        #查看密码是否为空
        if values != None:
            #判断密码是否一致
            if values[0] == password:
                #返回登陆成功的code
                return {"code":"1"}
            else:
                #返回密码错误的code
                return {"code":"3"}
        else:
            # 是则返回 没有该用户的code
            return {"code":"2"}
    except:
        return {"code":"-3"}

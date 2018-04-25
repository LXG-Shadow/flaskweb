from app.api import *

@app.route("/api/msg/send/", methods=["POST"])
def sendmsg():
    # 判断提交方式是不是post
    if request.method == "POST":
        if ("username" in request.cookies) and ("password" in request.cookies):
            username = request.cookies.get("username")
            password = request.cookies.get("password")
            dbdata = login.logindb(username, password)
            #密码正确则进行下一步
            if dbdata["code"] == "1":
                dbdata = database.get_user_id_by_name(username)
                user_id = dbdata["data"]["user_id"]
                # 判断内容是不是application/json
                if bool(request.json):
                    try:
                        message = request.json["message2send"]
                    except:
                        return newjson("-1")
                # 不是的话使用尝试使用form
                else:
                    try:
                        message = request.form.get("message2send")
                    except:
                        return newjson("-1")
                #判断message是否为空
                if len(message) < 1:
                    return newjson("12")
                #获取返回值
                dbdata = sendmsgdb(user_id, message)
                return newjson(dbdata["code"])
            #密码错误则返回错误信息
            else:
                return newjson('-5')
        # 未登陆则返回未登录信息
        else:
            return newjson('-4')
    else:
        return newjson('-2')


def sendmsgdb(user_id,message):
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        #获取最后一条消息的id
        cursor.execute("select msgid from messages order by msgid desc limit 1")
        newmsgid = int(cursor.fetchone()[0]) + 1
        # 插入新行
        cursor.execute('insert into messages values (%s, %s, %s)', [newmsgid, user_id, message])
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return {"code":"13"}
    except:
        return {"code":"-3"}
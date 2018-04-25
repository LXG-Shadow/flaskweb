from app.api import *

@app.route("/api/msg/clear/", methods = ["GET","POST"])
def clearmsg():
    if ("username" in request.cookies) and ("password" in request.cookies):
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        dbdata = login.logindb(username, password)
        # 密码正确则进行下一步
        if dbdata["code"] == "1":
            #查询该用户id
            dbdata = database.get_user_id_by_name(username)
            user_id = dbdata["data"]["user_id"]
            #查询该用户信息
            dbdata = database.get_user_info(user_id)
            #如果获取成功
            if dbdata["code"] == "8":
                #获取用户组
                user_group = str(dbdata["data"]["user_group"])
                #如果是管理员
                if user_group == "3":
                    #进行清除操作并返回信息
                    dbdata = clearmsgdb()
                    #如果操作成功
                    if dbdata["code"] == "10":
                        return newjson(dbdata["code"],data=dbdata["data"])
                    else:
                        #失败则返回错误code
                        return newjson(dbdata["code"])
                else:
                    #不是返回越权操作
                    return newjson('-6')
            else:
                #获取失败返回值
                return newjson(dbdata["code"])
        else:
            # 密码错误则返回错误信息
            return newjson('-5')
    # 为登陆则返回未登录信息
    else:
        return newjson('-4')

def clearmsgdb():
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        #获取最后一条消息的id
        cursor.execute("select msgid from messages order by msgid desc limit 1")
        totaldel = str(cursor.fetchone()[0])
        #删除所有数据
        cursor.execute("truncate messages")
        # 插入初始化信息
        cursor.execute('insert into messages values (%s, %s, %s)', [1, "0001", "SERVER OPEN"])
        #提交
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return {"code":"10","data":{"totaldel":totaldel}}
    except:
        return {"code":"-3"}
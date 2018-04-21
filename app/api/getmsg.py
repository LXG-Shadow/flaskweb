from app.api import *

@app.route("/api/getmsg/<msgid>", methods = ["GET"])
def getmsg(msgid):
    msgid = str(msgid)
    if msgid.isdigit():
        if int(msgid) > 0:
            dbdata = getmsgdb(start=int(msgid))
            return newjson(dbdata["code"],data = dbdata["data"])
        elif int(msgid) == 0:
            dbdata = getmsgdb()
            return newjson(dbdata["code"], data=dbdata["data"])
        else:
            return newjson("-1")
    else:
        return newjson("-1")


def getmsgdb(start=None):
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        # 是否传入了数据
        #是则查询之后的数据
        if start != None:
            # 查询在msgid之后的信息
            cursor.execute("select user_id,message from messages where msgid>%s", [start])
            msglist = list(cursor.fetchall())
        else:
            # 查询倒数10条数据
            cursor.execute("select user_id,message from messages order by msgid desc limit 10")
            msglist = list(cursor.fetchall())
            msglist.reverse()
        #将[(用户id,消息)]的格式转为[{'message': 消息, 'user_id': 用户id}]
        msglist = list(map(lambda x: dict(zip(["user_id", "message"], x)), msglist))
        for ndict in msglist:
            #获取用户信息
            dbdata = database.get_user_info(ndict["user_id"])
            #添加键值,username
            ndict["username"] = dbdata["data"]["username"]
            #添加兼职,user_group
            ndict["user_group"] = dbdata["data"]["user_group"]
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return {"code":"6","data":{"msgcount":str(len(msglist)),"msg":msglist}}
    except:
        return {"code":"-3"}
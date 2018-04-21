from app.api import *

@app.route("/api/register/",methods=["GET","POST"])
def register():
    if request.method == "POST":
        if bool(request.json):
            try:
                username = request.json["username"]
                password = request.json["password"]
                dbdata = registerdb(username, password)
                if "id" in dbdata:
                    return newjson(dbdata["code"],data=jsonify({"id":dbdata["id"]}))
                else:
                    return newjson(dbdata["code"])
            except:
                return newjson("-1")
        else:
            try:
                username = request.form.get("username")
                password = request.form.get("password")
                dbdata = registerdb(username, password)
                if "id" in dbdata:
                    return newjson(dbdata["code"],data={"id":dbdata["id"]})
                else:
                    return newjson(dbdata["code"])
            except:
                return newjson("-1")
    else:
        return render_template("register.html", webtitle="Register", webcss=url_for("static", filename="style.css"))

def registerdb(username,password):
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        # 查询用户名对应的id
        cursor.execute('select user_id from usertable where username=%s', [username])
        #获取id
        values = cursor.fetchone()
        #如果存在id 说明用户名被注册
        #如果不存在，则向数据库添加一个用户
        if values == None:
            # 查询id列
            cursor.execute('select user_id from usertable')
            # 获取所有的id
            values = cursor.fetchall()
            # 获取最大那那个值，+1并转换为字符串
            id = str(max(map(lambda x: int(list(x)[0]), values)) + 1)
            # 格式化id 如 '3' ==> '0003'
            id = "0" * (4 - len(id)) + id
            # 插入新行
            cursor.execute('insert into usertable values (%s, %s, %s, %s)', [id, username, password, 0])
            # 提交
            conn.commit()
            # 关闭游标
            cursor.close()
            # 关闭连接
            conn.close()
            return {"code":"4","id":id}
        else:
            return {"code":"5"}
    except:
        return {"code":"-3"}
from app.api import *

def get_user_info(id):
    # 开启链接
    conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
    # 定义游标
    cursor = conn.cursor()
    # 查询id对应的用户名
    cursor.execute('select username from usertable where user_id=%s', [id])
    values = cursor.fetchone()
    if values != None:
        username = values[0]
        #查询所在的用户组
        cursor.execute("select user_group from usertable where user_id=%s", [id])
        values = cursor.fetchone()
        group = values[0]
        return {"code":"8","data":{"username":username,"user_group":group}}
    else:
        return {"code":"7"}

def get_user_id_by_name(username):
    # 开启链接
    conn = mysql.connector.connect(user='root', password='root', database='chatlol', use_unicode=True)
    # 定义游标
    cursor = conn.cursor()
    # 查询用户名对应的id
    cursor.execute('select user_id from usertable where username=%s', [username])
    values = cursor.fetchone()
    if values != None:
        return {"code": "14", "data": {"user_id": values[0]}}
    else:
        return {"code": "7"}
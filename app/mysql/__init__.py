import mysql.connector
from .. import db

def getData(table,*column,**where):
    try:
        # 开启链接
        conn = mysql.connector.connect(user='root', password='root', database='website', use_unicode=True)
        # 定义游标
        cursor = conn.cursor()
        columns, wheres = "*", "1=1"
        if len(column) > 0:
            columns = ",".join(column)

        sql = "select %s from %s where %s" % (columns, table, "%s")

        if len(where) > 0:
            sql = sql % (" and ".join(map(lambda x: "%s=%%s" % x, where.keys())))
            wheres = tuple(where.values())

        cursor.execute(sql, wheres)

        data = cursor.fetchall()

        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return data
    except:
        return []


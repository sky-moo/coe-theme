import scopeCommon as sc
import pymysql

# sc.getScopeOther("html-derivative")

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="123456",
                             charset="utf8mb4",
                             database="langrage_scope",
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    valueList = sc.getValueListOther("html-derivative", "html")
    with connection.cursor() as cursor:
        sql = "insert ignore into minimum(lang,scope) values(%s,%s)"
        cursor.executemany(sql, valueList)
    connection.commit()

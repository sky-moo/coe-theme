import scopeCommon as sc
import pymysql

languageList = ["html", "css", "js", "py", "c", "cpp", "json", "md", "java", "xml"]
connection = pymysql.connect(host="localhost",
                             user="root",
                             password="123456",
                             charset="utf8mb4",
                             database="langrage_scope",
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    valueList = sc.getValueList(languageList)
    for i in range(len(valueList)):
        with connection.cursor() as cursor:
            sql = "insert ignore into minimum(lang,scope) values(%s,%s)"
            cursor.executemany(sql, valueList[i])
    connection.commit()

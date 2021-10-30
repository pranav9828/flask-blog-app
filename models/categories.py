from flask import Flask,json
from pymysql import cursors
import db

app = Flask(__name__)

class Categories:
    def getCategories(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories ORDER BY category_name asc")
            categories = cursor.fetchall()
            categories = list(categories)
            categories_list = []
            for category in categories:
                res = {}
                res.update({"id": category[0], "name": category[1]})
                categories_list.append(res)
            return categories_list
        except Exception as e:
            return {"error": json.dumps(e)}
        finally:
            conn.close()
            cursor.close()
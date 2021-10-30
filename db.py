from flask import Flask
from flaskext.mysql import MySQL

secret_key = '68c4e4554bf7cf3c9075eac69444c29e'
def configureDatabase():
    app = Flask(__name__)
    mysql = MySQL()

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'blog'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_PORT	'] = '5000'
    app.config['SECRET_KEY']= secret_key

    mysql.init_app(app)
    return mysql





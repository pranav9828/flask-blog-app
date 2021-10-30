from flask import json, Flask
import datetime
import db
from werkzeug.security import generate_password_hash
import jwt
import random

app = Flask(__name__)

class Users:
    def __init__(self, userid, name, username, email, password, phone, country, otp):
        self.id = userid,
        self.name = name,
        self.username = username,
        self.email = email,
        self.password = password,
        self.phone = phone,
        self.country = country,
        self.otp = otp
        
    def createUser(self):
        mobile = self.phone[0]
        if self.name is None or self.name == '':
            res = {}
            res.update({"error": "Name is required"})
            return res
        elif self.username is None or self.username == '':
            res = {}
            res.update({"error": "Username is required"})
            return res
        elif self.email is None or  self.email == '':
            res = {}
            res.update({"error": "Email is required"})
            return res
        elif self.password is None or self.password == '':
            res = {}
            res.update({"error": "Password is required"})
            return res
        elif self.phone is None:
            res = {}
            res.update({"error": "Phone is required"})
            return res
        elif len(mobile) != 10:
            print(mobile)
            res = {}
            res.update({"error": "Phone number is not appropriate"})
            return res
        elif self.country is None:
            res = {}
            res.update({"error": "Country is required"})
            return res
        else:
            try:
                mysql = db.configureDatabase()
                res = {}
                conn = mysql.connect()
                cursor = conn.cursor()
                # encrypted_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
                encrypted_password = generate_password_hash(self.password)
                current_timestamp = datetime.datetime.now()
                current_timestamp = str(current_timestamp)
                if(self.checkUser() == "Email already exists"):
                    res = {}
                    res.update({"error": "Email already exists"})
                    return res
                elif(self.checkUser() == "Username already exists"):
                    res = {}
                    res.update({"error": "Username already exists"})
                    return res
                else:
                    cursor.execute("INSERT INTO users(name,username, email, password, phone, country, createdat, otp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (self.name, self.username, self.email, self.password, self.phone, self.country, current_timestamp, ''))
                    data = cursor.fetchall()
                    if len(data) == 0:
                        otp_num = random.randint(1000,9999)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET otp = %s WHERE email = %s", (otp_num, self.email))
                        conn.commit()
                        res.update({"message": "Success"})
                        return res

            except Exception as e:
                return json.dumps({'error':str(e)})
            
            finally:
                cursor.close()
                conn.close()

    def login(self):
        if(self.username is None or self.username == ''):
            res = {}
            res.update({"error": "Username is required"})
            return res
        elif(self.password is None or self.password == ''):
            res = {}
            res.update({"error": "Password is required"})
            return res
        else:
            try:
                mysql = db.configureDatabase()
                conn = mysql.connect()
                cursor = conn.cursor()
                print(self.password)
                # encrypted_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("SELECT * FROM users WHERE username = %s AND PASSWORD = %s", (self.username, self.password))
                info = cursor.fetchall()
                print(info)
                if len(info) > 0:
                    res = {}
                    user_id = 0;
                    for data in info:
                        user_id = data[0]
                        res.update({"id": data[0], "name": data[1], "username": data[2], "email": data[3], "phone": data[5], "country": data[6], "createdat": data[7], "message": "Success"})
                    token = jwt.encode({'public_id' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, db.secret_key, "HS256")
                    res['token'] = token
                    return res
                else:
                    res = {}
                    print(len(info))
                    res.update({"error": "User does not exist"})
                    return res

            except Exception as e:
                return json.dumps({'error': str(e)})
            finally:
                cursor.close()
                conn.close()
    
    def checkUser(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor1 = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (self.email))
            cursor1.execute("SELECT * FROM users WHERE username = %s", (self.username))

            data = cursor.fetchall()
            if len(data) > 0:
                conn.commit()
                res = "Email already exists"
                return res
            
            data1 = cursor1.fetchall()
            if len(data1) > 0:
                conn.commit()
                res = "Username already exists"
                return res
        except Exception as e:
            return json.dumps({'error': str(e)})
        
        finally:
            cursor.close()
            cursor1.close()
            conn.close()

    def verifyOtp(self):
        if(self.email is None or self.email == ''):
            res = {}
            res.update({"error": "Email is required"})
            return res
        elif(self.otp is None or self.otp == ''):
            res = {}
            res.update({"error": "OTP is required"})
            return res
        else:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE otp = %s", (self.otp))
            data = cursor.fetchall()
            if len(data) > 0:
                res = {}
                user_id = 0;
                for dt in data:
                    user_id = dt[0]
                    res.update({"id": dt[0], "name": dt[1], "username": dt[2], "email": dt[3], "phone": dt[5], "country": dt[6], "createdat": dt[7], "message": "Success"})
                token = jwt.encode({'public_id' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, db.secret_key, "HS256")
                res['token'] = token
                return res
            else:
                return {"error": "OTP invalid"}

    def getProfileDetails(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            print(self.password)
            # encrypted_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("SELECT * FROM users WHERE id = %s", (self.id))
            info = cursor.fetchall()
            print(info)
            if len(info) > 0:
                res = {}
                for data in info:
                    res.update({"id": data[0], "name": data[1], "username": data[2], "email": data[3], "phone": data[5], "country": data[6], "createdat": data[7], "message": "Success"})
                return res
            else:
                res = {}
                print(len(info))
                res.update({"error": "User does not exist"})
                return res

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()

    def updateProfileDetails(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            if(self.checkRecord()):
                cursor.execute("UPDATE users SET name = %s, phone = %s, country = %s", (self.name, self.phone, self.country))
                conn.commit()
                return {"message": "Success"}
            else:
                return {"error": "User not available"}

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()

    def checkRecord(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id= %s", (self.id))
            data = cursor.fetchall()
            if(len(data) > 0):
                return True
            else:
                return False
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()


from flask import Flask,json
import db
import datetime

class Blogs:
    def __init__(self, blogid, userid, title, description, categoryId, isLiked, comment, commentid):
        self.blogid = blogid,
        self.userid = userid,
        self.title = title,
        self.description = description,
        self.categoryId = categoryId,
        self.isliked = isLiked,
        self.comment = comment,
        self.commentid = commentid

    def createBlog(self):
        if(self.title is None or self.title == ''):
            return {"error": "Title is required"}
        elif(self.description is None or self.description == ''):
            return {"error": "Description is required"}
        elif(self.categoryId is None):
            return {"error": "Category ID is required"}
        else:
            try:
                mysql = db.configureDatabase()
                conn = mysql.connect()
                cursor = conn.cursor()
                current_timestamp = datetime.datetime.now()
                current_timestamp = str(current_timestamp)
                cursor.execute("INSERT INTO blogs(userid,title,description,category_id,createdAt, likecount, commentcount) VALUES (%s,%s,%s,%s,%s, 0, 0)", (self.userid, self.title, self.description, self.categoryId, current_timestamp))
                data = cursor.fetchall()
                print(data)
                if(len(data) == 0):
                    conn.commit()
                    return {"message": "Success"}
            except Exception as e:
                return {"error": json.dumps(e)}

            finally:
                conn.close()
                cursor.close() 

    def editBlog(self):
        if(self.title is None or self.title == ''):
            return {"error": "Title is required"}
        elif(self.description is None or self.description == ''):
            return {"error": "Description is required"}
        elif(self.categoryId is None):
            return {"error": "Category ID is required"}
        else:
            try:
                mysql = db.configureDatabase()
                conn = mysql.connect()
                cursor = conn.cursor()
                current_timestamp = datetime.datetime.now()
                current_timestamp = str(current_timestamp)
                if(self.checkRecord(self.blogid)):
                    cursor.execute("UPDATE blogs SET title = %s, description = %s,category_id = %s WHERE id= %s", (self.title, self.description, self.categoryId, self.blogid))
                    conn.commit()
                    return {"message": "Success"}
                else:
                    return {"error": "Blog not available"}
            except Exception as e:
                return {"error": json.dumps(e)}

            finally:
                conn.close()
                cursor.close()

    def deleteBlog(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            if(self.checkRecord(self.blogid)):
                cursor.execute("DELETE FROM blogs WHERE id = %s", (self.blogid))
                conn.commit()
                return {"message": "Success"}
            else:
                return {"error": "Blog not available"}

        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()

    def checkRecord(self, blogId):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blogs WHERE id= %s", (blogId))
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

    def checkBlogLikes(self, userId, blogId):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM likes WHERE blogid= %s AND userid = %s", (blogId, userId))
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
    
    def isAlreadyLiked(self,blogId, userId):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT liked FROM likes WHERE blogid= %s AND userid = %s", (blogId, userId))
            data = cursor.fetchall()
            return data[0][0]

        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()


    def getBlogs(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT users.username, users.name, users.id, blogs.id, blogs.title, blogs.description, blogs.createdAt,blogs.likecount, blogs.commentcount,categories.id, categories.category_name FROM users JOIN blogs JOIN categories ON categories.id = blogs.category_id ORDER BY blogs.createdAt desc")
            blogs_list = []
            blogs = cursor.fetchall()
            for blog in blogs:
                res = {}
                res.update({"username": blog[0], "name": blog[1], "userid": blog[2], "blog_id": blog[3], "blog_title": blog[4], "blog_description": blog[5], "created_at": blog[6], "like_count": blog[7], "comment_count" : blog[8], "category_id": blog[9], "category_name": blog[10]})
                blogs_list.append(res)
            return blogs_list
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()   

    def getBlogsById(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT users.username, users.name, users.id, blogs.id, blogs.title, blogs.description, blogs.createdAt, blogs.likecount, blogs.commentcount, categories.id, categories.category_name FROM users JOIN blogs JOIN categories ON categories.id = blogs.category_id WHERE blogs.id = %s", (self.blogid))
            blogs = cursor.fetchall()
            if(len(blogs) > 0):
                for blog in blogs:
                    res = {}
                    res.update({"username": blog[0], "name": blog[1], "userid": blog[2], "blog_id": blog[3], "blog_title": blog[4], "blog_description": blog[5], "created_at": blog[6], "like_count": blog[7], "comment_count" : blog[8], "category_id": blog[9], "category_name": blog[10]})
                return res
            else:
                return {}
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()   

    def getBlogsByUserId(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT blogs.userid, users.name, users.username, blogs.id, blogs.title, blogs.description, blogs.createdAt, blogs.likecount, blogs.commentcount, categories.id, categories.category_name FROM blogs JOIN users JOIN categories ON blogs.category_id = categories.id WHERE userid = %s", (self.userid))
            blogs_list = []
            blogs = cursor.fetchall()
            if(len(blogs) > 0):
                for blog in blogs:
                    res = {}
                    res.update({"user_id": blog[0], "user_name": blog[1], "username": blog[2], "blog_id": blog[3], "title": blog[4], "description": blog[5], "createdAt": blog[6], "like_count": blog[7], "comment_count" : blog[8], "category_id": blog[9], "category_name": blog[10]})
                    blogs_list.append(res)
                return blogs_list
            else:
                return []
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()

    def getBlogsByCategoryId(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT blogs.userid, users.name, users.username, blogs.id, blogs.title, blogs.description, blogs.createdAt, blogs.likecount, blogs.commentcount, categories.id, categories.category_name FROM blogs JOIN users JOIN categories ON blogs.category_id = categories.id WHERE blogs.category_id = %s", (self.categoryId))
            blogs_list = []
            blogs = cursor.fetchall()
            if(len(blogs) > 0):
                for blog in blogs:
                    res = {}
                    res.update({"user_id": blog[0], "user_name": blog[1], "username": blog[2], "blog_id": blog[3], "title": blog[4], "description": blog[5], "createdAt": blog[6], "like_count": blog[7], "comment_count" : blog[8], "category_id": blog[9], "category_name": blog[10]})
                    blogs_list.append(res)
                return blogs_list
            else:
                return []
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()
    
    def getLikeCount(self):
        mysql = db.configureDatabase()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM likes WHERE blogid = %s AND liked = 1", (self.blogid))
        data = cursor.fetchall()
        conn.commit()
        return data[0][0]

    def getCommentCount(self):
        mysql = db.configureDatabase()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM comments WHERE blogid = %s", (self.blogid))
        data = cursor.fetchall()
        conn.commit()
        return data[0][0]


    def updateLikeCount(self):
        mysql = db.configureDatabase()
        conn = mysql.connect()
        cursor = conn.cursor()
        like_count = self.getLikeCount()
        print(like_count)
        cursor.execute("UPDATE blogs SET likecount = %s WHERE id = %s", (like_count, self.blogid))
        conn.commit()

    def updateCommentCount(self):
        mysql = db.configureDatabase()
        conn = mysql.connect()
        cursor = conn.cursor()
        comment_count = self.getCommentCount()
        cursor.execute("UPDATE blogs SET commentcount = %s WHERE id = %s", (comment_count, self.blogid))
        conn.commit()

    def likeUnlikeBlog(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            if(self.checkBlogLikes(self.userid, self.blogid) == False):
                cursor.execute("INSERT INTO likes(userid, blogid, liked) VALUES (%s, %s, %s)", (self.userid, self.blogid, self.isliked))
                conn.commit()
                self.updateLikeCount()
                return {"message": "Success"}
            else:
                val = self.isAlreadyLiked(self.blogid, self.userid)
                alreadyLiked = int(self.isliked[0])
                if(val == 1 and alreadyLiked == 1):
                    return {"error": "already liked"}
                elif(val == 0 and alreadyLiked == 0):
                    return {"error": "already disliked"}
                else:
                    cursor.execute("UPDATE likes SET liked = %s WHERE blogid = %s AND userid = %s", (self.isliked, self.blogid, self.userid))
                    conn.commit()
                    self.updateLikeCount()
                    return {"message": "Success"}
    
        except Exception as e:
            print(e)
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()
    
    def createComment(self):
        if(self.comment is None or self.comment == ''):
            return {"error": "Comment is required"}
        elif(self.userid is None or self.userid == ''):
            return {"error": "Userid is required"}
        elif(self.blogid is None or self.blogid == ''):
            return {"error": "blogid is required"}
        else:
            try:
                mysql = db.configureDatabase()
                conn = mysql.connect()
                cursor = conn.cursor()
                current_timestamp = datetime.datetime.now()
                current_timestamp = str(current_timestamp)
                cursor.execute("INSERT INTO comments(blogid,userid,comment,createdAt) VALUES (%s,%s,%s,%s)", (self.blogid, self.userid, self.comment, current_timestamp))
                data = cursor.fetchall()
                print(data)
                if(len(data) == 0):
                    conn.commit()
                    self.updateCommentCount()
                    return {"message": "Success"}
            except Exception as e:
                return {"error": json.dumps(e)}

            finally:
                conn.close()
                cursor.close() 

    def editComment(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            if(self.checkComment(self.commentid)):
                cursor.execute("UPDATE comments SET comment = %s WHERE id= %s", (self.comment, self.commentid))
                conn.commit()
                return {"message": "Success"}
            else:
                return {"error": "comment not available"}
        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()
            

    def deleteComment(self):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            if(self.checkComment(self.commentid)):
                cursor.execute("DELETE FROM comments WHERE id = %s", (self.commentid))
                self.updateCommentCount(self)
                conn.commit()
                return {"message": "Success"}
            else:
                return {"error": "comment not available"}

        except Exception as e:
            return {"error": json.dumps(e)}

        finally:
            conn.close()
            cursor.close()

    def checkComment(self, commentId):
        try:
            mysql = db.configureDatabase()
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM comments WHERE id= %s", (commentId))
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

    def getCommentsByBlogId(self):
        if(self.blogid is None or self.blogid == ''):
            return {"error": "blogid is required"}
        else:
            try:
                mysql = db.configureDatabase()
                conn = mysql.connect()
                cursor = conn.cursor()
                current_timestamp = datetime.datetime.now()
                current_timestamp = str(current_timestamp)
                cursor.execute("SELECT users.id, users.name, users.username, comments.id, comments.blogid, comments.comment, comments.createdat FROM users JOIN comments ON users.id = comments.userid WHERE comments.blogid = %s", (self.blogid))
                data = cursor.fetchall()
                comments_list = []
                print(data)
                for comment in data:
                    res = {}
                    res.update({"userid": comment[0], "name": comment[1], "username": comment[2], "commentid": comment[3], "blogid": comment[4], "comment": comment[5], "created_at": comment[6]})
                    comments_list.append(res)
                return comments_list

            except Exception as e:
                return {"error": json.dumps(e)}

            finally:
                conn.close()
                cursor.close()
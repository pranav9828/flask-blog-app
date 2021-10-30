from flask import Flask, request, jsonify
from models import users
from models import categories
from models import blogs


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/user', methods=['POST'])
def createUser():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        phone = request.form['phone']
        country = request.form['country']
        u = users.Users('', name, username, email, pwd, phone, country, otp='')
        res = u.createUser()
        res = jsonify(res)
        return res

@app.route('/api/login', methods=['POST'])
def loginUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = users.Users(userid='', name='',username=username, email='', password=password, phone='', country='', otp='')
        res = u.login()
        res = jsonify(res)
        return res

@app.route('/api/verify', methods=['POST'])
def verifyOtp():
    if request.method == 'POST':
        email = request.form['email']
        otp = request.form['otp']
        u = users.Users(userid= '', name='', username='', email=email, password='', phone='', country='', otp=otp)
        res = u.verifyOtp()
        res = jsonify(res)
        return res

@app.route('/api/categories', methods=['GET'])
def getCategories():
    if request.method == 'GET':
        cat = categories.Categories()
        res = cat.getCategories()
        res = jsonify(res)
        return res

@app.route('/api/blog', methods=['GET', 'POST'])
def createblog():
    if request.method == 'POST':
        userid = request.form['userid']
        title = request.form['title']
        description = request.form['description']
        categoryId = request.form['categoryId']
        blog = blogs.Blogs(userid=userid, blogid='', title=title,description=description, categoryId=categoryId, isLiked='', comment='', commentid='')
        res = blog.createBlog()
        res = jsonify(res)
        return res
    elif request.method == 'GET':
        blog = blogs.Blogs(userid='', blogid='', title='',description='', categoryId='', isLiked='', comment='', commentid='')
        res = blog.getBlogs()
        res = jsonify(res)
        return res

@app.route('/api/blog/<blog_id>', methods=['PUT', 'DELETE', 'GET'])
def blog(blog_id):
    if request.method == 'PUT':
        title = request.form['title']
        description = request.form['description']
        categoryId = request.form['categoryId']
        blogid = blog_id
        blog = blogs.Blogs(blogid=blogid, title=title,description=description, categoryId=categoryId, userid = '', isLiked='', comment='', commentid='')
        res = blog.editBlog()
        res = jsonify(res)
        return res
    elif request.method == 'DELETE':
        blogid = blog_id
        blog = blogs.Blogs(blogid=blogid, title='',description='', categoryId='', userid = '', isLiked='', comment='', commentid='')
        res = blog.deleteBlog()
        res = jsonify(res)
        return res
    elif request.method == 'GET':
        blogid = blog_id
        blog = blogs.Blogs(userid='', blogid=blogid, title='',description='', categoryId='', isLiked='', comment='', commentid='')
        res = blog.getBlogsById()
        res = jsonify(res)
        return res

@app.route('/api/user/blog/<user_id>', methods=['GET'])
def blogByUserId(user_id):
    if request.method == 'GET':
        userId = user_id
        blog = blogs.Blogs(userid=userId, blogid='', title='',description='', categoryId='', isLiked='', comment='', commentid='')
        res = blog.getBlogsByUserId()
        res = jsonify(res)
        return res

@app.route('/api/category/blog/<category_id>', methods=['GET'])
def blogByCategoryId(category_id):
    if request.method == 'GET':
        categoryId = category_id
        blog = blogs.Blogs(userid='', blogid='', title='',description='', categoryId=categoryId, isLiked='', comment='', commentid='')
        res = blog.getBlogsByCategoryId()
        res = jsonify(res)
        return res

@app.route('/api/member/details/<user_id>', methods=['GET', 'PUT'])
def getProfileDetailsByUserId(user_id):
    if request.method == 'GET':
        userId = user_id
        u = users.Users(userid=userId, name='', username='', email='', password='', phone='', country='', otp='')
        res = u.getProfileDetails()
        res = jsonify(res)
        return res
    elif request.method == 'PUT':
        userId = user_id
        user_name = request.form['name']
        mobile = request.form['phone']
        country = request.form['country']
        u = users.Users(userid=userId, name=user_name, username='', email='', password='', phone=mobile, country=country, otp='')
        res = u.updateProfileDetails()
        res = jsonify(res)
        return res

@app.route('/api/blog/like', methods=['POST'])
def likeBlog():
    if request.method == 'POST':
        usid = request.form['userid']
        blogid = request.form['blogid']
        liked = request.form['liked']
        blog = blogs.Blogs(userid=usid, blogid=blogid, title='', description='', categoryId='', isLiked=liked, comment='', commentid='')
        res = blog.likeUnlikeBlog()
        res = jsonify(res)
        return res

@app.route('/api/blog/comment', methods=['POST','GET'])
def comment():
    if request.method == 'POST':
        usid = request.form['userid']
        blogid = request.form['blogid']
        comment = request.form['comment']
        blog = blogs.Blogs(userid=usid, blogid=blogid, title='', description='', categoryId='', isLiked='', comment=comment, commentid='')
        res = blog.createComment()
        res = jsonify(res)
        return res
    elif request.method == 'GET':
        blogid = request.form['blogid']
        blog = blogs.Blogs(userid='', blogid=blogid, title='', description='', categoryId='', isLiked='', comment='', commentid='')
        res = blog.getCommentsByBlogId()
        res = jsonify(res)
        return res

@app.route('/api/blog/comment/<comment_id>', methods=[ 'PUT', 'DELETE'])
def editcomment(comment_id):
    if request.method == 'PUT':
        cid = comment_id
        comment = request.form['comment']
        blog = blogs.Blogs(userid='', blogid='', title='', description='', categoryId='', isLiked='', comment=comment, commentid=cid)
        res = blog.editComment()
        res = jsonify(res)
        return res
    elif request.method == 'DELETE':
        cid = comment_id
        blog = blogs.Blogs(userid='', blogid='', title='', description='', categoryId='', isLiked='', comment='', commentid=cid)
        res = blog.deleteComment()
        res = jsonify(res)
        return res
        

if __name__ == '__main__':
    app.run(debug=True)

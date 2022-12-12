from flask import Flask, request, session, render_template

from modules.admin import admin
from modules.blog import blog
from modules.entity import maptouser
from modules.sqltool import Sql
from modules.user import user
from modules.comment import comment

app = Flask(__name__)
app.secret_key = 'blog_session'


# 敏感操作需要验证是否登录
@app.before_request
def login_check():
    url = request.path
    noUrl = ["/blog/addBlog", "/blog/delBlog", "/blog/updBlog",
             "/blog/toUpd", "/blog/toAdd", "/space", "/user/delUser",
             "/user/updUser", "/user/toUpd", "/comment/addComment",
             "/user/report","/blog/report"]
    if url in noUrl:
        _id = session.get('uid', None)
        print('敏感操作: ', url, ": ", _id)
        if not _id:
            return render_template('user/login.html', msg='您未登录,不能进行此操作')
        else:
            user_status  = maptouser(Sql.get_user(session.get('mail'))).status
            session['status'] = user_status
            return
    else:
        return


@admin.before_request
def admin_check():
    url = request.path
    noUrl = ["/admin/login", "/admin/tologin"]
    if url not in noUrl:
        _status = session.get('status')
        if _status is None:
            return render_template('user/login.html',msg='您未登录,禁止访问此页面')
        if _status != 3:
            return render_template('result.html', msg='您不是管理员,禁止访问此页面!')
        else:
            return
    else:
        return


@app.before_request
def ban_check():
    url = request.path
    noUrl = ['/blog/toUpd', "/blog/updBlog", "/blog/addBlog", "/blog/toAdd", '/blog/delBlog','/comment/addComment']
    if url in noUrl:
        _status = session.get('status')
        if _status == 1:
            return render_template('result.html', msg='您现处于封禁状态中,无法进行此操作!!')
        else:
            return
    else:
        return


@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.register_blueprint(blog)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(comment)
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)

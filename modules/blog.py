from flask import Blueprint, session, render_template, request
import time

from modules.comment import get_blog_comment
from modules.sqltool import Sql
from modules.entity import *

blog = Blueprint('blog', __name__)


# 主页博客展示
@blog.route('/')
def index_page():
    li = maptobloglist(Sql.get_all_blog())
    if session.get('uid', None) is not None:
        mail = session.get('mail')
        return render_template('blog/index.html', blogs=li, login=True, mail=mail)
    else:
        return render_template('blog/index.html', blogs=li, login=False, mail=None)


# 用户个人空间
@blog.route('/space')
def center_page():
    num = Sql.count_blog(session.get('uid'))
    li = maptobloglist(Sql.get_user_blog(session.get('uid')))
    print(li)
    return render_template('blog/space.html', blogs=li, num=num, mail=session.get('mail'))


# 关键词搜索博客
@blog.route('/search', methods=['GET'])
def search_blog():
    keyword = request.args.get('keyword')
    blogs = maptobloglist(Sql.search_blog(keyword))
    return render_template('blog/search.html', blogs=blogs)


# 添加博客页面
@blog.route('/blog/toAdd')
def add_page():
    uid = session.get('uid', None)
    umail = session.get('mail')
    return render_template('blog/addBlog.html', uid=uid, umail=umail)


# 修改博客页面
@blog.route('/blog/toUpd')
def upd_page():
    bid = request.args.get('bid')
    blog = Sql.get_blog(bid)
    blog = maptoblog(blog)
    if blog is None:
        return render_template('result.html', msg='没有这篇博客')
    return render_template('blog/updPage.html', blog=blog)


# 博客详情页
@blog.route('/blog/<int:bid>')
def get_blog(bid):
    if session.get('uid', None) is not None:
        login = True
    else:
        login = False
    mail = session.get('mail')
    status = session.get('status')
    blog = maptoblog(Sql.get_blog(bid))

    if blog.status == 2 and blog.umail != mail and status != 3:
        return render_template('result.html', msg='该博客已封禁')

    comments = get_blog_comment(bid)
    return render_template('blog/blog.html', blog=blog, login=login, mail=mail, comments=comments)


# 添加博客
@blog.route('/blog/addBlog', methods=['POST'])
def add_Blog():
    status = request.form.get('status')
    uid = request.form.get('uid')
    umail = request.form.get('umail')
    content = request.form.get('content')
    title = request.form.get('title')
    date = time.strftime("%Y-%m-%d", time.localtime())

    if Sql.add_blog(uid, title, content, date, umail, status):
        return render_template('result.html', msg='成功!')
    else:
        return render_template('result.html', msg='失败!')


# 删除博客
@blog.route('/blog/delBlog', methods=['GET'])
def del_Blog():
    login_uid = session.get('uid')
    bid = request.args.get('bid')
    blog = maptoblog(Sql.get_blog(bid))
    if blog is not None:
        if login_uid != blog.uid:
            msg = '您没有操作的权限'
        else:
            # 删除博客
            if Sql.del_blog(bid, login_uid):
                msg = '删除成功'
            else:
                msg = '删除失败'
    else:
        msg = '没有这个博客'
    return render_template('result.html', msg=msg)


# 修改博客
@blog.route('/blog/updBlog', methods=['POST'])
def upd_Blog():
    status = request.form.get('status')
    uid = int(request.form.get('uid'))
    bid = request.form.get('bid')
    title = request.form.get('title')
    content = request.form.get('content')

    suid = int(session.get('uid'))
    if suid != uid:
        msg = '您没有修改的权限'
    else:
        if Sql.upd_blog(uid, bid, title, content, status):
            msg = '修改成功'
        else:
            msg = '修改失败'
    return render_template('result.html', msg=msg)

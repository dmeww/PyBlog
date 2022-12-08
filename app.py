#coding=utf-8
from flask import Flask, render_template, request, session, redirect

from model import *
from mysqlutil import *
import time

app = Flask(__name__)
app.secret_key = 'alpha_session'
sql = MysqlUnit('root', 'root', '127.0.0.1', 3306, 'python')


@app.route('/')
def index_page():
    li = maptobloglist(sql.get_all_blog())
    if session.get('uid', None) is not None:
        mail = session.get('mail')
        return render_template('index.html', blogs=li, login=True, mail=mail)
    else:
        return render_template('index.html', blogs=li, login=False, mail=None)


@app.route('/login')
def login_page():
    return render_template('login.html', msg='请登录')


@app.route('/blog/toAdd')
def add_page():
    uid = session.get('uid', None)
    umail = session.get('mail')
    return render_template('addBlog.html', uid=uid, umail=umail)


@app.route('/blog/toUpd')
def upd_page():
    bid = request.args.get('bid')
    blog = sql.get_blog(bid)
    blog = maptoblog(blog)
    if blog is None:
        return render_template('result.html', msg='没有这篇博客')
    return render_template('updPage.html', blog=blog)


@app.route('/space')
def center_page():
    num = sql.count_blog(session.get('uid'))
    li = maptobloglist(sql.get_user_blog(session.get('uid')))
    print(li)
    return render_template('space.html', blogs=li, num=num, mail=session.get('mail'))


@app.route('/tologin', methods=['POST'])
def login():
    mail = request.form.get('mail')
    passwd = request.form.get('password')

    if validateEmail(mail) is False:
        return render_template('login.html', msg='邮箱格式不对')
    if passwd == '' or passwd is None:
        return render_template('login.html', msg='密码不能为空')

    l_user = User(mail=mail, password=passwd, uid=None)
    d_user = maptouser(sql.get_user(mail))

    if d_user is None:
        return render_template('login.html', msg='没有此用户!')
    else:
        if d_user.password != l_user.password:
            return render_template('login.html', msg='密码错误!')
        else:
            session['uid'] = d_user.uid
            session['mail'] = d_user.mail
            session['passwd'] = d_user.password
            return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('result.html', msg='操作成功!')


@app.route('/toRegister', methods=['POST'])
def register():
    mail = request.form.get('mail')
    passwd = request.form.get('password')

    if validateEmail(mail) is False:
        return render_template('login.html', msg='邮箱格式不对')
    if passwd == '' or passwd is None:
        return render_template('login.html', msg='密码不能为空')
    if len(passwd) <= 8:
        return render_template('login.html', msg='密码必须大于等于8位')
    if sql.get_user(mail=mail) is not None:
        return render_template('login.html', msg='这个邮箱已经使用过了')

    if sql.add_user(mail, passwd):
        msg = '注册成功'
    else:
        msg = '服务器出错,请稍后重试'
    return render_template('result.html', msg=msg)


@app.route('/blog/<int:bid>')
def get_blog(bid):
    if session.get('uid', None) is not None:
        login = True
    else:
        login = False
    mail = session.get('mail')
    blog = maptoblog(sql.get_blog(bid))
    return render_template('blog.html', blog=blog, login=login, mail=mail)


@app.route('/blog/addBlog', methods=['POST'])
def add_Blog():
    uid = request.form.get('uid')
    umail = request.form.get('umail')
    content = request.form.get('content')
    title = request.form.get('title')
    date = time.strftime("%Y-%m-%d", time.localtime())

    if sql.add_blog(uid, title, content, date, umail):
        return render_template('result.html', msg='成功!')
    else:
        return render_template('result.html', msg='失败!')


@app.route('/blog/delBlog', methods=['GET'])
def del_Blog():
    login_uid = session.get('uid')
    bid = request.args.get('bid')
    blog = maptoblog(sql.get_blog(bid))
    if blog is not None:
        if login_uid != blog.uid:
            msg = '您没有操作的权限'
        else:
            # 删除博客
            if sql.del_blog(bid, login_uid):
                msg = '删除成功'
            else:
                msg = '删除失败'
    else:
        msg = '没有这个博客'
    return render_template('result.html', msg=msg)


@app.route('/blog/updBlog', methods=['POST'])
def upd_Blog():
    uid = int(request.form.get('uid'))
    bid = request.form.get('bid')
    title = request.form.get('title')
    content = request.form.get('content')

    suid = int(session.get('uid'))
    if suid != uid:
        msg = '您没有修改的权限'
    else:
        if sql.upd_blog(uid, bid, title, content):
            msg = '修改成功'
        else:
            msg = '修改失败'
    return render_template('result.html', msg=msg)


@app.route('/search', methods=['GET'])
def search_blog():
    keyword = request.args.get('keyword')
    blogs = maptobloglist(sql.search_blog(keyword))
    return render_template('search.html', blogs=blogs)


@app.route('/user/toUpd')
def upd_user_page():
    user = maptouser(sql.get_user(session.get('mail')))
    return render_template('userUpd.html', user=user)


@app.route('/user/updUser', methods=['POST'])
def upd_user():
    uid = session.get('uid')
    mail = session.get('mail')
    n_passwd = request.form.get('password')
    n_mail = request.form.get('mail')
    if validateEmail(n_mail) is False:
        msg = '新邮箱格式不合法'
        return render_template('result.html', msg=msg)
    if n_passwd == '' or None:
        msg = '新密码不能为空'
        return render_template('result.html', msg=msg)
    if sql.upd_user(uid, mail, n_passwd, n_mail):
        msg = '修改成功,请重新登录'
        session.clear()
    else:
        msg = '修改失败'
    return render_template('result.html', msg=msg)


@app.route('/user/delUser')
def delUser():
    uid = session.get('uid')
    mail = session.get('mail')
    if sql.del_user(uid):
        msg = '注销成功'
        session.clear()
    else:
        msg = '服务器错误,注销失败'
    return render_template('result.html', msg=msg)


# 敏感操作需要验证是否登录
@app.before_request
def check():
    url = request.path
    noUrl = ["/blog/addBlog", "/blog/delBlog", "/blog/updBlog",
             "/blog/toUpd", "/space","/user/delUser",
             "/user/updUser","/user/toUpd"]
    if url in noUrl:
        _id = session.get('uid', None)
        print('permission check: ', _id)
        if not _id:
            return render_template('login.html', msg='您未登录,不能进行此操作')
        else:
            return
    else:
        return


@app.errorhandler(404)
def err404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1')

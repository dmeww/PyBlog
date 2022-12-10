from flask import Blueprint, render_template, request, session, redirect
from modules.entity import *
from modules.sqltool import Sql

user = Blueprint('user', __name__)


# 登录页面
@user.route('/login')
def login_page():
    return render_template('user/login.html', msg='请登录')


# 用户信息修改页面
@user.route('/user/toUpd')
def upd_user_page():
    user = maptouser(Sql.get_user(session.get('mail')))
    return render_template('user/userUpd.html', user=user)


# 用户登录处理
@user.route('/tologin', methods=['POST'])
def login():
    mail = request.form.get('mail')
    passwd = request.form.get('password')

    if validateEmail(mail) is False:
        return render_template('user/login.html', msg='邮箱格式不对')
    if passwd == '' or passwd is None:
        return render_template('user/login.html', msg='密码不能为空')

    l_user = User(mail=mail, password=passwd, uid=None,status=0)
    d_user = maptouser(Sql.get_user(mail))

    if d_user is None:
        return render_template('user/login.html', msg='没有此用户!')
    else:
        if d_user.password != l_user.password:
            return render_template('user/login.html', msg='密码错误!')
        else:
            session['uid'] = d_user.uid
            session['mail'] = d_user.mail
            session['passwd'] = d_user.password
            session['status'] = d_user.status
            return redirect('/')


# 用户登出
@user.route('/logout')
def logout():
    session.clear()
    return render_template('result.html', msg='操作成功!')


# 用户注册
@user.route('/toRegister', methods=['POST'])
def register():
    mail = request.form.get('mail')
    passwd = request.form.get('password')
    passwd2 = request.form.get('password2')

    if passwd != passwd2:
        return render_template('user/login.html',msg='两次密码必须一致')
    if validateEmail(mail) is False:
        return render_template('user/login.html', msg='邮箱格式不对')
    if passwd == '' or passwd is None:
        return render_template('user/login.html', msg='密码不能为空')
    if len(passwd) <= 8:
        return render_template('user/login.html', msg='密码必须大于等于8位')
    if Sql.get_user(mail=mail) is not None:
        return render_template('user/login.html', msg='这个邮箱已经使用过了')

    if Sql.add_user(mail, passwd):
        msg = '注册成功'
    else:
        msg = '服务器出错,请稍后重试'
    return render_template('result.html', msg=msg)


# 用户信息修改
@user.route('/user/updUser', methods=['POST'])
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
    if Sql.upd_user(uid, mail, n_passwd, n_mail):
        msg = '修改成功,请重新登录'
        session.clear()
    else:
        msg = '修改失败'
    return render_template('result.html', msg=msg)


# 删除用户
@user.route('/user/delUser')
def delUser():
    uid = session.get('uid')
    mail = session.get('mail')
    if Sql.del_user(uid):
        msg = '注销成功'
        session.clear()
    else:
        msg = '服务器错误,注销失败'
    return render_template('result.html', msg=msg)

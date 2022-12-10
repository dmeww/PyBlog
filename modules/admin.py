from flask import Blueprint, render_template, session, request, redirect

from modules.entity import *
from modules.sqltool import Sql

admin = Blueprint('admin', __name__)


@admin.route('/admin/login')
def admin_login_page():
    return render_template('admin/login.html')


@admin.route('/admin/tologin', methods=['POST'])
def admin_login():
    mail = request.form.get('mail')
    passwd = request.form.get('password')
    query_user = maptouser(Sql.get_user(mail))
    if query_user.password == passwd:
        if query_user.status != 3:
            return render_template('result.html', msg='您不是管理员', url='/admin/login')
        else:
            session.clear()
            session['admin_mail'] = query_user.mail
            session['status'] = 3
            return redirect('/admin')
    else:
        return render_template('result.html', msg='密码错误', url='/admin/login')


@admin.route('/admin')
def menu_page():
    mail = session.get('admin_mail')
    return render_template('admin/menu_page.html', mail=mail)


@admin.route('/admin/user')
def free_user():
    mail = session.get('admin_mail')
    users = maptouserlist(Sql.get_all_user())
    return render_template('admin/user.html', mail=mail, users=users)


@admin.route('/admin/bannedUser')
def baned_user():
    mail = session.get('admin_mail')
    users = maptouserlist(Sql.get_all_user())
    return render_template('admin/bannedUser.html', mail=mail, users=users)


@admin.route('/admin/blog')
def manage_blog():
    mail = session.get('admin_mail')
    blogs = maptobloglist(Sql.get_all_blog_by_admin())
    for i in blogs:
        print(i)
    return render_template('admin/blog.html', mail=mail, blogs=blogs)


@admin.route('/admin/bannedBlog')
def go_deban_blog():
    mail = session.get('admin_mail')
    blogs = maptobloglist(Sql.get_all_blog_by_admin())
    return render_template('admin/bannedBlog.html', mail=mail, blogs=blogs)


@admin.route('/admin/banUser')
def ban_user():
    uid = request.args.get('uid')
    if Sql.ban_user(uid):
        msg = '已封禁用户'
    else:
        msg = '封禁失败,请检查服务器'
    return render_template('admin/result.html', msg=msg, url='/admin')


@admin.route('/admin/debanUser')
def deban_user():
    uid = request.args.get('uid')
    if Sql.deban_user(uid):
        msg = '已解封用户'
    else:
        msg = '解封失败,请检查服务器'
    return render_template('admin/result.html', msg=msg, url='/admin')


@admin.route('/admin/banBlog')
def ban_blog():
    bid = request.args.get('bid')
    if Sql.ban_blog(bid):
        msg = '已封禁博客'
    else:
        msg = '封禁失败,请检查服务器'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')


@admin.route('/admin/debanBlog')
def deban_blog():
    bid = request.args.get('bid')
    if Sql.deban_blog(bid):
        msg = '已解封博客'
    else:
        msg = '解封失败,请检查服务器'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')


@admin.route('/admin/banComment')
def ban_comment():
    bid = request.args.get('bid')
    if Sql.ban_comment(bid):
        msg = '已禁止改博客评论'
    else:
        msg = '禁止失败,请检查服务器日志'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')


@admin.route('/admin/debanComment')
def deban_comment():
    bid = request.args.get('bid')
    if Sql.deban_comment(bid):
        msg = '已解锁博客评论'
    else:
        msg = '解锁失败,请检查服务器日志'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')

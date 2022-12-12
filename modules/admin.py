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
    users = maptouserlist(Sql.admin_search_user('',0))
    return render_template('admin/user.html', mail=mail, users=users)


@admin.route('/admin/bannedUser')
def baned_user():
    mail = session.get('admin_mail')
    users = maptouserlist(Sql.admin_search_user('', 2))
    return render_template('admin/bannedUser.html', mail=mail, users=users)


@admin.route('/admin/blog')
def manage_blog():
    mail = session.get('admin_mail')
    blogs = maptobloglist(Sql.admin_search_blog('',0))
    return render_template('admin/blog.html', mail=mail, blogs=blogs)


@admin.route('/admin/bannedBlog')
def go_deban_blog():
    mail = session.get('admin_mail')
    blogs = maptobloglist(Sql.admin_search_blog('',2))

    return render_template('admin/bannedBlog.html', mail=mail, blogs=blogs)


@admin.route('/admin/banUser')
def ban_user():
    uid = request.args.get('uid')
    if Sql.ban_user(uid) and Sql.clear_report('user', uid):
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
    if Sql.ban_blog(bid) and Sql.clear_report('blog', bid):
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
    return render_template('admin/result.html', msg=msg, url='/admin')


@admin.route('/admin/banComment')
def ban_comment():
    bid = request.args.get('bid')
    if Sql.ban_comment(bid):
        msg = '已禁止该博客评论'
    else:
        msg = '禁止失败,请检查服务器日志'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')


@admin.route('/admin/debanComment')
def deban_comment():
    bid = request.args.get('bid')
    if Sql.deban_comment(bid):
        msg = '已允许博客评论'
    else:
        msg = '解锁失败,请检查服务器日志'
    return render_template('admin/result.html', msg=msg, url='/admin/blog')


@admin.route('/admin/blog/report')
def report_blog():
    blogs = maptobloglist(Sql.admin_search_blog('',1))
    mail = session.get('admin_mail')
    return render_template('admin/reportBlog.html', blogs=blogs, mail=mail)


@admin.route('/admin/user/report')
def report_user():
    users = maptouserlist(Sql.admin_search_user('', 1))
    mail = session.get('admin_mail')
    return render_template('admin/reportUser.html', users=users, mail=mail)


@admin.route('/admin/clearReport')
def clear_report():
    uid = request.args.get('uid')
    bid = request.args.get('bid')
    if uid is None and bid is not None:
        if Sql.clear_report('blog', bid):
            return redirect('/admin/blog/report')
        else:
            return render_template('admin/result.html', msg='清除失败,请查看服务器日志', url='/admin/blog/report')
    elif uid is not None and bid is None:
        if Sql.clear_report('user', uid):
            return redirect('/admin/blog/report')
        else:
            return render_template('admin/result.html', msg='清除失败,请查看服务器日志', url='/admin/blog/report')
    else:
        return render_template('admin/result.html', msg='参数获取失败,请重新发送', url='/admin/blog/report')


# 用户管理类型 0=正常用户 1=受举报用户 2=已封禁用户
@admin.route('/admin/user/search')
def user_search():
    type = int(request.args.get('type'))
    keyword = request.args.get('keyword')
    mail = session.get('admin_mail')
    users = maptouserlist(Sql.admin_search_user(keyword, type))
    if type == 0:
        return render_template('admin/user.html', mail=mail, users=users)
    elif type == 1:
        return render_template('admin/reportUser.html', mail=mail, users=users)
    else:
        return render_template('admin/bannedUser.html', mail=mail, users=users)


# 博客管理类型 0=正常博客搜索 1=受举报博客 2=已封禁博客
@admin.route('/admin/blog/search')
def blog_search():
    type = int(request.args.get('type'))
    keyword = request.args.get('keyword')
    mail = session.get('admin_mail')
    blogs = maptobloglist(Sql.admin_search_blog(keyword,type))
    if type == 0:
        return render_template('admin/blog.html', mail=mail, blogs=blogs)
    elif type == 1:
        return render_template('admin/reportBlog.html', mail=mail, blogs=blogs)
    else:
        return render_template('admin/bannedBlog.html', mail=mail, blogs=blogs)
from flask import Blueprint, session, render_template, request
from modules.sqltool import Sql
from modules.entity import *

comment = Blueprint('comment', __name__)


@comment.route('/comment/addComment',methods=['POST'])
def add_comment():
    content = request.form.get('content')
    umail = request.form.get('mail')
    bid = request.form.get('bid')

    if Sql.add_comment(content, umail, bid):
        return render_template('result.html', msg="评论成功")
    else:
        return render_template('result.html', msg="评论失败")


@comment.route('/comment/delComment')
def del_comment():
    id = request.args.get("id")

    if Sql.del_comment(id):
        return render_template('result.html', msg="删除评论成功")
    else:
        return render_template('result.html', msg="删除评论失败")


def get_blog_comment(bid):
    comments = maptocommentlist(Sql.get_comments(bid))
    return comments

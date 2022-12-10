# coding=utf-8
import re


class Blog(object):
    def __init__(self):
        self.title = ''
        self.content = None
        self.date = None
        self.uid = None
        self.bid = -1
        self.umail = None
        self.status = None
        self.comment=None

    def __str__(self):
        return f'{self.bid}:{self.umail}--{type(self.status)}'


class User(object):
    def __init__(self, mail, password, uid, status):
        self.mail = mail
        self.password = password
        self.uid = uid
        self.status = status


class Comment(object):
    def __init__(self):
        self.id = None
        self.content = None
        self.umail = None
        self.bid = None

    def __str__(self):
        return f"{self.id}:{self.content}"


def maptoblog(target):
    if target is None:
        return None
    else:
        blog = Blog()
        blog.bid = int(target[0])
        blog.content = target[1]
        blog.title = target[2]
        blog.uid = int(target[3])
        blog.date = target[4]
        blog.umail = target[5]
        blog.status = int(target[6])
        blog.comment = int(target[7])
        return blog


def maptobloglist(target):
    li = []
    for i in target:
        li.append(maptoblog(i))
    return li


def maptouser(target):
    if target is None:
        return None
    else:
        user = User(uid=int(target[0]), password=target[1], mail=target[2], status=int(target[3]))
        return user


def maptouserlist(target):
    li = []
    for i in target:
        li.append(maptouser(i))
    return li


def maptocomment(target):
    if target is None:
        return None
    else:
        comment = Comment()
        comment.id = int(target[0])
        comment.content = target[1]
        comment.umail = target[2]
        comment.bid = int(target[3])
        return comment


def maptocommentlist(target):
    li = []
    for i in target:
        li.append(maptocomment(i))
    return li


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return True
        else:
            return False
    else:
        return False

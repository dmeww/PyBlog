#coding=utf-8
import re


class Blog(object):
    def __init__(self):
        self.title = ''
        self.content = None
        self.date = None
        self.uid = None
        self.bid = -1
        self.umail=None


class User(object):
    def __init__(self, mail, password, uid):
        self.mail = mail
        self.password = password
        self.uid = uid


def maptobloglist(target):
    li = []
    if target is None:
        return li
    else:
        for i in target:
            temp = Blog()
            temp.bid = i[0]
            temp.content = i[1]
            temp.title = i[2]
            temp.uid = i[3]
            temp.date = i[4]
            temp.umail = i[5]
            li.append(temp)

        return li


def maptoblog(target):
    if target is None:
        return None
    else:
        blog = Blog()
        blog.bid = target[0]
        blog.content = target[1]
        blog.title = target[2]
        blog.uid = target[3]
        blog.date = target[4]
        blog.umail=target[5]
        return blog


def maptouser(target):
    if target is None:
        return None
    else:
        user = User(uid=target[0], password=target[1], mail=target[2])
        return user


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return True
        else:
            return False
    else:
        return False

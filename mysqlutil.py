#coding=utf-8
from pymysql import *


class MysqlUnit(object):
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        try:
            self.conn = connect(
                user=self.username,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port
            )
        except Exception as e:
            print('MYSQL连接失败')
            print(e.__class__.__name__, ":", e)
        self.cursor = self.conn.cursor()

    def get_all_blog(self):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute('select * from blog')
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def get_user_blog(self, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select * from blog where uid = {uid}')
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def get_blog(self, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select * from blog where bid = {bid}')
            blog = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.close()
            return blog
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def search_blog(self, keyword):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select * from blog where title like "%{keyword}%"')
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def count_blog(self, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select count(*) from blog where uid = {uid}')
            num = self.cursor.fetchone()[0]
            self.conn.commit()
            self.cursor.close()
            return num
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return -1

    def get_user(self, mail):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"select * from user where mail = '{mail}'")
            user = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.close()
            return user
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def add_user(self, mail, passwd):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"insert into user(password, mail)values ('{passwd}','{mail}')")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def add_blog(self, uid, title, content, date, umail):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                f"insert into blog (content, title, uid, date,umail)values ('{content}','{title}',{uid},'{date}','{umail}');")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def del_blog(self, bid, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"delete from blog where uid={uid} and bid={bid};")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def upd_blog(self, uid, bid, title, content):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                f"update blog set title = '{title}',content='{content}' where uid = {uid} and bid = {bid};")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def upd_user(self, uid, mail, password, new_mail):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update user set mail = '{new_mail}',password='{password}' where uid = {uid} ;")
            self.conn.commit()
            if mail != new_mail:
                self.cursor = self.conn.cursor()
                self.cursor.execute(f"update blog set umail = '{new_mail}' where uid = {uid};")
                # a = 1/0
                self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def del_user(self, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"delete from user where uid={uid};")
            self.conn.commit()
            self.cursor.execute(f"update blog set umail='用户已注销' where uid = {uid};")
            # a = 1/0
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

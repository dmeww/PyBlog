# coding=utf-8
from pymysql import *


class MysqlTool(object):
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

    def get_all_blog_by_admin(self):
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

    def get_all_blog(self):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute('select * from blog where status = 0 or status = 3')
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

    def search_blog(self, keyword):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select * from blog where title like "%{keyword}%" and status = 0')
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

    def get_all_user(self):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"select * from user where uid != 3")
            users = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return users
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def add_user(self, mail, passwd):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"insert into user(password, mail,status)values ('{passwd}','{mail}',0)")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def add_blog(self, uid, title, content, date, umail, status):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                f"insert into blog (content, title, uid, date,umail,status,comment)values ('{content}','{title}',{uid},'{date}','{umail}',{status},0);")
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
            self.cursor.execute(f'delete from comment where bid ={bid}')
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            self.conn.rollback()
            return False

    def upd_blog(self, uid, bid, title, content, status):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                f"update blog set title = '{title}',content='{content}',status={status} where uid = {uid} and bid = {bid};")
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

    def get_comments(self, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"select * from comment where bid = '{bid}'")
            comments = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return comments
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def ban_user(self, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'update user set status = 1 where uid = {uid}')
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def deban_user(self, uid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'update user set status = 0 where uid = {uid}')
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def ban_blog(self, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'update blog set status = 2 where bid = {bid}')
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def deban_blog(self, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'update blog set status = 1 where bid = {bid}')
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def add_comment(self, content, umail, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"insert into comment (content, umail, bid) values ('{content}','{umail}',{bid});")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def ban_comment(self,bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update blog set comment = 1 where bid ={bid}")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def deban_comment(self,bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update blog set comment = 0 where bid ={bid}")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False


Sql = MysqlTool('root', 'root', '127.0.0.1', 3306, 'python')
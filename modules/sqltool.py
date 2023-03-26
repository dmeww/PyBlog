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
            self.cursor.execute(f"select * from user where status != 3")
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
            self.cursor.execute(f"insert into user(password, mail,status,report)values ('{passwd}','{mail}',0,0)")
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
                f"insert into blog (content, title, uid, date,umail,status,comment,report)values ('{content}','{title}',{uid},'{date}','{umail}',{status},0,0);")
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

    def ban_comment(self, bid):
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

    def deban_comment(self, bid):
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

    def report_user(self, mail):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update user set report = report+1 where mail ='{mail}'")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def report_blog(self, bid):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update blog set report = report+1 where bid ={bid}")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def clear_report(self, table, id):
        if table is 'user':
            col = 'uid'
        else:
            col = 'bid'
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"update {table} set report = 0 where {col} ={id}")
            self.conn.commit()
            self.cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e.__class__.__name__, ":", e)
            return False

    def user_search_blog(self, uid, keyword):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'select * from blog where title like "%{keyword}%" and uid = {uid}')
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    def admin_search_user(self, keyword, type):
        if type == 0:
            sqlstr = f"select * from user where mail like '%{keyword}% and status =0'"
        elif type == 1:
            sqlstr = f"select * from user where mail like '%{keyword}%' and report != 0 and status =0"
        else:
            sqlstr = f"select * from user where mail like '%{keyword}%' and status = 1"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sqlstr)
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None

    # 博客管理类型 0=正常博客搜索 1=受举报博客 2=已封禁博客
    def admin_search_blog(self, keyword, type):
        if type == 0:
            sqlstr = f"select * from blog where title like '%{keyword}%' and status != 2"
        elif type == 1:
            sqlstr = f"select * from blog where title like '%{keyword}%' and status != 2 and report !=0"
        else:
            sqlstr = f"select * from blog where title like '%{keyword}%' and status = 2"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sqlstr)
            li = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            return li
        except Exception as e:
            print(e.__class__.__name__, ":", e)
            return None


Sql = MysqlTool('root', '123456', '121.37.185.55', 3306, 'python')

"""
    dict项目 用于处理数据
"""
import pymysql
import hashlib
import time

# 编写功能类 提供给服务端使用
class Database:
    def __init__(self, host='0.0.0.0',
                 port=3306,
                 user='root',
                 passwd='Root@123',
                 database='dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset

        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库连接
    def close(self):
        self.db.close()
        self.cur.close()

    # 处理注册
    def register(self, name, passwd):
        sql = "select * from user where name='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False

        # 加密处理
        hash = hashlib.md5((name+"the-salt").encode())
        hash.update(passwd.encode())

        sql = "insert into user (name, passwd) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # 处理登陆
    def login(self, name, passwd):
        sql = "select * from user where name = %s and passwd = %s"
        # name + the-salt  --->盐
        hash = hashlib.md5((name + "the-salt").encode())
        hash.update(passwd.encode())
        self.cur.execute(sql, [name, hash.hexdigest()])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 插入历史纪录
    def insert_history(self, name, word):
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values (%s,%s,%s)"
        try:
            self.cur.execute(sql, [name, word, tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 单词查询
    def query(self, word):
        sql = "select mean from words where word = '%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    # 历史纪录
    def history(self, name):
        sql = "select name,word,time from hist where name='%s' order by id desc limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()

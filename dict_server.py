"""
    dict 服务端
    处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from operation_db import *
from time import sleep

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


def do_history(c, db, data):
    name = data.split(' ')[1]
    r = db.history(name)  # 返回元组
    if not r:
        c.send(b'FAIL')
        return
    c.send(b'OK')
    for i in r:
        # i ---> (name, word, time)
        msg = "%s\t%s\t\t%s" % i
        sleep(0.1)  # 防止粘包
        c.send(msg.encode())
    sleep(0.1)
    c.send(b'##')


# 处理登陆  data = L name passwd
def do_login(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


# 处理注册
def do_register(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')


# 处理客户端请求
def do_request(c, db):
    db.create_cursor()  # 生成游标 db.cur
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ':', data)
        if not data or data[0] == 'E':
            db.cur.close()
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, db, data)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_history(c, db, data)


def do_query(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    db.insert_history(name, word)  # 插入历史纪录

    mean = db.query(word)  # 查单词  如果没查到，返回none
    if not mean:
        c.send("没有找到该单词！".encode())
    else:
        c.send((word + ":" + mean).encode())


# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建TCP套接字
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port 8000...")
    while True:
        try:
            c, addr = sockfd.accept()
            print("Connect from", addr)

        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务器关闭")
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=do_request, args=(c, db))
        p.daemon = True  # 父进程结束，子进程也结束
        p.start()


if __name__ == '__main__':
    main()

"""
    dict 客户端
    发起请求，展示结果
"""
from socket import *
from getpass import getpass

ADDR = ('127.0.0.1', 8000)
sockfd = socket(AF_INET, SOCK_STREAM)
sockfd.connect(ADDR)


def do_history(name):
    msg = "H %s" % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while True:
            data = sockfd.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")


# 查单词
def do_query(name):
    while True:
        word = input("单词：")
        if word == "##":  # 结束单词查询
            break
        msg = "Q %s %s" % (name, word)
        sockfd.send(msg.encode())
        # 等待回复
        data = sockfd.recv(2048).decode()
        print(data)


# 二级界面
def login(name):
    while True:
        print("""
        ================= Quary =================
          1.查单词     2.历史纪录      3.退出登陆
        =========================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print("输入命令有误，请重新输入")


# 注册
def do_register():
    while True:
        name = input("UserName:")
        if ' ' in name:
            print("用户名不能有空格，请重新输入！")
            continue
        passwd = getpass()
        if ' ' in passwd:
            print("密码不能有空格，请重新输入！")
            continue
        passwd1 = getpass("Again:")
        if passwd != passwd1:
            print("两次密码不一致，请重新输入")
            continue

        msg = "R %s %s" % (name, passwd)
        # 发送请求
        sockfd.send(msg.encode())
        # 接收反馈
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


# 处理登陆
def do_login():
    name = input("UserName:")
    passwd = getpass()
    msg = "L %s %s" % (name, passwd)
    sockfd.send(msg.encode())
    # 接收反馈
    data = sockfd.recv(128).decode()
    if data == 'OK':
        print("登陆成功")
        login(name)
    else:
        print("登陆失败")
    return


# 创建网络连接
def main():
    while True:
        print("""
        =============== Welcome ===============
          1.注册         2.登录         3.退出
        =======================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            sockfd.send(b'E')
            print("谢谢使用!")
            return
        else:
            print("输入命令有误，请重新输入")


if __name__ == '__main__':
    main()

# english_dict
>>The first test of me

>Using for study mysql python socket TCP 
>Include dic_client dict_server insert_world operation_db and dict

>1.确定技术
    >>通信      TCP通信
    >>并发      多进程并发
    >>数据库     MySQL

>2.确定数据库：建立几个表，每个表作用和存储内容
    >>create database dict charset=utf8;
    >建表
    >存储用户   用户表 id  name   password
    >>create table user(id int primary key auto_increment,name varchar(32) not null,passwd varchar(128) not null);
    >历史记录         id  name   word    time
    >>create table hist(id int primary key auto_increment,name varchar(32) not null,word varchar(32) not null,time varchar(64) not null);
    >单词表           id  word   mead
    >>create table words(id int primary key auto_increment,word varchar(32),mean text);
    >编写程序将单词本存入数据库

>3.结构设计
    >>客户端
    >>服务端（处理数据）

>4.功能分析
    >>客户端和服务端分别需要实现哪些功能

    网络模型（并发模型）
    注册
        客户端  * 输入注册信息
               * 将信息发送给服务端
               * 等待反馈信息

        服务端  * 接收注册信息
               * 验证用户是否存在
               * 插入数据库
               * 将信息反馈给客户端

    登录
        客户端 * 输入登陆信息
              * 将信息发给服务器
              * 得到回复

        服务端 * 接收请求
              * 判断是否允许登陆
              * 反馈结果

    查单词
        客户端
              * 循环输入单词
              * 发送给服务器
              * 获取结果

        服务端
              * 接收请求
              * 查找单词
              * 将结果发送给服务端
              * 插入历史纪录

    历史记录
        客户端
              * 发送请求
              * 循环接收历史纪录

        服务端
              * 接收请求
              * 查询历史纪录
              * 发送历史纪录


>协议指定：
           >>注册  R  name   passwd
           >>登陆  L  name   passwd
           >>查词  Q  name   word
           >>历史  H  name



>cookie: import getpass

>>getpass.getpass()
>>功能：隐藏输入的内容
>>返回值：输入内容字符串


>cookie:
 >>import hashlib

>生成加密对象 参数为“盐”
 >>hash = hashlib.md5(("Levi"+"the-sat").encode())

>对密码进行算法加密
 >>hash.update(passwd.encode())

>获取加密后的密码字串
 >>hash.hexdigest()

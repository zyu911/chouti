#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Session类型：cache/redis/memcached
SESSION_TYPE = "redis"


# Session超时时间（秒）
SESSION_EXPIRES = 60*60*24*7

# 默认登录页面
LOGIN_URL = '/login'


# 数据库连接
PY_MYSQL_CONN_DICT = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "password": '123456',
    "db": 'choutidb',
    "charset": 'utf8'
}

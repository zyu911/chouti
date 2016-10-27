#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SESSION_TYPE = "redis"

SESSION_EXPIRES = 60*60*24*7

LOGIN_URL = '/login'


PY_MYSQL_CONN_DICT = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "password": '123456',
    "db": 'choutidb',
    "charset": 'utf8'
}

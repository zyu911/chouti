#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
from repository import chouti_orm as ORM


class DbConnection:

    def __init__(self):
        self.conn = ORM.session()

    def commit(self):
        self.conn.commit()

    def close(self):

        self.conn.close()
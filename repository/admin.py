#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import connection
from models.admin import IAdminRepository
from repository import chouti_orm as ORM


class AdminRepostiory(IAdminRepository):
    def __init__(self):
        self.db_conn = connection.DbConnection()

    def fetch_news(self):
        cursor = self.db_conn.connect()
        sql = """select * from news"""
        cursor.execute(sql)
        db_result = cursor.fetchall()

        self.db_conn.close()
        print(db_result)
        return db_result

    def show_new(self, nid):
        conn = ORM.session()
        conn.query(ORM.News).filter_by(nid=nid).update({"show": 1})
        conn.commit()
        conn.close()

    def hidden_new(self, nid):
        conn = ORM.session()
        conn.query(ORM.News).filter_by(nid=nid).update({"show": 0})
        conn.commit()
        conn.close()

    def show_or_hidden(self, nid):
        conn = ORM.session()
        obj = conn.query(ORM.News).filter_by(nid=nid).first()
        conn.close()
        return obj.show
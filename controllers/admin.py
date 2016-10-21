#!/usr/bin/env python
# -*- coding:utf-8 -*-
from backend.core.request_handler import BaseRequestHandler
from backend.utils.pager import Pagination
from models import chouti_orm as ORM
from sqlalchemy import and_, or_
import json
import time
from models.admin import AdminService
from repository.AdminRepository import AdminRepostiory


class AdminHandler(BaseRequestHandler):
    def get(self):
        self.render("admin/home/index.html")

    def post(self, *args, **kwargs):
        pass


class AdminUserHandler(BaseRequestHandler):
    def get(self):
        self.render('admin/home/index.html')

    def post(self):
        pass


class FindLover(BaseRequestHandler):
    def get(self):
        pass


class EditNews(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render("admin/home/edit_news.html")

    def post(self):
        ret = {'status': True, 'message': '', 'total': 0, 'rows': []}
        current_time = time.time()

        conn = ORM.session()
        all_count = conn.query(ORM.News).count()
        ret['total'] = all_count
        page = self.get_argument("page")
        rows = self.get_argument("rows")

        print(page, rows)

        news = AdminService(AdminRepostiory()).fetch_news()

        for i in news:
            # print(i.nid)
            ret['rows'].append({
                'nid': i['nid'],
                'url': i['url'],
                'title': i['title'],
                "ctime": str(i['ctime']),
                'content': i['content'],
                'favor_count': i['favor_count'],
                'comment_count': i['comment_count'],
                'show': '显示' if i['show'] else '隐藏'
            })

        print(ret)
        self.write(json.dumps(ret))

    def delete(self, *args, **kwargs):
        ret = {'status': False, 'rows': "", 'summary': ''}
        nid = self.get_argument("nid", None)
        print(nid, 'zyu')
        if nid:
            try:
                service = AdminService(AdminRepostiory())
                service.set_show(nid)

                service.show_or_hidden(nid)
            except IOError as E:
                ret['summary'] = str(E)
                print(ret)
                self.write(json.dumps(ret))

            ret['status'] = True
            self.write(json.dumps(ret))


class SetImg(BaseRequestHandler):
    def get(self):
        print("set_img.html")
        self.render('admin/home/set_img.html')
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from backend.di.Meta import DIMetaClass


class IAdminRepository(object):
    pass


class AdminService(metaclass=DIMetaClass):
    def __init__(self, admin_repository):  # 组合
        self.admin_repository = admin_repository

    def fetch_news(self):
        return self.admin_repository.fetch_news()

    def del_new(self, nid):
        return self.admin_repository.show_new(nid)

    def show_or_hidden(self, nid):
        return self.admin_repository.show_or_hidden(nid)

    def set_show(self, nid):
        info = self.admin_repository.show_or_hidden(nid)
        if info:
            self.admin_repository.hidden_new(nid)
        else:
            self.admin_repository.show_new(nid)
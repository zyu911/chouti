#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from backend import uimethods as mt
from controllers import home
from controllers import account
from controllers import admin
settings = {
    'template_path': 'views',
    'static_path': 'statics',
    'static_url_prefix': '/statics/',
    'autoreload': True,
    'ui_methods': mt
}

application = tornado.web.Application([
    (r"/index", home.IndexHandler),
    (r"/check_code", account.CheckCodeHandler),
    (r"/send_msg", account.SendMsgHandler),
    (r"/register", account.RegisterHandler),
    (r"/login", account.LoginHandler),
    (r"/upload_image", home.UploadImageHandler),
    (r"/comment", home.CommentHandler),
    (r"/favor", home.FavorHandler),

    (r"/publish_url", home.Publish_url),  # 查询url信息

    (r"/admin", admin.AdminHandler),
    (r"/admin_user", admin.AdminUserHandler),

    (r"/find_love", admin.FindLover),
    (r"/edit_news", admin.EditNews),
    (r"/set_img", admin.SetImg),

], **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
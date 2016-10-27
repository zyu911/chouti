#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import hashlib
import time
import copy
import datetime
import collections
from backend.utils.pager import Pagination
from backend.core.request_handler import BaseRequestHandler
from backend import commons
from forms.home import IndexForm
from forms.home import UrlForm
from forms.home import CommentForm
from backend.utils import decrator
from backend.utils.response import BaseResponse
from backend.utils.response import StatusCodeEnum
from sqlalchemy import and_, or_
import redis
from config import BASE_DIR
import shutil
from models.home import HomeServer
import repository.chouti_orm as ORM

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)


def cache(func):
    def inner(self, *args, **kwargs):
        ret = r.get('index')
        if ret:
            self.write(ret)
            return
        func(self, *args, **kwargs)
        r.set('index', self._response_html, ex=10)

    return inner


class IndexHandler(BaseRequestHandler):
    # @cache
    def get(self, page=1):
        current_time = time.time()
        all_count = HomeServer().count_news('all')

        obj = Pagination(page, all_count)
        # print(self.session)
        print(self.session['is_login'])
        print(self.session['user_info'], type(self.session['user_info']))
        current_user_id = self.session['user_info']['nid'] if self.session['is_login'] else 0

        result = HomeServer().all_news(current_user_id, obj.start, obj.end)
        # result = conn.query(ORM.News.nid,
        #                     ORM.News.title,
        #                     ORM.News.url,
        #                     ORM.News.content,
        #                     ORM.News.ctime,
        #                     ORM.UserInfo.username,
        #                     ORM.NewsType.caption,
        #                     ORM.News.favor_count,
        #                     ORM.News.comment_count,
        #                     ORM.News.news_type_id,
        #                     ORM.News.image,
        #                     ORM.Favor.nid.label('has_favor')).join(ORM.NewsType, isouter=True).join(ORM.UserInfo,
        #                                                                                             isouter=True).join(
        #     ORM.Favor, and_(ORM.Favor.user_info_id == current_user_id, ORM.News.nid == ORM.Favor.news_id),
        #     isouter=True)[obj.start:10]
        # conn.close()

        str_page = obj.string_pager('/index/')
        print(result)
        # self.write()
        self.render('home/index.html', str_page=str_page, news_list=result, current_time=current_time, cla=1)

    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        ret = {'status': False, "data": {}, 'summary': {}, "message": {}}
        form = IndexForm()
        if form.valid(self):
            # title,content,href,news_type,user_info_id
            input_dict = copy.deepcopy(form._value_dict)
            input_dict['ctime'] = datetime.datetime.now()
            input_dict['user_info_id'] = self.session['user_info']['nid']

            nid, new_type = HomeServer().save_news(**input_dict)
            nid = str(nid)

            if nid and new_type == 3:
                user_name = str(self.session['user_info']["username"])
                base_dir = os.path.join(BASE_DIR, 'zyu_chouti', "statics", "upload", user_name, nid)
                os.mkdir(base_dir)  # 新建当前微博Id对应的图片目录
                base_old_dir = os.path.join(BASE_DIR, "zyu_chouti", "statics", "upload", user_name, 'temp')
                image = None
                for i in os.listdir(base_old_dir):  # 移动文件到该目录
                    image = i
                    shutil.move(os.path.join(base_old_dir, i), base_dir)

                image = "/statics/upload/%s/%s/%s" % (user_name, nid, image)
                HomeServer().update_news_img(nid, image)  # 添加图标
                # 清空用户当前临时目录
                file_path = os.path.join(BASE_DIR, 'zyu_chouti', "statics", "upload", user_name, 'temp')
                files = os.listdir(file_path)  # 清空目录内容
                for i in files:
                    os.remove(os.path.join(file_path, i))
                print("清空文件夹")

            ret['status'] = True
        else:
            ret['status'] = False
            ret['message']['error'] = "标题是必须的"

        self.write(json.dumps(ret))


class UploadImageHandler(BaseRequestHandler):
    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        print("我到了!!!")
        rep = BaseResponse()
        try:
            file_metas = self.request.files["fafafa"]
            for meta in file_metas:
                file_name = meta['filename']
                xxx = file_name.split(".")[-1]
                username = self.session['user_info']["username"]
                file_path = os.path.join('statics', 'upload', username, 'temp',
                                         commons.generate_md5(file_name) + '.' + xxx)
                with open(file_path, 'wb') as up:
                    up.write(meta['body'])
            rep.status = True
            rep.data = file_path
        except Exception as ex:
            rep.summary = str(ex)
        self.write(json.dumps(rep.__dict__))


class CommentHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        # comment_list需要按照时间从小到大排列
        nid = self.get_argument('nid', 0)
        comment_list = HomeServer().obtain_comment(nid)
        """
        comment_list = [
            (1, '111',None),
            (2, '222',None),
            (3, '33',None),
            (9, '999',5),
            (4, '444',2),
            (5, '555',1),
            (6, '666',4),
            (7, '777',2),
            (8, '888',4),
        ]
        """

        comment_tree = commons.build_tree(comment_list)

        self.render('include/comment.html', comment_tree=comment_tree)

    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        print("评论!!!!!!")
        rep = BaseResponse()
        form = CommentForm()
        if form.valid(self):
            form._value_dict['ctime'] = datetime.datetime.now()

            conn = ORM.session()
            obj = ORM.Comment(user_info_id=self.session['user_info']['nid'],
                              news_id=form._value_dict['news_id'],
                              reply_id=form._value_dict['reply_id'],
                              content=form._value_dict['content'],
                              up=0,
                              down=0,
                              ctime=datetime.datetime.now())
            conn.add(obj)
            conn.flush()
            conn.refresh(obj)

            rep.data = {
                'user_info_id': self.session['user_info']['nid'],
                'username': self.session['user_info']['username'],
                'nid': obj.nid,
                'news_id': obj.news_id,
                'ctime': obj.ctime.strftime("%Y-%m-%d %H:%M:%S"),
                'reply_id': obj.reply_id,
                'content': obj.content,
            }

            conn.query(ORM.News).filter(ORM.News.nid == form._value_dict['news_id']).update(
                {"comment_count": ORM.News.comment_count + 1}, synchronize_session="evaluate")
            conn.commit()
            conn.close()

            rep.status = True
        else:
            rep.message = form._error_dict
        print(rep.__dict__)
        self.write(json.dumps(rep.__dict__))


class FavorHandler(BaseRequestHandler):
    @decrator.auth_login_json
    def post(self, *args, **kwargs):
        rep = BaseResponse()

        news_id = self.get_argument('news_id', None)
        if not news_id:
            rep.summary = "新闻ID不能为空."
        else:
            user_info_id = self.session['user_info']['nid']
            conn = ORM.session()
            has_favor = conn.query(ORM.Favor).filter(ORM.Favor.user_info_id == user_info_id,
                                                     ORM.Favor.news_id == news_id).count()
            if has_favor:
                conn.query(ORM.Favor).filter(ORM.Favor.user_info_id == user_info_id,
                                             ORM.Favor.news_id == news_id).delete()
                conn.query(ORM.News).filter(ORM.News.nid == news_id).update(
                    {"favor_count": ORM.News.favor_count - 1}, synchronize_session="evaluate")
                rep.code = StatusCodeEnum.FavorMinus
            else:
                conn.add(ORM.Favor(user_info_id=user_info_id, news_id=news_id, ctime=datetime.datetime.now()))
                conn.query(ORM.News).filter(ORM.News.nid == news_id).update(
                    {"favor_count": ORM.News.favor_count + 1}, synchronize_session="evaluate")
                rep.code = StatusCodeEnum.FavorPlus
            conn.commit()
            conn.close()

            rep.status = True

        self.write(json.dumps(rep.__dict__))


class Publish_url(BaseRequestHandler):
    def post(self):
        ret = {'status': False, "data": {}, 'summary': {}, "message": {}}
        form = UrlForm()
        if form.valid(self):
            import requests
            import re
            print('这是我的Url', form._value_dict['url'])
            # conn = ORM.session()
            # num = conn.query(ORM.News).filter(ORM.News.url == form._value_dict['url']).count()
            num = HomeServer().count_news(form._value_dict['url'])
            if not num:
                try:
                    txt = requests.get(form._value_dict['url'])
                    txt = txt.text
                    title = re.search(r'<title>(.*)</title>', txt)
                    content = re.search(r'<p>(\w*)</p>', txt)
                    image = re.findall(r'src="(http://\S*g|f$)', txt)
                    for i in image:
                        if len(i) > 50 and len(i) < 256:
                            image = i
                            break
                    else:
                        image = ''
                    print(len(image), image)
                    if title:
                        title = title.group(1)
                    else:
                        title = ''
                    if content:
                        content = content.group(1)
                    else:
                        content = ''
                    ret['status'] = True
                    ret['message'] = {
                        'url': form._value_dict['url'],
                        'title': title,
                        'content': content,
                        'image': image
                    }
                except IOError as E:
                    print(E, "-------->")
                    ret['status'] = False
                    ret['message']['error'] = 'url错误!无法找到该网页'
            else:
                ret['status'] = False
                ret['message']['error'] = '该url连接已经存在了'
        else:
            ret['status'] = False
            ret['message']['error'] = '无效URL!!'

        print(ret)
        return self.write(json.dumps(ret))


class Image(BaseRequestHandler):
    def get(self, num):
        print("图片")
        try:
            item = HomeServer().obtain_one_news(num)
            data = []
            if item.nid:
                print("有图片", item.nid)
                user_name = self.session['user_info']["username"]
                pic_list = os.path.join(BASE_DIR, 'zyu_chouti', "statics", "upload", user_name, str(item.nid))
                for pic_src in os.listdir(pic_list):
                    src = "/statics/upload/%s/%s/%s" % (user_name, str(item.nid), pic_src)
                    data.append(src)

            self.render("home/images.html", pic_list=data, item=item, cla=3)
        except Exception as E:
            print(E)
            self.redirect("/index/")


class Chat(BaseRequestHandler):
    def get(self, num):
        item = HomeServer().obtain_one_news(num)
        self.render("home/chat.html", item=item, cla=2)


class Images(BaseRequestHandler):
    def get(self, page):
        current_time = time.time()
        all_count = HomeServer().count_news(3)
        obj = Pagination(page, all_count)
        user_id = self.session['user_info']['nid'] if self.session['is_login'] else 0
        result = HomeServer().texts_server(user_id, 3, obj.start, obj.end)

        str_page = obj.string_pager('/index/')
        print(result)
        # self.write()
        self.render('home/index.html', str_page=str_page, news_list=result, current_time=current_time, cla=3)


class Texts(BaseRequestHandler):
    def get(self, page):
        current_time = time.time()
        all_count = HomeServer().count_news(2)
        obj = Pagination(page, all_count)
        user_id = self.session['user_info']['nid'] if self.session['is_login'] else 0

        result = HomeServer().texts_server(user_id, 2, obj.start, obj.end)
        str_page = obj.string_pager('/index/')
        print(result)
        self.render('home/index.html', str_page=str_page, news_list=result, current_time=current_time, cla=2)


class Logout(BaseRequestHandler):
    def get(self):
        self.session['is_login'] = False
        self.redirect('/index/')
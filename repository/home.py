from models.home import Ihome
from repository.connection import DbConnection
from repository import chouti_orm as ORM
from sqlalchemy import and_, or_


class HomeRepostiory(Ihome):
    def __init__(self):
        self.conn = ORM.session()

    def count_news(self, news_type='all'):
        if news_type == 'all':
            all_count = self.conn.query(ORM.News).filter().count()
        else:
            all_count = self.conn.query(ORM.News).filter(ORM.News.news_type_id == news_type).count()
        return all_count

    def count_url(self, url):
        num = self.conn.query(ORM.News).filter(ORM.News.url == url).count()
        return num

    def texts_repository(self, user_id, new_type, start, end):
        result = self.conn.query(ORM.News.nid,
                                 ORM.News.title,
                                 ORM.News.url,
                                 ORM.News.content,
                                 ORM.News.ctime,
                                 ORM.UserInfo.username,
                                 ORM.NewsType.caption,
                                 ORM.News.favor_count,
                                 ORM.News.comment_count,
                                 ORM.News.news_type_id,
                                 ORM.News.image,
                                 ORM.Favor.nid.label('has_favor')).join(
            ORM.NewsType, isouter=True).join(ORM.UserInfo, isouter=True).join(
            ORM.Favor, and_(ORM.Favor.user_info_id == user_id, ORM.News.nid == ORM.Favor.news_id),
            isouter=True).filter(ORM.News.news_type_id == new_type).order_by(ORM.News.ctime.desc())[start:end]
        self.conn.close()
        return result

    def obtain_one_news(self, nid):
        result = self.conn.query(ORM.News.nid,
                                 ORM.News.title,
                                 ORM.News.url,

                                 ORM.News.content,
                                 ORM.News.ctime,
                                 ORM.UserInfo.username,
                                 ORM.NewsType.caption,
                                 ORM.News.favor_count,
                                 ORM.News.comment_count,
                                 ORM.News.news_type_id,
                                 ORM.Favor.nid.label('has_favor')).join(ORM.NewsType, isouter=True).join(
            ORM.UserInfo, isouter=True).join(
            ORM.Favor, and_(ORM.Favor.user_info_id == 1, ORM.News.nid == ORM.Favor.news_id),
            isouter=True).filter(ORM.News.nid == nid).first()
        self.conn.close()
        return result

    def obtain_comment(self, nid):
        comment_list = self.conn.query(
            ORM.Comment.nid,
            ORM.Comment.content,
            ORM.Comment.reply_id,
            ORM.UserInfo.username,
            ORM.Comment.ctime,
            ORM.Comment.up,
            ORM.Comment.down,
            ORM.Comment.news_id
        ).join(ORM.UserInfo, isouter=True).filter(ORM.Comment.news_id == nid).all()

        return comment_list

    def save_news(self, **input_dict):
        obj2 = ORM.News(**input_dict)
        self.conn.add(obj2)
        self.conn.commit()
        nid, new_type = obj2.nid, obj2.news_type_id
        self.conn.close()
        return int(nid), new_type

    def update_news_img(self, nid, img):
        print("src", img)
        print(self.conn.query(ORM.News).filter(ORM.News.nid == nid).update({'image': img}))
        self.conn.query(ORM.News).filter(ORM.News.nid == nid).update({"image": img})
        self.conn.commit()
        self.conn.close()

    def all_news(self, user_id, start, end):
        result = self.conn.query(ORM.News.nid,
                                 ORM.News.title,
                                 ORM.News.url,
                                 ORM.News.content,
                                 ORM.News.ctime,
                                 ORM.UserInfo.username,
                                 ORM.NewsType.caption,
                                 ORM.News.favor_count,
                                 ORM.News.comment_count,
                                 ORM.News.news_type_id,
                                 ORM.News.image,
                                 ORM.Favor.nid.label('has_favor')).join(
            ORM.NewsType, isouter=True).join(ORM.UserInfo, isouter=True).join(
            ORM.Favor, and_(ORM.Favor.user_info_id == user_id, ORM.News.nid == ORM.Favor.news_id),
            isouter=True).order_by(ORM.News.ctime.desc())[start:end]

        return result

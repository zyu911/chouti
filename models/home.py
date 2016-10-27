from backend.di.Meta import DIMetaClass


class Ihome(object):
    def find_images(self, num):
        raise Exception("你不能执行此方法")

    def find_chat(self, num):
        raise Exception("你也不能执行此方法")


class HomeServer(metaclass=DIMetaClass):
    def __init__(self, home_repository):
        self.home_repository = home_repository

    def texts_server(self, user_id, new_type, start, end):
        return self.home_repository.texts_repository(user_id, new_type, start, end)

    def count_news(self, num):
        return self.home_repository.count_news(num)

    def count_url(self, url):
        return self.home_repository.count_url(url)

    def obtain_one_news(self, nid):
        return self.home_repository.obtain_one_news(nid)

    def obtain_comment(self, nid):
        return self.home_repository.obtain_comment(nid)

    def save_news(self, **input_dict):
        return self.home_repository.save_news(**input_dict)

    def update_news_img(self, user_name, img):
        self.home_repository.update_news_img(user_name, img)

    def all_news(self, user_id, start, end):
        return self.home_repository.all_news(user_id, start, end)
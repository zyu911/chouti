from models.account import IAccount
from repository.connection import DbConnection
from repository import chouti_orm as ORM
from sqlalchemy import and_, or_


class AccountRepostiory(IAccount):
    def __init__(self):
        self.conn = ORM.session()

    def login(self, user_name, email, pwd):
        obj = self.conn.query(ORM.UserInfo).filter(
            or_(
                and_(ORM.UserInfo.email == user_name,
                     ORM.UserInfo.password == pwd),
                and_(ORM.UserInfo.username == email,
                     ORM.UserInfo.password == pwd)
            )).first()
        self.conn.close()
        return obj
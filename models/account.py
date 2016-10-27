from backend.di.Meta import DIMetaClass

class IAccount:
    pass


class AccountServer(metaclass=DIMetaClass):
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def loginHandel(self, user_name, email, pwd):
        return self.account_repository.login(user_name, email, pwd)


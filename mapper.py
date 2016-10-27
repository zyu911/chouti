from backend.di.Meta import DIMapper

from models.admin import AdminService
from repository.admin import AdminRepostiory

from models.home import HomeServer
from repository.home import HomeRepostiory

from models.account import AccountServer
from repository.account import AccountRepostiory

DIMapper.inject(AdminService, AdminRepostiory())
DIMapper.inject(HomeServer, HomeRepostiory())
DIMapper.inject(AccountServer, AccountRepostiory())


#coding:utf-8
from apps.api.common import BaseHandler
from lib.routes import route
from bson import ObjectId
from login_handler import login
from settings import PAGE_LIMIT


@route('/manager/index')
class IndexHandler(BaseHandler):
    @login()
    def get(self):
        return self.write_json({'errno': 0, 'msg': 'success'})


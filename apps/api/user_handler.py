#coding:utf-8
from hashlib import md5
from bson import ObjectId
from apps.api.common import BaseHandler
from lib.routes import route
from apps.api.utils import auth_decorator



@route('/api/login')
class ApiLogin(BaseHandler):
    '''login api'''
    def get(self):
        return self.write_json({'errno': 0, 'msg': 'success'})
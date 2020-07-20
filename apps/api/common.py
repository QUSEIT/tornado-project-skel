#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, datetime
import settings
import json
from bson import ObjectId
try:
    import ujson as json
except ImportError:
    import json
from urllib.parse import urlparse
import urllib
import math
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import tornado.web
from settings import PAGE_LIMIT


class BareboneHandler(tornado.web.RequestHandler):
    """底层的handler 用以解决各个资源组件连接"""
    def __init__(self, application, request, **kwargs):
        #处理
        super(BareboneHandler, self).__init__(application, request, **kwargs)
        if request.headers.get("cdn-src-ip", None):
            request.remote_ip = request.headers["cdn-src-ip"]
        elif request.headers.get("X-Forwarded-For", None):
            try:
                request.remote_ip = request.headers["X-Forwarded-For"].split(",")[0]
            except Exception as e:
                print(e)
        
    @property
    def db(self):
        return self.application.con[settings.DATABASE_NAME]

    @property
    def huanxin(self):
        return self.application.huanxin

    @property
    def redis(self):
        return self.application.redis

    @property
    def log(self):
        return self.application.log
    
    def write_json(self, obj):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.make_str_id(obj))

    def make_str_id(self, obj):
        if type(obj) is dict:
            return {k: self.make_str_id(v) for k, v in obj.items()}
        if type(obj) is list:
            return [self.make_str_id(i) for i in obj]
        if type(obj) in [int, float]:
            return obj
        return str(obj)


    def pagination(self, num, page):
        # TODO 搜索后的分页跳转会清掉s=xx
        page_num = num/PAGE_LIMIT + (not (not num%PAGE_LIMIT))
        page_list = range(page_num)[page-3 if page-3 >=0 else 0:page+3 if page+3 <= page_num else page_num]
        page_list = [str(x+1) for x in page_list]
        if '1' not in page_list:
            page_list = (['1'] if '2' in page_list else ['1', '...']) + page_list
        if str(page_num) not in page_list:
            page_list = page_list + ([str(page_num)] if str(page_num - 1) in page_list else ['...', str(page_num)])
        return self.render_string("pagination.html", **{
            'num': num,
            'page': page,
            'page_num': page_num,
            'page_list': page_list
        })


class BaseHandler(BareboneHandler):
    """基础handler 类"""

    def send_log(self, *args):
        """发送日志，后台记录"""
        try:
            self.log.publish(settings.NAMESPACE, ",".join(map(str, args)))
        except ConnectionError as e:
            print("send_log error", args, e)

class MaintainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write({"error": 1, "msg": "We are busy updating the server for you and will be back shortly.\n"
                                       "我們正忙著為您更新服務器，馬上回來。\n"
                                       "私たちはあなたのために、サーバーを更新忙しく、すぐに戻ってくる。\n"
                                       "เราจะยุ่งปรับปรุงเซิร์ฟเวอร์สำหรับคุณและจะกลับมาในไม่ช้า"})

    def post(self, *args, **kwargs):
        self.get()

    def delete(self, *args, **kwargs):
        self.get()


class SimpleException(Exception):
    """基本异常类"""
    __data = ""
    def __init__(self, data):
        self.__data = data

    def __str__(self):  # 相当于 str(#)
        return self.__data

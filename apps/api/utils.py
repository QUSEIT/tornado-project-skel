#coding: utf-8
from functools import wraps
from tornado.web import HTTPError
from bson import ObjectId
from hashlib import md5
import time, os
import settings
import pickle
from datetime import datetime
import Geohash
import redis


def generate_access_token(user_id):
    raw_string = str(user_id) + "quseit_application_for_qutao"
    return md5(raw_string).hexdigest()


def generate_geohash(lng_lat):
	#生成 Geohash
	#5位长度：2.4km
	#6位长度：0.61km
	#7位长度：0.076
	#8位长度：0.01911
	#9：0.00478
    lng, lat = lng_lat.split(',')
    return Geohash.encode(float(lat), float(lng), 6)


def auth_decorator(method):

    """
    auth验证装饰器
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        access_token = self.get_argument("access_token", "").strip()
        user_id = self.get_argument("id", "").strip()
        
        if not access_token or not user_id or generate_access_token(user_id) != access_token:
            raise HTTPError(500, "Error. invalid user!")

        return method(self, *args, **kwargs)

    return wrapper


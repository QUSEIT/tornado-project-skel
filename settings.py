#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import platform
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
PIC_PATH = os.path.join(ROOT, 'static/')
HOST = ''
API_PORT = 10000

#server is in mataining ?
IS_MAINTAIN = False
IS_DEV = False

REVIEW_ADMIN = ['admin']
REVIEW_PASSWOED = ['admin']

LOGGING_LEVEL = logging.DEBUG
DEBUG = True

#db
DATABASE_NAME = "db_name"
DB_REPLICA_SET_HOST = "localhost"
DB_REPLICA_SET_PORT= 27017
DB_REPLICA_SET_NAME = "qprs0"

#redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_POOL = 0

#启动的app
APPS = ("api",
        "backend")

PAGE_LIMIT = 20

#图片地址
STATIC_DIR = os.path.join(HOST, 'static/')

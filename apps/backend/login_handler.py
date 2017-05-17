#!/usr/bin/env python
# coding:utf-8
import urllib
from apps.api.common import BaseHandler
from lib.routes import route
import settings


def login():
    def wrap(view_func):
        def is_login(self, *args, **kwargs):
            self.me = self.get_secure_cookie("user_name")
            if self.request.method == "GET" and not self.me:
                url = "/login"
                if self.request.uri.count("next") > 3:
                    return self.redirect(url)
                if "?" not in url:
                    url += "?" + urllib.urlencode(dict(next=self.request.uri))
                return self.redirect(url)
            return view_func(self, *args, **kwargs)
        return is_login
    return wrap


@route('/login')
class LoginHandler(BaseHandler):

    def get(self):
        if self.get_secure_cookie("user_name"):
            return self.redirect('/manager/index')
        return self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        remember = self.get_argument("remember", '')
        if username in settings.REVIEW_ADMIN and password in settings.REVIEW_PASSWOED:
            if remember == '1':
                self.set_secure_cookie("user_name", username, expires_days=365)
            else:
                self.set_secure_cookie("user_name", username, expires_days=1)
            return self.redirect('/manager/index')
        else:
            return self.redirect('/login')


@route('/login_out')
class LoginOutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user_name", '', expires_days=365)
        return self.redirect('/login')

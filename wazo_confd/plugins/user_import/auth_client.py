# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from werkzeug.local import LocalProxy as Proxy

from flask import g

from wazo_auth_client import Client as AuthClient

auth_config = {}


class AuthClientProxy(AuthClient):
    def __init__(self, *args, **kwargs):
        super(AuthClientProxy, self).__init__(*args, **kwargs)
        self.users_created = []
        # 30 minutes should be enought to import all users
        token = self.token.new(expiration=30 * 60)['token']
        self.set_token(token)

    def new_user(self, *args, **kwargs):
        user = self.users.new(*args, **kwargs)
        self.users_created.append(user)
        return user

    def edit_user(self, *args, **kwargs):
        # rollback system can be added here
        self.users.edit(*args, **kwargs)

    def rollback(self):
        for user in self.users_created:
            self.users.delete(user['uuid'])


def get_auth_client():
    client = g.get('auth_client_user_import')
    if not client:
        client = g.auth_client_user_import = AuthClientProxy(**auth_config)
    return client


def set_auth_client_config(config):
    global auth_config
    auth_config = config


auth_client = Proxy(get_auth_client)

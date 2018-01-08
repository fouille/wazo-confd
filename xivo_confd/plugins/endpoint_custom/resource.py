# -*- coding: UTF-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import url_for

from xivo_dao.alchemy.usercustom import UserCustom as Custom

from xivo_confd.auth import required_acl
from xivo_confd.helpers.restful import ListResource, ItemResource

from .schema import CustomSchema


class CustomList(ListResource):

    model = Custom
    schema = CustomSchema

    def build_headers(self, custom):
        return {'Location': url_for('endpoint_custom', id=custom.id, _external=True)}

    @required_acl('confd.endpoints.custom.read')
    def get(self):
        return super(CustomList, self).get()

    @required_acl('confd.endpoints.custom.create')
    def post(self):
        return super(CustomList, self).post()


class CustomItem(ItemResource):

    schema = CustomSchema

    @required_acl('confd.endpoints.custom.{id}.read')
    def get(self, id):
        return super(CustomItem, self).get(id)

    @required_acl('confd.endpoints.custom.{id}.update')
    def put(self, id):
        return super(CustomItem, self).put(id)

    @required_acl('confd.endpoints.custom.{id}.delete')
    def delete(self, id):
        return super(CustomItem, self).delete(id)

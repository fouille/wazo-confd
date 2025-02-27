# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request

from wazo_confd.auth import required_acl
from wazo_confd.helpers.restful import ConfdResource

from .schema import GroupFallbackSchema


class GroupFallbackList(ConfdResource):

    schema = GroupFallbackSchema

    def __init__(self, service, group_dao):
        super(GroupFallbackList, self).__init__()
        self.service = service
        self.group_dao = group_dao

    @required_acl('confd.groups.{group_id}.fallbacks.read')
    def get(self, group_id):
        group = self.group_dao.get(group_id)
        return self.schema().dump(group.fallbacks)

    @required_acl('confd.groups.{group_id}.fallbacks.update')
    def put(self, group_id):
        group = self.group_dao.get(group_id)
        fallbacks = self.schema().load(request.get_json())
        self.service.edit(group, fallbacks)
        return '', 204

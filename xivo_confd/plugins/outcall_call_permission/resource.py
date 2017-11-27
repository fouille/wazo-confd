# -*- coding: UTF-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_confd.authentication.confd_auth import required_acl
from xivo_confd.helpers.restful import ConfdResource


class OutcallCallPermissionAssociation(ConfdResource):

    def __init__(self, service, outcall_dao, call_permission_dao):
        super(OutcallCallPermissionAssociation, self).__init__()
        self.service = service
        self.outcall_dao = outcall_dao
        self.call_permission_dao = call_permission_dao

    @required_acl('confd.outcalls.{outcall_id}.callpermissions.{call_permission_id}.update')
    def put(self, outcall_id, call_permission_id):
        outcall = self.outcall_dao.get(outcall_id)
        call_permission = self.call_permission_dao.get(call_permission_id)
        self.service.associate(outcall, call_permission)
        return '', 204

    @required_acl('confd.outcalls.{outcall_id}.callpermissions.{call_permission_id}.delete')
    def delete(self, outcall_id, call_permission_id):
        outcall = self.outcall_dao.get(outcall_id)
        call_permission = self.call_permission_dao.get(call_permission_id)
        self.service.dissociate(outcall, call_permission)
        return '', 204

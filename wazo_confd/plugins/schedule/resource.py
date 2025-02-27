# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import url_for

from xivo_dao.alchemy.schedule import Schedule

from wazo_confd.auth import required_acl
from wazo_confd.helpers.restful import ListResource, ItemResource

from .schema import ScheduleSchema


class ScheduleList(ListResource):

    model = Schedule
    schema = ScheduleSchema

    def build_headers(self, schedule):
        return {'Location': url_for('schedules', id=schedule.id, _external=True)}

    @required_acl('confd.schedules.create')
    def post(self):
        return super(ScheduleList, self).post()

    @required_acl('confd.schedules.read')
    def get(self):
        return super(ScheduleList, self).get()


class ScheduleItem(ItemResource):

    schema = ScheduleSchema
    has_tenant_uuid = True

    @required_acl('confd.schedules.{id}.read')
    def get(self, id):
        return super(ScheduleItem, self).get(id)

    @required_acl('confd.schedules.{id}.update')
    def put(self, id):
        return super(ScheduleItem, self).put(id)

    @required_acl('confd.schedules.{id}.delete')
    def delete(self, id):
        return super(ScheduleItem, self).delete(id)

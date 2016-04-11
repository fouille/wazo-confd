# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from flask import request
from flask_restful import abort
from marshmallow import Schema, fields, pre_dump

from xivo_confd.authentication.confd_auth import required_acl
from xivo_confd.helpers.restful import ConfdResource


class BaseSchema(Schema):
    def handle_error(self, error, data):
        # Format the error message to have the same behavior as flask-restful
        error_msg = {key: value[0] for key, value in error.message.iteritems()}
        return abort(400, message=error_msg)


class StrictBoolean(fields.Boolean):

    def _deserialize(self, value, attr, data):
        if not isinstance(value, bool):
            self.fail('invalid')
        return value


class UserSubResource(ConfdResource):

    def __init__(self, service):
        self.service = service

    def get(self, user_id):
        user = self.service.get(user_id)
        return self.schema.dump(user).data

    def put(self, user_id):
        user = self.service.get(user_id)
        self.parse_and_update(user)
        return '', 204

    def parse_and_update(self, model):
        form = self.schema.load(request.get_json()).data
        for name, value in form.iteritems():
            setattr(model, name, value)
        self.service.edit(model, self.schema)


class ServiceDNDSchema(BaseSchema):
    enabled = StrictBoolean(attribute='dnd_enabled', required=True)

    types = ['dnd']


class ServiceIncallFilterSchema(BaseSchema):
    enabled = StrictBoolean(attribute='incallfilter_enabled', required=True)

    types = ['incallfilter']


class ServicesSchema(BaseSchema):
    dnd = fields.Nested(ServiceDNDSchema)
    incallfilter = fields.Nested(ServiceIncallFilterSchema)

    @pre_dump()
    def add_envelope(self, data):
        return {'dnd': data,
                'incallfilter': data}


class UserServiceDND(UserSubResource):

    schema = ServiceDNDSchema()

    @required_acl('confd.users.{user_id}.services.dnd.read')
    def get(self, user_id):
        return super(UserServiceDND, self).get(user_id)

    @required_acl('confd.users.{user_id}.services.dnd.update')
    def put(self, user_id):
        return super(UserServiceDND, self).put(user_id)


class UserServiceIncallFilter(UserSubResource):

    schema = ServiceIncallFilterSchema()

    @required_acl('confd.users.{user_id}.services.dnd.read')
    def get(self, user_id):
        return super(UserServiceIncallFilter, self).get(user_id)

    @required_acl('confd.users.{user_id}.services.dnd.update')
    def put(self, user_id):
        return super(UserServiceIncallFilter, self).put(user_id)


class UserServiceList(UserSubResource):

    schema = ServicesSchema()

    @required_acl('confd.users.{user_id}.services.read')
    def get(self, user_id):
        return super(UserServiceList, self).get(user_id)


class ForwardBusySchema(BaseSchema):
    enabled = StrictBoolean(attribute='busy_enabled', falsy=set((False,)), truthy=set((True,)))
    destination = fields.String(attribute='busy_destination', allow_none=True)

    types = ['busy']


class ForwardNoAnswerSchema(BaseSchema):
    enabled = StrictBoolean(attribute='noanswer_enabled')
    destination = fields.String(attribute='noanswer_destination', allow_none=True)

    types = ['noanswer']


class ForwardUnconditionalSchema(BaseSchema):
    enabled = StrictBoolean(attribute='unconditional_enabled')
    destination = fields.String(attribute='unconditional_destination', allow_none=True)

    types = ['unconditional']


class ForwardsSchema(BaseSchema):
    busy = fields.Nested(ForwardBusySchema)
    noanswer = fields.Nested(ForwardNoAnswerSchema)
    unconditional = fields.Nested(ForwardUnconditionalSchema)

    @pre_dump
    def add_envelope(self, data):
        return {'busy': data,
                'noanswer': data,
                'unconditional': data}


class UserForwardBusy(UserSubResource):

    schema = ForwardBusySchema()

    @required_acl('confd.users.{user_id}.forwards.busy.read')
    def get(self, user_id):
        return super(UserForwardBusy, self).get(user_id)

    @required_acl('confd.users.{user_id}.forwards.busy.update')
    def put(self, user_id):
        return super(UserForwardBusy, self).put(user_id)


class UserForwardNoAnswer(UserSubResource):

    schema = ForwardNoAnswerSchema()

    @required_acl('confd.users.{user_id}.forwards.noanswer.read')
    def get(self, user_id):
        return super(UserForwardNoAnswer, self).get(user_id)

    @required_acl('confd.users.{user_id}.forwards.noanswer.update')
    def put(self, user_id):
        return super(UserForwardNoAnswer, self).put(user_id)


class UserForwardUnconditional(UserSubResource):

    schema = ForwardUnconditionalSchema()

    @required_acl('confd.users.{user_id}.forwards.unconditional.read')
    def get(self, user_id):
        return super(UserForwardUnconditional, self).get(user_id)

    @required_acl('confd.users.{user_id}.forwards.unconditional.update')
    def put(self, user_id):
        return super(UserForwardUnconditional, self).put(user_id)


class UserForwardList(UserSubResource):

    schema = ForwardsSchema()

    @required_acl('confd.users.{user_id}.forwards.read')
    def get(self, user_id):
        return super(UserForwardList, self).get(user_id)

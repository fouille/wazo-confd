# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request

from wazo_confd.auth import required_acl
from wazo_confd.helpers.mallow import BaseSchema, StrictBoolean
from wazo_confd.helpers.restful import ConfdResource


class LiveReloadSchema(BaseSchema):
    enabled = StrictBoolean(required=True)


class LiveReloadResource(ConfdResource):

    schema = LiveReloadSchema

    def __init__(self, service):
        super(LiveReloadResource, self).__init__()
        self.service = service

    @required_acl('confd.configuration.live_reload.read')
    def get(self):
        model = self.service.get()
        return self.schema().dump(model)

    @required_acl('confd.configuration.live_reload.update')
    def put(self):
        form = self.schema().load(request.get_json())
        self.service.edit(form)
        return '', 204

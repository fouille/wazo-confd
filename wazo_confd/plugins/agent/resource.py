# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import url_for

from xivo_dao.alchemy.agentfeatures import AgentFeatures as Agent

from wazo_confd.auth import required_acl
from wazo_confd.helpers.restful import ListResource, ItemResource

from .schema import AgentSchema, AgentSchemaPUT


class AgentList(ListResource):

    model = Agent
    schema = AgentSchema

    def build_headers(self, agent):
        return {'Location': url_for('agents', id=agent.id, _external=True)}

    @required_acl('confd.agents.create')
    def post(self):
        return super(AgentList, self).post()

    @required_acl('confd.agents.read')
    def get(self):
        return super(AgentList, self).get()


class AgentItem(ItemResource):

    schema = AgentSchemaPUT
    has_tenant_uuid = True

    @required_acl('confd.agents.{id}.read')
    def get(self, id):
        return super(AgentItem, self).get(id)

    @required_acl('confd.agents.{id}.update')
    def put(self, id):
        return super(AgentItem, self).put(id)

    @required_acl('confd.agents.{id}.delete')
    def delete(self, id):
        return super(AgentItem, self).delete(id)

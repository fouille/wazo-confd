# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .resource import RegisterSIPItem, RegisterSIPList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            RegisterSIPList, '/registers/sip', resource_class_args=(service,)
        )

        api.add_resource(
            RegisterSIPItem,
            '/registers/sip/<int:id>',
            endpoint='register_sip',
            resource_class_args=(service,),
        )

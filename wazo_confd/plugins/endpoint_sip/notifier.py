# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.endpoint_sip.event import (
    CreateSipEndpointEvent,
    DeleteSipEndpointEvent,
    EditSipEndpointEvent,
)

from wazo_confd import bus, sysconfd


class SipEndpointNotifier:
    def __init__(self, sysconfd, bus):
        self.sysconfd = sysconfd
        self.bus = bus

    def send_sysconfd_handlers(self):
        handlers = {
            'ipbx': ['module reload res_pjsip.so', 'dialplan reload'],
            'agentbus': [],
        }
        self.sysconfd.exec_request_handlers(handlers)

    def created(self, line):
        event = CreateSipEndpointEvent(line.id)
        self.bus.send_bus_event(event)

    def edited(self, line):
        self.send_sysconfd_handlers()
        event = EditSipEndpointEvent(line.id)
        self.bus.send_bus_event(event)

    def deleted(self, line):
        self.send_sysconfd_handlers()
        event = DeleteSipEndpointEvent(line.id)
        self.bus.send_bus_event(event)


def build_notifier():
    return SipEndpointNotifier(sysconfd, bus)

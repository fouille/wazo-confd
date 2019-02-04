# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from mock import patch, Mock
from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_items,
)

from .._sysconfd import SysconfdPublisher


class TestSysconfdClient(TestCase):

    def setUp(self):
        self.dao = Mock()
        self.url = "http://localhost:8668"
        self.client = SysconfdPublisher(self.url, self.dao)
        session_init_patch = patch('xivo_confd._sysconfd.requests.Session')
        session_init = session_init_patch.start()
        self.session = session_init.return_value
        self.addCleanup(session_init.stop)

    def test_delete_voicemail_storage(self):
        self.session.request.return_value = Mock(status_code=200)

        self.client.delete_voicemail("123", "default")
        self.client.flush()

        url = "http://localhost:8668/delete_voicemail"
        self.session.request.assert_called_once_with('GET',
                                                     url,
                                                     params={'mailbox': '123', 'context': 'default'})

    def test_commonconf_generate(self):
        self.session.request.return_value = Mock(status_code=200)

        self.client.commonconf_generate()
        self.client.flush()

        url = "http://localhost:8668/commonconf_generate"
        self.session.request.assert_called_once_with('POST', url, json={})

    def test_commonconf_apply(self):
        self.session.request.return_value = Mock(status_code=200)

        self.client.commonconf_apply()
        self.client.flush()

        url = "http://localhost:8668/commonconf_apply"
        self.session.request.assert_called_once_with('GET', url)

    def test_xivo_service_start(self):
        self.session.request.return_value = Mock(status_code=200)
        expected_json = {'wazo-service': 'start'}

        self.client.xivo_service_start()
        self.client.flush()

        method, url, json = self.extract_request()
        expected_url = "http://localhost:8668/xivoctl"
        self.assertEquals(method, "POST")
        self.assertEquals(url, expected_url)
        self.assertEquals(json, expected_json)

    def test_xivo_service_enable(self):
        self.session.request.return_value = Mock(status_code=200)
        expected_json = {'wazo-service': 'enable'}

        self.client.xivo_service_enable()
        self.client.flush()

        method, url, json = self.extract_request()
        expected_url = "http://localhost:8668/xivoctl"
        self.assertEquals(method, "POST")
        self.assertEquals(url, expected_url)
        self.assertEquals(json, expected_json)

    def test_set_hosts(self):
        self.session.request.return_value = Mock(status_code=200)
        expected_json = {'hostname': 'toto',
                         'domain': 'toto.tata.titi'}

        self.client.set_hosts(expected_json['hostname'], expected_json['domain'])
        self.client.flush()

        method, url, json = self.extract_request()
        expected_url = "http://localhost:8668/hosts"
        self.assertEquals(method, "POST")
        self.assertEquals(url, expected_url)
        self.assertEquals(json, expected_json)

    def test_set_resolvconf(self):
        self.session.request.return_value = Mock(status_code=200)
        domain = 'toto.titi.tata'
        expected_json = {'nameservers': ['127.0.0.1'],
                         'search': [domain]}

        self.client.set_resolvconf(expected_json['nameservers'], domain)
        self.client.flush()

        method, url, json = self.extract_request()
        expected_url = "http://localhost:8668/resolv_conf"
        self.assertEquals(method, "POST")
        self.assertEquals(url, expected_url)
        self.assertEquals(json, expected_json)

    def test_move_voicemail_storage(self):
        self.session.request.return_value = Mock(status_code=200)

        self.client.move_voicemail("100", "default", "2000", "newcontext")
        self.client.flush()

        url = "http://localhost:8668/move_voicemail"
        params = {'old_mailbox': '100',
                  'old_context': 'default',
                  'new_mailbox': '2000',
                  'new_context': 'newcontext'}
        self.session.request.assert_called_once_with('GET',
                                                     url,
                                                     params=params)

    def test_exec_request_handlers_live_reload_enabled(self):
        self.session.request.return_value = Mock(status_code=200)
        self.dao.is_live_reload_enabled.return_value = True

        commands = {'ctibus': (),
                    'ipbx': ()}

        self.client.exec_request_handlers(commands)
        self.client.flush()

        method, url, json = self.extract_request()

        expected_url = "http://localhost:8668/exec_request_handlers"
        self.assertEquals(method, "POST")
        self.assertEquals(url, expected_url)
        self.assertEquals(json, commands)

        self.dao.is_live_reload_enabled.assert_called_once_with()

    def extract_request(self):
        call = self.session.request.call_args_list[0]
        method = call[0][0]
        url = call[0][1]
        json = call[1]['json']
        return method, url, json

    def test_exec_request_handlers_live_reload_disabled(self):
        self.dao.is_live_reload_enabled.return_value = False

        commands = {'ctibus': [],
                    'ipbx': []}

        self.client.exec_request_handlers(commands)
        self.client.flush()

        self.assertFalse(self.session.request.called)
        self.dao.is_live_reload_enabled.assert_called_once_with()

    def test_exec_request_handlers_merges_commands_sent(self):
        self.session.request.return_value = Mock(status_code=200)
        self.dao.is_live_reload_enabled.return_value = True

        self.client.exec_request_handlers({'ctibus': ['command1'],
                                           'ipbx': ['command2']})
        self.client.exec_request_handlers({'ctibus': ['command1', 'command3', 'command4'],
                                           'ipbx': ['command5'],
                                           'bus': ['command6']})
        self.client.flush()

        method, url, json = self.extract_request()

        expected_url = "http://localhost:8668/exec_request_handlers"
        expected_body = has_entries(ctibus=has_items('command1', 'command3', 'command4'),
                                    ipbx=has_items('command2', 'command5'),
                                    bus=has_items('command6'))

        assert_that(method, equal_to("POST"))
        assert_that(url, equal_to(expected_url))
        assert_that(json, expected_body)

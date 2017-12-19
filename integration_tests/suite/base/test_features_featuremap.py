# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, has_entries

from ..helpers import scenarios as s
from . import confd


def test_put_errors():
    url = confd.asterisk.features.featuremap.put
    for check in error_checks(url):
        yield check


def error_checks(url):
    yield s.check_bogus_field_returns_error, url, 'options', 123
    yield s.check_bogus_field_returns_error, url, 'options', None
    yield s.check_bogus_field_returns_error, url, 'options', 'string'
    yield s.check_bogus_field_returns_error, url, 'options', [['ordered', 'option']]
    yield s.check_bogus_field_returns_error, url, 'options', {'wrong_value': 23}
    yield s.check_bogus_field_returns_error, url, 'options', {'none_value': None}


def test_get():
    response = confd.asterisk.features.featuremap.get()
    response.assert_ok()


def test_edit_features_featuremap():
    parameters = {'options': {'nat': 'toto',
                              'username': 'Bob'}}

    response = confd.asterisk.features.featuremap.put(**parameters)
    response.assert_updated()

    response = confd.asterisk.features.featuremap.get()
    assert_that(response.item, has_entries(parameters))


def test_edit_features_featuremap_with_no_option():
    parameters = {'options': {}}
    response = confd.asterisk.features.featuremap.put(**parameters)
    response.assert_updated()

    response = confd.asterisk.features.featuremap.get()
    assert_that(response.item, has_entries(parameters))


def test_bus_event_when_edited():
    url = confd.asterisk.features.featuremap
    yield s.check_bus_event, 'config.features_featuremap.edited', url.put, {'options': {}}

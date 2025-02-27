# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from . import confd


def add_sip(wazo_tenant=None, **params):
    response = confd.endpoints.sip.post(params, wazo_tenant=wazo_tenant)
    return response.item


def delete_sip(sip_id, check=False):
    response = confd.endpoints.sip(sip_id).delete()
    if check:
        response.assert_ok()


def generate_sip(**params):
    return add_sip(**params)

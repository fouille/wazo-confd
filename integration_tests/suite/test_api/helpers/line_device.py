# -*- coding: UTF-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from contextlib import contextmanager

from test_api.database import create_helper


def associate(line_id, device_id):
    database = create_helper()
    with database.queries() as queries:
        queries.associate_line_device(line_id, device_id)


def dissociate(line_id, device_id):
    database = create_helper()
    with database.queries() as queries:
        queries.dissociate_line_device(line_id, device_id)


@contextmanager
def line_and_device_associated(line, device):
    associate(line['id'], device['id'])
    yield
    dissociate(line['id'], device['id'])

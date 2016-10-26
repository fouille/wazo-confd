# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
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


from marshmallow import fields
from marshmallow.validate import OneOf, Length

from xivo_confd.helpers.destination import DestinationField
from xivo_confd.helpers.mallow import BaseSchema, Link, ListLink


class IncallSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    preprocess_subroutine = fields.String(validate=Length(max=39))
    caller_id_mode = fields.String(validate=OneOf(['prepend', 'overwrite', 'append']), allow_none=True)
    caller_id_name = fields.String(validate=Length(max=80), allow_none=True)
    description = fields.String(allow_none=True)
    destination = DestinationField(required=True)
    links = ListLink(Link('incalls'))
    extensions = fields.Nested('ExtensionSchema',
                               only=['id', 'exten', 'context', 'links'],
                               many=True,
                               dump_only=True)

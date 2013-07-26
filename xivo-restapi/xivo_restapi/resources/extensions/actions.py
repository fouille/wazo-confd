# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import logging

from flask import Blueprint, url_for
from flask.globals import request
from flask.helpers import make_response
from xivo_dao.data_handler.extension import services as extension_services
from xivo_dao.data_handler.extension.model import Extension
from xivo_restapi.resources.extensions import mapper
from xivo_restapi.helpers import serializer
from xivo_dao.helpers.provd_connector import ProvdError
from xivo_dao.helpers.sysconfd_connector import SysconfdError
from xivo_restapi.helpers.route_generator import RouteGenerator
from xivo_restapi import config


logger = logging.getLogger(__name__)
blueprint = Blueprint('extensions', __name__, url_prefix='/%s/extensions' % config.VERSION_1_1)
route = RouteGenerator(blueprint)


@route('/')
def list():
    if 'q' in request.args:
        extensions = extension_services.find_by_exten(request.args['q'])
    else:
        extensions = extension_services.find_all()

    result = mapper.encode_list(extensions)
    return make_response(result, 200)


@route('/<int:extensionid>')
def get(extensionid):
    extension = extension_services.get(extensionid)
    result = mapper.encode_extension(extension)

    return make_response(result, 200)


@route('/', methods=['POST'])
def create():
    data = request.data.decode("utf-8")
    data = serializer.decode(data)

    if 'type' not in data and 'typeval' not in data:
        data.update({
            'type': 'user',
            'typeval': 0
         })

    extension = Extension.from_user_data(data)

    extension = extension_services.create(extension)

    extension_location = url_for('.get', extensionid=extension.id)
    result = serializer.encode({
        'id': extension.id
    })

    response = make_response(result, 201)
    response.headers['Location'] = extension_location
    return response


@route('/<int:extensionid>', methods=['PUT'])
def edit(extensionid):
    data = request.data.decode("utf-8")
    data = serializer.decode(data)
    extension = extension_services.get(extensionid)
    extension.update_from_data(data)
    extension_services.edit(extension)
    return make_response('', 204)


@route('/<int:extensionid>', methods=['DELETE'])
def delete(extensionid):
    extension = extension_services.get(extensionid)
    try:
        extension_services.delete(extension)
        return make_response('', 204)
    except ProvdError as e:
        result = "The extension was deleted but the device could not be reconfigured (%s)" % str(e)
        result = serializer.encode([result])
        return make_response(result, 500)
    except SysconfdError as e:
        result = "The extension was deleted but the voicemail content could not be removed (%s)" % str(e)
        result = serializer.encode([result])
        return make_response(result, 500)

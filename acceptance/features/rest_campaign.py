# -*- coding: UTF-8 -*-
#
# Copyright (C) 2012  Avencall
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

from gevent import httplib

from xivo_recording.recording_config import RecordingConfig
import random
import time
from xivo_recording.rest import rest_encoder


class RestCampaign(object):

    def __init__(self):
        unique_id = "lettuce" + time.ctime() + str(random.randint(10000, 99999999))
        queue_id = 1
        base_filename = unique_id + "-" + str(queue_id) + "-"

        self.campaign = {
            "campaign_name": unique_id,
            "base_filename": base_filename,
            "activated": True,
            "queue_id": queue_id
        }

    def create(self, campaign_name):
        connection = httplib.HTTPConnection(
                                RecordingConfig.XIVO_RECORD_SERVICE_ADDRESS +
                                ":" +
                                str(RecordingConfig.XIVO_RECORD_SERVICE_PORT)
                            )

        requestURI = RecordingConfig.XIVO_REST_SERVICE_ROOT_PATH + \
                        RecordingConfig.XIVO_RECORDING_SERVICE_PATH + "/"

        body = rest_encoder.encode(self.campaign)
        headers = RecordingConfig.CTI_REST_DEFAULT_CONTENT_TYPE

        connection.request("POST", requestURI, body, headers)

        reply = connection.getresponse()
        print("\nreply: " + reply.read() + '\n')

        # TODO : Verify the Content-type
        # replyHeader = reply.getheaders()

        assert reply.status == 201

        return (reply.status == 201)

    def list(self):
        connection = httplib.HTTPConnection(
                                RecordingConfig.XIVO_RECORD_SERVICE_ADDRESS +
                                ":" +
                                str(RecordingConfig.XIVO_RECORD_SERVICE_PORT)
                            )

        requestURI = RecordingConfig.XIVO_REST_SERVICE_ROOT_PATH + \
                        RecordingConfig.XIVO_RECORDING_SERVICE_PATH + "/"

        headers = RecordingConfig.CTI_REST_DEFAULT_CONTENT_TYPE

        connection.request("GET", requestURI, "", headers)
        reply = connection.getresponse()

        body = reply.read()

        campaigns = rest_encoder.decode(body)

        result = False
        for campaign in campaigns:
            for attribute in self.campaign:
                if (attribute in campaign):
                    result = True
                    break

        assert result

        return result

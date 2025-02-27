# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random

CONTEXT = 'default'
INCALL_CONTEXT = 'from-extern'
OUTCALL_CONTEXT = 'to-extern'
EXTEN_OUTSIDE_RANGE = str('99999')
USER_EXTENSION_RANGE = list(range(1000, 2000))
MAIN_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee1'
SUB_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee2'


def gen_line_exten():
    return str(random.randint(1000, 1999))


def gen_group_exten():
    return str(random.randint(2000, 2999))


def gen_queue_exten():
    return str(random.randint(3000, 3999))


def gen_conference_exten():
    return str(random.randint(4000, 4999))

# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import yaml

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_file, read_config_file_hierarchy
from xivo.xivo_logging import get_log_level_by_name

API_VERSION = '1.1'
WIZARD_KEY_FILE = '/var/lib/wazo-auth-keys/xivo-wizard-key.yml'

DEFAULT_CONFIG = {
    'debug': False,
    'user': 'www-data',
    'log_level': 'info',
    'config_file': '/etc/wazo-confd/config.yml',
    'extra_config_files': '/etc/wazo-confd/conf.d/',
    'log_filename': '/var/log/wazo-confd.log',
    'pid_filename': '/run/wazo-confd/wazo-confd.pid',
    'rest_api': {
        'profile': None,
        'listen': '0.0.0.0',
        'port': 9486,
        'certificate': '/usr/share/xivo-certs/server.crt',
        'private_key': '/usr/share/xivo-certs/server.key',
        'cors': {
            'enabled': True,
            'allow_headers': ['Content-Type', 'X-Auth-Token', 'Wazo-Tenant'],
        },
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'verify_certificate': '/usr/share/xivo-certs/server.crt',
        'key_file': '/var/lib/wazo-auth-keys/wazo-confd-key.yml',
    },
    'ari': {
        'host': 'localhost',
        'port': 5039,
        'https': False,
        'username': 'xivo',
        'password': 'Nasheow8Eag',
    },
    'bus': {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'exchange_name': 'xivo',
        'exchange_type': 'topic',
        'exchange_durable': True,
    },
    'consul': {
        'scheme': 'https',
        'host': 'localhost',
        'port': 8500,
        'verify': '/usr/share/xivo-certs/server.crt',
    },
    'provd': {
        'host': 'localhost',
        'port': 8666,
        'verify_certificate': '/usr/share/xivo-certs/server.crt',
    },
    'sysconfd': {'host': 'localhost', 'port': '8668'},
    'enabled_plugins': {
        'access_feature': True,
        'agent': True,
        'agent_skill': True,
        'api': True,
        'application': True,
        'call_filter': True,
        'call_filter_fallback': True,
        'call_filter_user': True,
        'call_permission': True,
        'call_pickup': True,
        'call_pickup_member': True,
        'confbridge': True,
        'conference': True,
        'conference_extension': True,
        'configuration': True,
        'context': True,
        'context_context': True,
        'device': True,
        'dhcp': True,
        'endpoint_custom': True,
        'endpoint_iax': True,
        'endpoint_sccp': True,
        'endpoint_sip': True,
        'extension': True,
        'extension_feature': True,
        'features': True,
        'func_key': True,
        'group': True,
        'group_call_permission': True,
        'group_extension': True,
        'group_fallback': True,
        'group_member_user': True,
        'group_schedule': True,
        'ha': True,
        'hep': True,
        'iax_callnumberlimits': True,
        'iax_general': True,
        'incall': True,
        'incall_extension': True,
        'incall_schedule': True,
        'info': True,
        'ivr': True,
        'line': True,
        'line_application': True,
        'line_device': True,
        'line_endpoint': True,
        'line_extension': True,
        'line_sip': True,
        'moh': True,
        'outcall': True,
        'outcall_call_permission': True,
        'outcall_extension': True,
        'outcall_schedule': True,
        'outcall_trunk': True,
        'paging': True,
        'paging_user': True,
        'parking_lot': True,
        'parking_lot_extension': True,
        'provisioning_networking': True,
        'queue': True,
        'queue_extension': True,
        'queue_fallback': True,
        'queue_general': True,
        'queue_member': True,
        'queue_schedule': True,
        'register_iax': True,
        'register_sip': True,
        'registrar': True,
        'rtp': True,
        'schedule': True,
        'sccp_general': True,
        'sip_general': True,
        'skill': True,
        'skill_rule': True,
        'sound': True,
        'sound_language': True,
        'switchboard': True,
        'switchboard_member': True,
        'timezone': True,
        'trunk': True,
        'trunk_endpoint': True,
        'trunk_register': True,
        'user': True,
        'user_agent': True,
        'user_call_permission': True,
        'user_fallback': True,
        'user_group': True,
        'user_import': True,
        'user_line': True,
        'user_line_associated': True,
        'user_schedule': True,
        'user_voicemail': True,
        'voicemail': True,
        'voicemail_general': True,
        'voicemail_zonemessages': True,
        'wizard': True,
    },
    'service_discovery': {
        'enabled': True,
        'advertise_address': 'localhost',
        'advertise_port': 9486,
        'advertise_address_interface': 'eth0',
        'refresh_interval': 25,
        'retry_interval': 2,
        'ttl_interval': 30,
        'extra_tags': [],
    },
    'wizard': {'service_id': None, 'service_key': None},
}


def load(argv):
    try:
        with open(WIZARD_KEY_FILE, 'r') as f:
            key_config = {'wizard': yaml.safe_load(f)}
    except IOError:
        key_config = {}

    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(cli_config, file_config, DEFAULT_CONFIG)
    )
    service_key = _load_key_file(ChainMap(cli_config, file_config, DEFAULT_CONFIG))
    return ChainMap(
        reinterpreted_config,
        key_config,
        cli_config,
        service_key,
        file_config,
        DEFAULT_CONFIG,
    )


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'username': key_file.get('service_id'),
            'password': key_file.get('service_key'),
        }
    }


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config-file',
        action='store',
        help="The path where is the config file. Default: %(default)s",
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="Log debug messages. Overrides log_level. Default: %(default)s",
    )
    parser.add_argument(
        '-l',
        '--log-level',
        action='store',
        default='INFO',
        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
        "critical, error, warning, info, debug. Default: %(default)s",
    )
    parser.add_argument(
        '-u', '--user', action='store', help="The owner of the process."
    )
    parser.add_argument(
        '-p',
        '--profile',
        help="Write profiling stats to directory (for debugging performance issues)",
        action='store',
    )
    parsed_args = parser.parse_args(argv)

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.profile:
        result['rest_api']['profile'] = parsed_args.profile
    if parsed_args.log_level:
        result['log_level'] = parsed_args.log_level
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result


def _get_reinterpreted_raw_values(config):
    result = {}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    return result

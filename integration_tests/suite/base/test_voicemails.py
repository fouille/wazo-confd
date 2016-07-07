
from test_api import confd
from test_api import fixtures
from test_api import mocks
from test_api import scenarios as s
from test_api import errors as e

from test_api.helpers import voicemail as vm_helper
from test_api.helpers import context as context_helper

from hamcrest import assert_that, has_items, contains, has_entry, has_entries, has_item, is_not


def build_string(length):
    return ''.join('a' for _ in range(length))


def test_get_errors():
    fake_get = confd.voicemails(999999).get
    yield s.check_resource_not_found, fake_get, 'Voicemail'


def test_post_errors():
    url = confd.voicemails.post
    for check in error_checks(url):
        yield check

    for check in error_required_checks(url):
        yield check


@fixtures.voicemail()
def test_put_errors(voicemail):
    fake_put = confd.voicemails(9999999).put
    yield s.check_resource_not_found, fake_put, 'Voicemail'

    url = confd.voicemails(voicemail['id']).put
    for check in error_checks(url):
        yield check


def error_checks(url):
    yield s.check_bogus_field_returns_error, url, 'name', 123
    yield s.check_bogus_field_returns_error, url, 'name', None
    yield s.check_bogus_field_returns_error, url, 'name', True
    yield s.check_bogus_field_returns_error, url, 'name', build_string(81)
    yield s.check_bogus_field_returns_error, url, 'number', 123
    yield s.check_bogus_field_returns_error, url, 'number', None
    yield s.check_bogus_field_returns_error, url, 'number', 'one'
    yield s.check_bogus_field_returns_error, url, 'number', '#1234'
    yield s.check_bogus_field_returns_error, url, 'number', '*1234'
    yield s.check_bogus_field_returns_error, url, 'number', build_string(0)
    yield s.check_bogus_field_returns_error, url, 'number', build_string(41)
    yield s.check_bogus_field_returns_error, url, 'context', 123
    yield s.check_bogus_field_returns_error, url, 'context', None
    yield s.check_bogus_field_returns_error, url, 'context', True
    yield s.check_bogus_field_returns_error, url, 'password', 123
    yield s.check_bogus_field_returns_error, url, 'password', True
    yield s.check_bogus_field_returns_error, url, 'password', 'one'
    yield s.check_bogus_field_returns_error, url, 'password', '#1234'
    yield s.check_bogus_field_returns_error, url, 'password', '*1234'
    yield s.check_bogus_field_returns_error, url, 'password', build_string(0)
    yield s.check_bogus_field_returns_error, url, 'password', build_string(81)
    yield s.check_bogus_field_returns_error, url, 'email', 123
    yield s.check_bogus_field_returns_error, url, 'email', True
    yield s.check_bogus_field_returns_error, url, 'email', build_string(81)
    yield s.check_bogus_field_returns_error, url, 'language', 123
    yield s.check_bogus_field_returns_error, url, 'language', True
    yield s.check_bogus_field_returns_error, url, 'timezone', 123
    yield s.check_bogus_field_returns_error, url, 'timezone', True
    yield s.check_bogus_field_returns_error, url, 'max_messages', '2'
    yield s.check_bogus_field_returns_error, url, 'max_messages', True
    yield s.check_bogus_field_returns_error, url, 'max_messages', {}
    yield s.check_bogus_field_returns_error, url, 'max_messages', []
    yield s.check_bogus_field_returns_error, url, 'attach_audio', 'false'
    yield s.check_bogus_field_returns_error, url, 'attach_audio', {}
    yield s.check_bogus_field_returns_error, url, 'attach_audio', []
    yield s.check_bogus_field_returns_error, url, 'delete_messages', 'true'
    yield s.check_bogus_field_returns_error, url, 'delete_messages', None
    yield s.check_bogus_field_returns_error, url, 'delete_messages', {}
    yield s.check_bogus_field_returns_error, url, 'delete_messages', []
    yield s.check_bogus_field_returns_error, url, 'ask_password', 'false'
    yield s.check_bogus_field_returns_error, url, 'ask_password', None
    yield s.check_bogus_field_returns_error, url, 'ask_password', {}
    yield s.check_bogus_field_returns_error, url, 'ask_password', []
    yield s.check_bogus_field_returns_error, url, 'options', 'string'
    yield s.check_bogus_field_returns_error, url, 'options', 1234
    yield s.check_bogus_field_returns_error, url, 'options', True
    yield s.check_bogus_field_returns_error, url, 'options', None
    yield s.check_bogus_field_returns_error, url, 'options', {}
    yield s.check_bogus_field_returns_error, url, 'options', ['string']
    yield s.check_bogus_field_returns_error, url, 'options', ['string', 'string']
    yield s.check_bogus_field_returns_error, url, 'options', [{'string': 'string'}]
    yield s.check_bogus_field_returns_error, url, 'options', [['string']]
    yield s.check_bogus_field_returns_error, url, 'options', [[None, None]]
    yield s.check_bogus_field_returns_error, url, 'options', [['string', 'string', 'string']]
    yield s.check_bogus_field_returns_error, url, 'options', [['string', 'string'], ['string']]


def error_required_checks(url):
    yield s.check_missing_required_field_returns_error, url, 'name'
    yield s.check_missing_required_field_returns_error, url, 'number'
    yield s.check_missing_required_field_returns_error, url, 'context'


@fixtures.voicemail
def test_fake_fields(voicemail):
    fake = [
        ('context', 'wrongcontext', 'Context'),
        ('language', 'fakelanguage', 'Language'),
        ('timezone', 'faketimezone', 'Timezone')
    ]
    requests = (confd.voicemails.post,
                confd.voicemails(voicemail['id']).put)

    for (field, value, error_field) in fake:
        for request in requests:
            fields = _generate_fields()
            fields[field] = value
            response = request(fields)
            yield response.assert_match, 400, e.not_found(error_field)


def _generate_fields():
    number, context = vm_helper.generate_number_and_context()
    return {'number': number, 'context': context, 'name': 'testvoicemail'}


@fixtures.voicemail()
def test_create_voicemail_with_same_number_and_context(voicemail):
    response = confd.voicemails.post(name='testvoicemail',
                                     number=voicemail['number'],
                                     context=voicemail['context'])
    response.assert_match(400, e.resource_exists('Voicemail'))


@fixtures.voicemail()
@fixtures.voicemail()
def test_edit_voicemail_with_same_number_and_context(first_voicemail, second_voicemail):
    response = confd.voicemails(first_voicemail['id']).put(number=second_voicemail['number'],
                                                           context=second_voicemail['context'])
    response.assert_match(400, e.resource_exists('Voicemail'))


@fixtures.voicemail(name="SearchVoicemail",
                    email="searchemail@proformatique.com",
                    pager="searchpager@proformatique.com")
@fixtures.voicemail(name="HiddenVoicemail",
                    email="hiddenvoicemail@proformatique.com",
                    pager="hiddenpager@proformatique.com")
def test_search_voicemail(voicemail, hidden):
    url = confd.voicemails

    searches = {'name': 'searchv',
                'number': voicemail['number'],
                'email': 'searche',
                'pager': 'searchp'}

    for field, term in searches.items():
        yield check_search, url, voicemail, hidden, field, term


def check_search(url, device, hidden, field, term):
    response = url.get(search=term)

    expected_device = has_item(has_entry(field, device[field]))
    hidden_device = is_not(has_item(has_entry(field, hidden[field])))
    assert_that(response.items, expected_device)
    assert_that(response.items, hidden_device)


@fixtures.voicemail()
@fixtures.voicemail()
def test_list_voicemails(first, second):
    response = confd.voicemails.get()
    expected = has_items(has_entries(first), has_entries(second))
    assert_that(response.items, expected)


@fixtures.voicemail()
def test_get_voicemail(voicemail):
    response = confd.voicemails(voicemail['id']).get()
    assert_that(response.item, has_entries(voicemail))


def test_create_minimal_voicemail():
    number, context = vm_helper.generate_number_and_context()
    response = confd.voicemails.post(name='minimal',
                                     number=number,
                                     context=context)

    response.assert_created('voicemails')
    assert_that(response.item, has_entries({'name': 'minimal',
                                            'number': number,
                                            'context': context,
                                            'ask_password': True,
                                            'attach_audio': None,
                                            'delete_messages': False,
                                            'options': contains()}))


def test_create_voicemails_same_number_different_contexts():
    number, context = vm_helper.new_number_and_context('vmctx1')
    other_context = context_helper.generate_context(name='vmctx2')

    response = confd.voicemails.post(name='samenumber1',
                                     number=number,
                                     context=context)
    response.assert_ok()

    response = confd.voicemails.post(name='samenumber2',
                                     number=number,
                                     context=other_context['name'])
    response.assert_ok()


def test_create_voicemail_with_all_parameters():
    number, context = vm_helper.generate_number_and_context()

    parameters = {'name': 'full',
                  'number': number,
                  'context': context,
                  'email': 'test@example.com',
                  'pager': 'test@example.com',
                  'language': 'en_US',
                  'timezone': 'eu-fr',
                  'password': '1234',
                  'max_messages': 10,
                  'attach_audio': True,
                  'ask_password': False,
                  'delete_messages': True,
                  'enabled': True,
                  'options': [["saycid", "yes"],
                              ["emailbody", "this\nis\ra\temail|body"]]}

    expected = has_entries({'name': 'full',
                            'number': number,
                            'context': context,
                            'email': 'test@example.com',
                            'pager': 'test@example.com',
                            'language': 'en_US',
                            'timezone': 'eu-fr',
                            'password': '1234',
                            'max_messages': 10,
                            'attach_audio': True,
                            'ask_password': False,
                            'delete_messages': True,
                            'enabled': True,
                            'options': has_items(["saycid", "yes"],
                                                 ["emailbody", "this\nis\ra\temail|body"])
                            })

    response = confd.voicemails.post(parameters)
    response.assert_created('voicemails')
    assert_that(response.item, expected)


@fixtures.voicemail()
def test_edit_voicemail(voicemail):
    number, context = vm_helper.new_number_and_context('vmctxedit')

    parameters = {'name': 'edited',
                  'number': number,
                  'context': context,
                  'email': 'test@example.com',
                  'pager': 'test@example.com',
                  'language': 'en_US',
                  'timezone': 'eu-fr',
                  'password': '1234',
                  'max_messages': 10,
                  'attach_audio': True,
                  'ask_password': False,
                  'delete_messages': True,
                  'enabled': False,
                  'options': [["saycid", "yes"],
                              ["emailbody", "this\nis\ra\temail|body"]]}

    expected = has_entries({'name': 'edited',
                            'number': number,
                            'context': context,
                            'email': 'test@example.com',
                            'pager': 'test@example.com',
                            'language': 'en_US',
                            'timezone': 'eu-fr',
                            'password': '1234',
                            'max_messages': 10,
                            'attach_audio': True,
                            'ask_password': False,
                            'delete_messages': True,
                            'enabled': False,
                            'options': has_items(["saycid", "yes"],
                                                 ["emailbody", "this\nis\ra\temail|body"])
                            })

    url = confd.voicemails(voicemail['id'])

    response = url.put(parameters)
    response.assert_updated()

    response = url.get()
    assert_that(response.item, expected)


@fixtures.voicemail()
@mocks.sysconfd()
def test_edit_number_and_context_moves_voicemail(voicemail, sysconfd):
    number, context = vm_helper.new_number_and_context('vmctxmove')

    response = confd.voicemails(voicemail['id']).put(number=number,
                                                     context=context)
    response.assert_updated()

    sysconfd.assert_request('/move_voicemail',
                            query={'old_mailbox': voicemail['number'],
                                   'old_context': voicemail['context'],
                                   'new_mailbox': number,
                                   'new_context': context})


@fixtures.voicemail()
def test_delete_voicemail(voicemail):
    response = confd.voicemails(voicemail['id']).delete()
    response.assert_deleted()


@fixtures.voicemail()
@mocks.sysconfd()
def test_delete_voicemail_deletes_on_disk(voicemail, sysconfd):
    response = confd.voicemails(voicemail['id']).delete()
    response.assert_deleted()

    sysconfd.assert_request('/delete_voicemail',
                            query={'mailbox': voicemail['number'],
                                   'context': voicemail['context']})


@fixtures.voicemail()
def test_update_fields_with_null_value(voicemail):
    number, context = vm_helper.generate_number_and_context()

    response = confd.voicemails.post(name='nullfields',
                                     number=number,
                                     context=context,
                                     password='1234',
                                     email='test@example.com',
                                     pager='test@example.com',
                                     language='en_US',
                                     timezone='eu-fr',
                                     max_messages=10,
                                     attach_audio=True)

    url = confd.voicemails(response.item['id'])
    response = url.put(password=None,
                       email=None,
                       pager=None,
                       language=None,
                       timezone=None,
                       max_messages=None,
                       attach_audio=None)
    response.assert_updated()

    response = url.get()
    assert_that(response.item, has_entries({'password': None,
                                            'email': None,
                                            'language': None,
                                            'timezone': None,
                                            'max_messages': None,
                                            'attach_audio': None}))

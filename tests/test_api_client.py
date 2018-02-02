from __future__ import print_function, unicode_literals

import uuid

from nose import with_setup
from nose.tools import assert_equal

from dnsdb_sdk.api import APIClient
from dnsdb_sdk.exceptions import APIException
from tests import api_mock_server, errors
from tests.api_mock_server import APIUser


def setup_func():
    APIClient.API_BASE_URL = 'http://localhost:5000'
    api_mock_server.reset_all_response()
    api_mock_server.start()


def teardown_func():
    api_mock_server.stop()


def check_api_exception(client_func, error):
    api_mock_server.set_api_user_response_and_restart(error.as_response())
    try:
        client_func()
    except APIException as e:
        assert_equal(e.error_code, error.code)
        assert_equal(e.error_msg, error.msg)


@with_setup(setup_func, teardown_func)
def test_search():
    api_user = APIUser('admin')
    client = APIClient(api_id=api_user.api_id, api_key=api_user.api_key)
    result = client.search_dns()
    count = 0
    for _ in result:
        count += 1
    assert_equal(len(result), count)
    assert_equal(result.total, len(api_mock_server.records))
    assert_equal(result.remaining_requests, api_mock_server.api_user_response.get('remaining_requests'))
    check_api_exception(client.search_dns, errors.AUTHENTICATION_FAILED)
    check_api_exception(client.search_dns, errors.INVALID_API_ID)
    check_api_exception(client.search_dns, errors.INVALID_API_KEY)
    check_api_exception(client.search_dns, errors.INVALID_DOMAIN)
    check_api_exception(client.search_dns, errors.INVALID_IP)
    check_api_exception(client.search_dns, errors.INVALID_HOST)
    check_api_exception(client.search_dns, errors.INVALID_VALUE_DOMAIN)
    check_api_exception(client.search_dns, errors.INVALID_VALUE_HOST)
    check_api_exception(client.search_dns, errors.INVALID_VALUE_IP)
    check_api_exception(client.search_dns, errors.INVALID_PAGE)
    check_api_exception(client.search_dns, errors.INVALID_SIZE)
    check_api_exception(client.search_dns, errors.INTERNAL_ERROR)
    check_api_exception(client.search_dns, errors.TOO_LARGE_IP_RANGE)
    check_api_exception(client.search_dns, errors.TOO_LARGE_RESULT_WINDOW)


@with_setup(setup_func, teardown_func)
def test_scan():
    api_user = APIUser('admin')
    client = APIClient(api_id=api_user.api_id, api_key=api_user.api_key)
    scan_id = uuid.uuid4().hex
    total = 5
    api_mock_server.scan_create_response = {
        'scan_id': scan_id,
        'remaining_requests': 10000,
        'records': [
            {'host': 'maps-cctld.l.google.com', 'type': 'a', 'value': '119.110.118.221'},
            {'host': 'maps-cctld.l.google.com', 'type': 'a', 'value': '204.186.215.52'},
            {'host': 'maps-cctld.l.google.com', 'type': 'a', 'value': '46.134.193.89'},
        ],
        'total': total
    }
    api_mock_server.scan_next_response = {
        'scan_id': scan_id,
        'remaining_requests': 10000,
        'records': [
            {'host': 'maps-cctld.l.google.com', 'type': 'a', 'value': '59.18.45.84'},
            {'host': 'maps.l.google.com', 'type': 'a', 'value': '59.18.45.119'},
        ],
        'total': total
    }
    api_mock_server.restart()
    result = client.scan_dns(domain='google.com', dns_type='a', host='', ip='', value_host='', value_ip='', value_domain='',
                             email='', per_size=3)
    assert_equal(result.total, total)
    assert_equal(len(result), total)
    count = 0
    for _ in result:
        count += 1
    assert_equal(count, total)
    check_api_exception(client.scan_dns, errors.AUTHENTICATION_FAILED)
    check_api_exception(client.scan_dns, errors.INVALID_API_ID)
    check_api_exception(client.scan_dns, errors.INVALID_API_KEY)
    check_api_exception(client.scan_dns, errors.INVALID_DOMAIN)
    check_api_exception(client.scan_dns, errors.INVALID_IP)
    check_api_exception(client.scan_dns, errors.INVALID_HOST)
    check_api_exception(client.scan_dns, errors.INVALID_VALUE_DOMAIN)
    check_api_exception(client.scan_dns, errors.INVALID_VALUE_HOST)
    check_api_exception(client.scan_dns, errors.INVALID_VALUE_IP)
    check_api_exception(client.scan_dns, errors.INVALID_SIZE)
    check_api_exception(client.scan_dns, errors.INTERNAL_ERROR)
    check_api_exception(client.scan_dns, errors.TOO_LARGE_IP_RANGE)
    check_api_exception(client.scan_dns, errors.TOO_LARGE_RESULT_WINDOW)


@with_setup(setup_func, teardown_func)
def test_get_user():
    api_user = APIUser('admin')
    client = APIClient(api_id=api_user.api_id, api_key=api_user.api_key)
    user = client.get_api_user()
    assert_equal(user.api_id, api_user.api_id)
    check_api_exception(client.get_api_user, errors.AUTHENTICATION_FAILED)
    check_api_exception(client.get_api_user, errors.INVALID_API_ID)
    check_api_exception(client.get_api_user, errors.INVALID_API_KEY)
    check_api_exception(client.get_api_user, errors.INTERNAL_ERROR)

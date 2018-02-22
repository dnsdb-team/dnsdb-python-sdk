from dnsdb_sdk.api import APIResponse
from nose.tools import assert_false, assert_true


def test_success():
    response = APIResponse({}, 200)
    assert_true(response.success)
    content = {'error_code': 10001, 'error_msg': 'unauthorized'}
    response = APIResponse(content, 200)
    assert_false(response.success)

from dnsdb_sdk.api import APIException, ScanResult
from mock import Mock
from nose.tools import raises


@raises(APIException)
def test_next_raise_api_exception():
    client = Mock()
    client.next_dns_scan = Mock(side_effect=APIException(10001, 'unauthorized'))
    scan_response = Mock()
    scan_response.total = 5
    scan_response.records = []
    result = ScanResult(scan_response, client)
    result.__next__()


@raises(StopIteration)
def test_next_raise_stop_iteration():
    scan_response = Mock()
    scan_response.total = 5
    scan_response.records = []
    client = Mock()
    client.next_dns_scan = Mock(return_value=scan_response)
    result = ScanResult(scan_response, client)
    result.__next__()

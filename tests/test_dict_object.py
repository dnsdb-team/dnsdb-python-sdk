from dnsdb_sdk.api import DictObject, DNSRecord
from nose.tools import assert_equal


class Data(DictObject):
    def __init__(self, records):
        self.records = records
        self.total = len(records)


def test_get_item():
    r = [DNSRecord(host='foo', type='a', value='1.1.1.1')]
    data = Data(r)
    dict_data = dict(data)
    result = {'records': [{'host': 'foo', 'type': 'a', 'value': '1.1.1.1'}], 'total': 1}
    assert_equal(result, dict_data)

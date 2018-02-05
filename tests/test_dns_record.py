from nose.tools import assert_equal

from dnsdb_sdk.api import DNSRecord


def test_dns_record():
    record = DNSRecord(host='foo.com', type='A', value='1.1.1.1')
    record_dic = dict(record)
    assert_equal(record_dic['host'], record.host)
    assert_equal(record_dic['type'], record.type)
    assert_equal(record_dic['value'], record.value)

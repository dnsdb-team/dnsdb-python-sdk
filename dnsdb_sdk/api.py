# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import platform

import requests

from dnsdb_sdk.__init__ import __version__
from dnsdb_sdk.exceptions import APIException

logger = logging.getLogger(__name__)


class DictObject(object):
    def __getitem__(self, item, ignore=None):
        if isinstance(item, int):
            d = self.__dict__
            keys = list(d.keys())
            if ignore is None:
                ignore = []
            for item in ignore:
                keys.remove(item)
            key = keys[item]
            value = d[key]
            if isinstance(value, list):
                list_value = []
                for item in value:
                    list_value.append(dict(item))
                value = list_value
            return key, value


class APIResponse(object):
    def __init__(self, content, status_code):
        self.content = content
        self.error_code = content.get('error_code', None)
        self.error_msg = content.get('error_msg', None)
        self.doc = content.get('doc', None)
        self.status_code = status_code

    @property
    def success(self):
        return self.error_code is None

    def has_error(self):
        return self.error_code is not None


class ScanResponse(APIResponse):

    def __init__(self, content, status_code):
        APIResponse.__init__(self, content, status_code)
        self.scan_id = self.content.get('scan_id')
        self.remaining_requests = self.content.get('remaining_requests')
        self.records = self.content.get('records')
        self.total = self.content.get('total')


class APIUser(DictObject):
    def __init__(self, api_id, user, remaining_requests, creation_time, expiration_time):
        self.api_id = api_id
        self.user = user
        self.remaining_requests = remaining_requests
        self.creation_time = creation_time
        self.expiration_time = expiration_time


class DNSRecord(DictObject):
    def __init__(self, host, type, value):
        self.host = host
        self.type = type
        self.value = value


class SearchResult(object):
    def __init__(self, total, data, remaining_requests):
        self.total = total
        self.data = data
        self.remaining_requests = remaining_requests

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


class ScanResult(object):
    def __init__(self, scan_response, client):
        self.total = scan_response.total
        self.remaining_requests = scan_response.remaining_requests
        self.__scan_id = scan_response.scan_id
        self.__current_data_set = scan_response.records
        self.__client = client
        self.__record_count = 0
        self.request_times = 1

    def __next__(self):
        return self.next()

    def next(self):
        if len(self.__current_data_set) == 0:
            try:
                if self.__record_count == self.total:
                    raise StopIteration()
                scan_response = self.__client.next_dns_scan(self.__scan_id)
                self.request_times += 1
                self.__current_data_set = scan_response.records
                self.remaining_requests = scan_response.remaining_requests
                self.__scan_id = scan_response.scan_id
                if len(self.__current_data_set) > 0:
                    data = self.__current_data_set[0]
                    self.__current_data_set.remove(data)
                    self.__record_count += 1
                    return data
                else:
                    raise StopIteration()
            except APIException as e:
                raise e
        else:
            data = self.__current_data_set[0]
            self.__current_data_set.remove(data)
            self.__record_count += 1
            return data

    def __iter__(self):
        return self

    def __len__(self):
        return self.total


class APIClient(object):
    API_BASE_URL = 'https://api.dnsdb.io'
    API_VERSION = 'v1'

    def __init__(self, api_id, api_key, proxies=None, timeout=None):
        self.api_id = api_id
        self.api_key = api_key
        self.session = requests.Session()
        self.session.proxies = proxies
        self.session.headers = {
            'User-Agent': "DnsDB Python SDK(%s)" % __version__,
            'API-ID': self.api_id,
            'API-Key': self.api_key,
            'Client-Platform': platform.platform(),
            'Client-Python': platform.python_version(),
        }
        self.timeout = timeout

    def __request_get(self, url, params=None):
        response = self.session.get(url, params=params, timeout=self.timeout)
        return APIResponse(response.json(), response.status_code)

    @staticmethod
    def __get_api_url(path):
        return "%s/%s/%s" % (APIClient.API_BASE_URL, APIClient.API_VERSION, path)

    def search_dns_response(self, domain=None, ip=None, host=None, dns_type=None, value_domain=None, value_host=None,
                            value_ip=None, email=None, page=1, page_size=None):
        params = {}
        if domain:
            params['domain'] = domain
        if ip:
            params['ip'] = ip
        if host:
            params['host'] = host
        if dns_type:
            params['type'] = dns_type
        if value_domain:
            params['value_domain'] = value_domain
        if value_host:
            params['value_host'] = value_host
        if value_ip:
            params['value_ip'] = value_ip
        if email:
            params['email'] = email
        if page:
            params['page'] = 1
        if page_size:
            params['size'] = page_size
        return self.__request_get(self.__get_api_url('dns/search'), params=params)

    def get_api_user_response(self):
        return self.__request_get(self.__get_api_url('api_user'))

    def search_dns(self, domain=None, ip=None, host=None, dns_type=None, value_domain=None, value_host=None,
                   value_ip=None, email=None, page=1, per_size=None):
        response = self.search_dns_response(domain, ip, host, dns_type, value_domain, value_host, value_ip, email, page,
                                            per_size)
        if response.has_error():
            raise APIException(response.error_code, response.error_msg)
        else:
            data = response.content
            total = data.get('total')
            remaining_requests = data.get('remaining_requests')
            records = []
            for record in data.get('records', []):
                records.append(DNSRecord(host=record.get('host'), type=record.get('type'), value=record.get('value')))
            return SearchResult(total=total, data=records, remaining_requests=remaining_requests)

    def get_api_user(self):
        """
        获取API User信息
        :return:  API User对象
        """
        response = self.get_api_user_response()
        if response.has_error():
            raise APIException(response.error_code, response.error_msg)
        else:
            data = response.content
            return APIUser(api_id=data.get('api_id'), user=data.get('user'),
                           remaining_requests=data.get('remaining_requests'), creation_time=data.get('creation_time'),
                           expiration_time=data.get('expiration_time'))

    def create_dns_scan(self, domain=None, ip=None, host=None, dns_type=None, value_domain=None, value_host=None,
                        value_ip=None, email=None, per_size=None):
        params = {}
        if domain:
            params['domain'] = domain
        if ip:
            params['ip'] = ip
        if host:
            params['host'] = host
        if dns_type:
            params['type'] = dns_type
        if value_domain:
            params['value_domain'] = value_domain
        if value_host:
            params['value_host'] = value_host
        if value_ip:
            params['value_ip'] = value_ip
        if email:
            params['email'] = email
        if per_size:
            params['size'] = per_size
        response = self.__request_get(self.__get_api_url('dns/scan/create'), params=params)
        return ScanResponse(response.content, response.status_code)

    def next_dns_scan(self, scan_id):
        response = self.__request_get(self.__get_api_url('dns/scan/next'), params={'scan_id': scan_id})
        return ScanResponse(response.content, response.status_code)

    def scan_dns(self, domain=None, ip=None, host=None, dns_type=None, value_domain=None, value_host=None,
                 value_ip=None,
                 email=None, per_size=None):
        scan_response = self.create_dns_scan(domain=domain, ip=ip, host=host, dns_type=dns_type,
                                             value_domain=value_domain, value_host=value_host, value_ip=value_ip,
                                             email=email, per_size=per_size)
        return ScanResult(scan_response, self)

# DnsDB Python SDK

[![build-status-image]][travis]
[![pypi-version]][pypi]
[![python-version]][pypi]
[![license]][pypi]

**dnsdb-python-sdk** 是[DnsDB](https://dnsdb.io) 为开发者提供的python SDK。使用该SDK，您可以方便的将DnsDB的查询服务集成到您的python应用中，您也可以利用它来导出查询结果。[查看教程](https://github.com/dnsdb-team/dnsdb-python-sdk/wiki/Tutorials)

# Install

```shell
pip install --upgrade dnsdb-python-sdk
```

# How to use

```python
from dnsdb_sdk.api import APIClient

api_id = "your API ID"
api_key = "your API key"
client = APIClient(api_id, api_key)
result = client.search_dns(domain='github.com')
for record in result:
    print(record)
```

# 相关链接
* [DnsDB官网](https://dnsdb.io)
* [DnsDB API服务介绍](https://dnsdb.io/apiservice)
* [DnsDB Web API](https://apidoc.dnsdb.io)
* [GetDNS - 基于DnsDB-Python-SDK开发的命令行工具](https://getdns.dnsdb.io)

[build-status-image]: https://img.shields.io/travis/dnsdb-team/dnsdb-python-sdk/master.svg
[travis]: https://travis-ci.org/dnsdb-team/dnsdb-python-sdk
[pypi-version]: https://img.shields.io/pypi/v/dnsdb-python-sdk.svg
[pypi]: https://pypi.python.org/pypi/dnsdb-python-sdk
[python-version]: https://img.shields.io/pypi/pyversions/dnsdb-python-sdk.svg
[license]: https://img.shields.io/pypi/l/dnsdb-python-sdk.svg

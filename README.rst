=================
DnsDB Python SDK
=================

.. image:: https://img.shields.io/travis/dnsdb-team/dnsdb-python-sdk/master.svg
    :target: https://travis-ci.org/dnsdb-team/dnsdb-python-sdk
.. image:: https://img.shields.io/pypi/v/dnsdb-python-sdk.svg
    :target: https://pypi.python.org/pypi/dnsdb-python-sdk
.. image:: https://img.shields.io/pypi/pyversions/dnsdb-python-sdk.svg
    :target: https://pypi.python.org/pypi/dnsdb-python-sdk


**dnsdb-python-sdk** 是 DNSDB_ 为开发者提供的python SDK。使用该SDK，您可以方便的将DNSDB的查询服务集成到您的python应用中，您也可以利用它来导出查询结果。查看教程_。


Install
========

::

    pip install --upgrade dnsdb-python-sdk


How to use
==========

::

    from dnsdb_sdk.api import APIClient

    api_id = "your API ID"
    api_key = "your API key"
    client = APIClient(api_id, api_key)
    result = client.search_dns(domain='github.com')
    for record in result:
        print(record)

更多使用方法请 查看教程_


Links
========

* `DNSDB网站 <https://dnsdb.io>`_
* `DNSDB API服务介绍 <https://dnsdb.io/apiservice>`_
* `DNSDB Web API <https://apidoc.dnsdb.io>`_
* `GetDNS - 基于dnsdb-python-sdk开发的命令行工具 <https://getdns.dnsdb.io>`_

.. _DNSDB: https://dnsdb.io
.. _查看教程: https://github.com/dnsdb-team/dnsdb-python-sdk/wiki/Tutorials


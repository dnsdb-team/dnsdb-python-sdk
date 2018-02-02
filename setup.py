from setuptools import find_packages, setup

PACKAGE = "dnsdb_sdk"
NAME = "dnsdb-python-sdk"
DESCRIPTION = "DnsDB Python SDK"
AUTHOR = "DnsDB Team"
AUTHOR_EMAIL = "team@dnsdb.io"
URL = "http://pysdk.dnsdb.io"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD License",
    url=URL,
    packages=find_packages(exclude=['docs', 'tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    zip_safe=False,
    install_requires=['requests[socks]'],
)

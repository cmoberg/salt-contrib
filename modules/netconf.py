'''
A module for gathering performing NETCONF queries

:maintainer:    Carl Moberg <calle@tail-f.com>
:maturity:      new
:depends:       ncclient - a Python library for NETCONF clients
:platform:      all
'''

# Import python libs
import re
import logging

# Import salt libs
import salt.utils

# Import NETCONF libs
from ncclient import manager

log = logging.getLogger(__name__)


def __virtual__():
    return 'netconf'

def my_unknown_host_cb(host,fingerprint):
    return True

def get_config(host="127.0.0.1", port="830", username="admin", password="admin", source="running", filter=None):
    '''
    Perform a NETCONF request to a host, on a port, on a database, using an XPath filter.

    CLI Example:

    .. code-block:: bash

        salt '*' netconf.get_config <ip-address> <port> <username> <password> <source> <filter>
        salt '*' netconf.get_config 127.0.0.1 2022 admin admin running "aaa"
    '''

    m = manager.connect(host=host, port=port,
                        username=username, password=password,
                        unknown_host_cb=my_unknown_host_cb,
                        allow_agent=False,
                        look_for_keys=False) 

    if filter != None:
        assert(":xpath" in m.server_capabilities), "Server does not support XPath filtering"
        result = m.get_config(source, ('xpath', filter))
    else:
        result = m.get_config(source)

    return result.data_xml

def capabilities(host="127.0.0.1", port="830", username="admin", password="admin"):
    '''

    Query for the NETCONF capabilities advertised by a specific host

    CLI Example:

    .. code-block:: bash
    
        salt '*' netconf.capabilities <ip-address> <port> <username> <password>
        salt '*' netconf.capabilities 127.0.0.1 2022 admin admin
    '''

    m = manager.connect(host=host, port=port,
                        username=username, password=password,
                        unknown_host_cb=my_unknown_host_cb,
                        allow_agent=False,
                        look_for_keys=False) 

    return '\n'.join(m.server_capabilities)


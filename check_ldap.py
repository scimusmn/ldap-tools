#!/usr/bin/env python

# Script to check the status of a remote LDAP search

import ConfigParser
import string
import subprocess
import sys
import ldap
import ldap.sasl

config = ConfigParser.ConfigParser()
config.read("ldap.cfg")
LDAP_URI = 'ldap://' + config.get("ldap", "host")
# TODO (bkennedy): Conditionally read port if desired.
#LDAP_PORT = config.get("ldap", "port")
#LDAP_URI = 'ldap://' + LDAP_HOST + ':' + LDAP_PORT
LDAP_BASE_DN = config.get("ldap", "base_dn")
BIND_USER = config.get("ldap", "bind_user")
BIND_PASSWD = config.get("ldap", "bind_passwd")

class LDAPUserMgmt:

    def __init__(self, ldap_uri=None, ldap_base_dn=None, bind_user=None, bind_passwd=None):
        if not ldap_uri:
            ldap_uri = LDAP_URI
        if not ldap_base_dn:
            ldap_base_dn = LDAP_BASE_DN
        if not bind_user:
            bind_user = BIND_USER
        if not bind_passwd:
            bind_passwd = BIND_PASSWD
        #self.ldap_connection = ldap.initialize(ldap_uri,trace_level=2)
        self.ldap_connection = ldap.initialize(ldap_uri)
        self.ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
        self.ldap_connection.simple_bind(bind_user, bind_passwd)
        self.ldap_base_dn = ldap_base_dn

    def list_users(self, search_filter=None, attributes=None):
        results = self.ldap_connection.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)
        for result in results:
            attribute_dict = result[1]
            for attribute in attributes:
                if type(attribute_dict) is dict:
                    out = "%s: %s" % (attribute, attribute_dict[attribute])
                    print out

    def unbind_s(self):
        self.ldap_connection.unbind_s

def main():
    l = LDAPUserMgmt()
    l.list_users(search_filter='CN=bkennedy*', attributes=['cn', 'distinguishedName'])
    l.unbind_s()

if __name__ == "__main__":
    main()

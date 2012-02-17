#!/usr/bin/env python

# Script to check the status of a remote LDAP search

import ConfigParser
import string
import subprocess
import sys
import ldap
import time

config = ConfigParser.ConfigParser()
config.read("ldap.cfg")
LDAP_URI = 'ldap://' + config.get("ldap", "host")
# TODO (bkennedy): Conditionally read port if desired.
#LDAP_PORT = config.get("ldap", "port")
#LDAP_URI = 'ldap://' + LDAP_HOST + ':' + LDAP_PORT
LDAP_BASE_DN = config.get("ldap", "base_dn")
BIND_USER = config.get("ldap", "bind_user")
BIND_PASSWD = config.get("ldap", "bind_passwd")
LDAP_SEARCH_FILTER = config.get("ldap", "search_filter")
VERBOSE = config.getboolean("ldap", "verbose")

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

        try:
            self.ldap_connection = ldap.initialize(ldap_uri)
        except:
            error_print("Connect error: %s" % (e), 1)

        self.ldap_connection.set_option(ldap.OPT_REFERRALS, 0)

        try:
            self.ldap_connection.simple_bind_s(bind_user, bind_passwd)
        except ldap.LDAPError as e:
            error_print("Bind error: %s" % (e), 2)

        self.ldap_base_dn = ldap_base_dn

    def list_users(self, search_filter=None, attributes=None):
        try:
            results = self.ldap_connection.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)
            entries = []
            for result in results:
                attribute_dict = result[1]
                for attribute in attributes:
                    if type(attribute_dict) is dict:
                        entry = "%s: %s" % (attribute, attribute_dict[attribute])
                        entries.append(entry)

            if len(entries) == 0:
                self.ldap_connection.unbind()
                error_print("Your search returned no results", 3)
            else:
                self.ldap_connection.unbind()
                result_print(entries)
        except ldap.LDAPError as e:
            self.ldap_connection.unbind()
            error_print("Search error: %s" % (e), 4)

def main():
    l = LDAPUserMgmt()
    l.list_users(search_filter=LDAP_SEARCH_FILTER, attributes=['cn', 'distinguishedName'])

def error_print(message = '', error_code=0):
    if VERBOSE == True:
        print message
    else:
        print error_code
    sys.exit(error_code)

def result_print(entries = []):
    if VERBOSE == True:
        print '\n'.join(entries)
    else:
        print 0
    sys.exit(0)

if __name__ == "__main__":
    main()

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

    def unbind(self):
        self.ldap_connection.unbind_s

def main():
    l = LDAPUserMgmt()
    l.list_users(search_filter='CN=username*', attributes=['cn', 'distinguishedName'])
    l.unbind()

if __name__ == "__main__":
    main()


#def main():
    #l = userLDAPMgmt
    #l.list_users(attrib=['cn', 'mail', 'homePhone'])
    #print ldap.__version__

    #ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    #l = ldap.initialize('ldap://' + LDAP_IP)
    #l.set_option(ldap.OPT_REFERRALS, 0)
    #l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    #l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
    #l.set_option( ldap.OPT_X_TLS_DEMAND, True )
    #l.set_option( ldap.OPT_DEBUG_LEVEL, 255 )

    #try:
        ##l.start_tls_s()
        #l.bind_s(BIND_USER, BIND_PASS)
    #except ldap.INVALID_CREDENTIALS:
        #print "Your username or password is incorrect."
        #sys.exit()
    #except ldap.LDAPError, e:
        #if type(e.message) == dict and e.message.has_key('desc'):
            #print e.message['desc']
        #else:
            #print e
        #sys.exit()

    #print "Bind worked"

    #ldapsearch_str = "ldapsearch" + \
            #" -b '" + SEARCH_SCOPE + "'" + \
            #" -D " + "'" + BIND_USER + "'" + \
            #" -H " + "'ldap://" + LDAP_IP + ":389'" + \
            #" -x" + \
            #" -w '" + BIND_PASS + "'"
    #print ldapsearch_str
    #output,error = (call_command(ldapsearch_str))
    #print "output = " + output
    #print "error = " + error

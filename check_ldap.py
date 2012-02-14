#!/usr/bin/env python

# Script to check the status of a remote LDAP search

import ConfigParser
import string
import subprocess
import sys

config = ConfigParser.ConfigParser()
config.read("ldap.cfg")
LDAP_IP = config.get("ldap", "ip")
LDAP_PORT = config.getint("ldap", "port")
SEARCH_SCOPE = config.get("ldap", "scope")
BIND_USER = config.get("ldap", "bind_user")
BIND_PASS = config.get("ldap", "bind_pass")

def main():
    ldapsearch_str = "ldapsearch" + \
            " -b '" + SEARCH_SCOPE + "'" + \
            " -D " + "'" + BIND_USER + "'" + \
            " -H " + "'ldap://" + LDAP_IP + "'" + \
            " -x" + \
            " -w '" + BIND_PASS + "'"
    print ldapsearch_str
    output,error = (call_command(ldapsearch_str))
    print "output = " + output
    print "error = " + error

# Parse commands for python
def call_command(command):
    process = subprocess.Popen(command.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True
                              )
# Returns a tuple of the stdout and stderr
    return process.communicate()

if __name__ == "__main__":
    main()

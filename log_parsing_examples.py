#!/usr/bin/env python
#
# Examples of parsing through the contents of /var/log/messages to identify hosts hitting HAProxy or see what items have logged there
#
# This comes primarily from David Beazley's slides "Generator Tricks for Systems Programmers"
# http://www.dabeaz.com/generators/Generators.pdf


import re
from collections import Counter

source_file='/var/log/messages'

data = open(source_file)

def log_sources(data):
    logpats=r'\<(\S+)\>(\S+ * \S+ \S*) (\S+) ([a-zA-Z]+)[\.\[\]0-9]*:* (.*)'
    logpat=re.compile(logpats)
    groups = ( logpat.match(line) for line in data)
    tuples = ( g.groups() for g in groups if g)
    sources = ( tuple[3] for tuple in tuples if tuple)
    return sources

def haproxy_sources(data):
    logpats_haproxy=r'\<(\S+)\>(\S+ * \S+ \S*) (\S+) ([a-zA-Z]+)[\.\[\]0-9]*:* (\S+):[0-9]* (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) \"(\S+) (\S+) \S+'
    logpat=re.compile(logpats_haproxy)
    groups = ( logpat.match(line) for line in data)
    tuples = ( g.groups() for g in groups if g)
    sources = ( tuple[4] for tuple in tuples if tuple if tuple[9] == '404')
    #sources = ( tuple[4] for tuple in tuples if tuple)
    return sources
    #return tuples

sources = haproxy_sources(data)

for source in Counter(sources).items():
    print str(source[0])+" - "+str(source[1])

#for source in set(sources):
#    print source

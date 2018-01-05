#!/usr/bin/env python                                                                                                                                                                                             
"""                                                                                                                                                                                                               
Output rabbitmq logs with each log entry grouped onto a single line                                                                                                                                               
Read the log file from the first argument passed to the script                                                                                                                                                    
                                                                                                                                                                                                                  
If you need to read from stdin, just pass /dev/stdin as the argument:                                                                                                                                              
$ cat rabbit@messaging-node-1.log | python parse_rabbit_logs.py /dev/stdin                                                                                                                                        
"""

from itertools import groupby, ifilter, imap
import sys
RABBIT_LOG = sys.argv[1]
with open(RABBIT_LOG) as f:
    lines = f.readlines()
    out = groupby(map(lambda x: x.strip(),lines), lambda x: x != '')
    matching_groups = ifilter(lambda x: x[0], out)
    log_messages = imap(lambda x: x[1], matching_groups)
    for x in log_messages: print '\t'.join(list(x))

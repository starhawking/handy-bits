#!/usr/bin/env python3
'''
Example of identifying all of the parameters that need to be populated for templated string replacement

Put another way, find ${all} of ${these} ${paramater_names} in a string

I was investigating this as part of identifying all of the required environment variables for a docker-compose.yaml file
'''

import argparse
from string import Template
from itertools import chain
import os
import re


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        type=argparse.FileType('r'))
    return parser.parse_args()

def main():
    args = parse_args()
    raw_string = args.f.read()
    '''
    The Template class has a pattern attribute that is a compiled regex match object
    We can pull this match object off of it, and find the matches against our string
    '''
    format_pattern = Template.pattern
    string_params = re.finditer(format_pattern, raw_string)
    groups = map(lambda x: x.groups(), string_params)
    all_groups = chain.from_iterable(groups)
    final_matches = filter(lambda x: x, all_groups)
    for x in sorted(final_matches):
        print(x)

if __name__ == '__main__':
    main()
    


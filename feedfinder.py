#!/usr/bin/env python3

import urllib.request
import argparse
import re
import sys
import ssl
from bs4 import BeautifulSoup

HTML_PARSER = 'html.parser'

parser = argparse.ArgumentParser(description='Extract RSS/ATOM URLs from web sites.')
parser.add_argument('input_file', type=str, nargs=1, help='input file name')
parser.add_argument('--user-agent', type=str, nargs='?', help='user agent string')
parser.add_argument('--no-check-certificate', action='store_true', help='ignore SSL certificate validation errors')
args = parser.parse_args()

headers = {}
if args.user_agent != None:
    headers['User-Agent'] = args.user_agent

ctx = None
if args.no_check_certificate:
    # Don't perform SSL certificate validation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

with open(args.input_file[0], 'r') as infile:
    for line in infile.readlines():
        try:
            line = re.sub(r'/$', '', line.strip())
            req = urllib.request.Request(line, headers=headers)
            if ctx != None:
                soup = BeautifulSoup(urllib.request.urlopen(req, context=ctx).read(), HTML_PARSER)
            else:
                soup = BeautifulSoup(urllib.request.urlopen(req).read(), HTML_PARSER)
            for link in soup.find_all('link', rel='alternate'):
                if link.has_attr('type') and (link['type'] == 'application/rss+xml' or link['type'] == 'application/atom+xml'):
                    if link['href'].lower().startswith('http://') or link['href'].lower().startswith('https://'):
                        # link is absolute
                        print(link['href'])
                    else:
                        # link is relative
                        print(line + link['href'])
        except Exception as e:
            sys.stderr.write(f'++ ERROR({e}): {line}\n')

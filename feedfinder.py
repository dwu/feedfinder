import urllib2
import argparse
import re
import sys
import ssl
from bs4 import BeautifulSoup

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

with open(args.input_file[0], "rb") as infile:
    for line in infile.readlines():
        try:
            line = re.sub(r'/$', '', line.strip())
            req = urllib2.Request(line, headers=headers)
            if ctx != None:
                soup = BeautifulSoup(urllib2.urlopen(req, context=ctx).read())
            else:
                soup = BeautifulSoup(urllib2.urlopen(req).read())
            for link in soup.find_all('link', rel="alternate"):
                if link['href'].lower().startswith("http://") or link['href'].lower().startswith("https://"):
                    # link is absolute
                    print link['href']
                else:
                    # link is relative
                    print line + link['href']
        except (urllib2.HTTPError, urllib2.URLError):
            sys.stderr.write("++ ERROR: " + line + '\n')

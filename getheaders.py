#!/usr/bin/env python
import argparse
import collections
import json

import requests
from colors import blue, bold, green, red, underline
from prettytable import PrettyTable


def print_headers():
    resp = requests.get(args.url, headers=headers)
    if resp.ok:
        headtable = PrettyTable(["header", "value"])
        headtable.header = False
        session_info = {}
        h = collections.OrderedDict(sorted(resp.headers.items()))
        for header in h:
            if header == 'x-akamai-session-info':
                aheadtable = PrettyTable(["header", "value"])
                aheadtable.header = False
                si = [x.strip() for x in h[header].split(',')]
                for s in si:
                    i = [x.strip() for x in s.split(';')]
                    session_info[i[0][5:]] = i[1][6:]
                    if len(i) > 2:
                        t = i[2].split('=')
                        session_info[t[0]] = t[1]
            elif header == 'x-check-cacheable':
                if h[header] == 'NO':
                    headtable.add_row([blue(header), red(h[header])])
                else:
                    headtable.add_row([blue(header), green(h[header])])
            elif header == 'x-cache':
                if 'TCP_MISS' in h[header]:
                    headtable.add_row([blue(header), red(h[header])])
                else:
                    headtable.add_row([blue(header), green(h[header])])
            else:
                headtable.add_row([blue(header), green(h[header])])
        headtable.align = "l"
        print bold(underline(blue("### Headers")))
        print headtable
        if session_info:
            if args.session:
                d = collections.OrderedDict(sorted(session_info.items()))
                for key in d:
                    aheadtable.add_row([blue(key), green(d[key])])
                aheadtable.align = "l"
                print bold(underline(blue("### Akamai Session Info")))
                print aheadtable


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Headers")
    parser.add_argument("url", help="URL to get Header info", type=str)
    parser.add_argument(
        "-p",
        "--pragma",
        help="Request Pragma Headers.",
        action='store_true')
    parser.add_argument(
        "-s",
        "--session",
        help="Show Akamai Session Info.",
        action='store_true')
    args = parser.parse_args()
    if args.pragma:
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Pragma': ('akamai-x-check-cacheable,'
                              ' akamai-x-get-request-id,'
                              ' akamai-x-cache-on,'
                              ' akamai-x-cache-remote-on,'
                              ' akamai-x-get-cache-key,'
                              ' akamai-x-get-extracted-values,'
                              ' akamai-x-get-true-cache-key')
                   }
    else:
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
    print_headers()

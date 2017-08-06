#!/usr/bin/env python3

# Script to print links in a web page, in the reverse order of # of occurrences
# Useful e.g. to count most popular referrals on "Ask HN"
#
# usage: links.py [-h] [--html] --url URL
#
# Extract top links out of a HTML page
# 
# optional arguments:
#   -h, --help  show this help message and exit
#   --html      Print output as a HTML table
#   --url URL   Input URL

import argparse

from urllib import request, parse
from collections import defaultdict
from bs4 import BeautifulSoup


def get_links(url):
    conn = request.urlopen(url)
    html = conn.read()

    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    link_dict = defaultdict(int)
    for tag in links:
        link = tag.get('href', None)
        # kill links like javascript: and mailto:
        if link and link.startswith('http'):
            link = parse.urljoin(url, link)
            link_dict[link] += 1
    return link_dict


def print_links(link_dict, url, in_html):
    title = 'Top links in %s' % url
    if in_html:
        print('<html><head><title>%s</title></head>' % title)
        print('<body><h3>%s</h3><table width="100%%"><tr><th align="left">Link</th><th align="right">Mentions</th></tr>'\
              % title)
    else:
        print(title)
    # Sort descending by link count, then sort by URL in alphabetical order
    # Secondary sort credit:
    # https://stackoverflow.com/questions/11476371/sort-by-multiple-keys-using-different-orderings
    for l in sorted(link_dict, key=lambda k: (link_dict[k], [-ord(c) for c in k]), reverse=True):
        if in_html:
            print('<tr><td><a href="%s">%s</a></td><td align="right">%d</td></tr>' % (l, l, link_dict[l]))
        else:
            print('%s\t%d' % (l, link_dict[l]))
    if in_html:
        print('</table></body></html>')

def main():
    parser = argparse.ArgumentParser(description='Extract top links out of a HTML page')
    parser.add_argument("--html", help="Print output as a HTML table",
                        default=False, action="store_true")
    parser.add_argument("--url", help="Input URL", required=True)
    args = parser.parse_args()
    link_dict = get_links(args.url)
    print_links(link_dict, args.url, args.html)


if __name__ == '__main__':
    main()


"""For each pattern and each URL, starting at start_url, find the
URLs of all links matching pattern.
"""

import argparse
from bs4 import BeautifulSoup
import os.path
import re
import requests
import urllib.parse

def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser(description='For each pattern and each address, starting at start_url, find the addresses of all links matching pattern.')
    parser.add_argument('--start_url', '-s', required=True, help='the url of the page at which to start the search for links matching patterns')
    parser.add_argument('--patterns', '-p', required=True, nargs='+', help='regular expressions to search in each link in each page at each url')
    return parser.parse_args()

def get_matching_links_in_page_at(url, pattern):
    """Get all links in page at URL with href matching pattern.

    Arguments
    ---------
    url : str
        URL of page containing links
    pattern : str
        regular expression to search in each link in page at url

    Returns
    -------
    links : list
        list of links (URLs) matching pattern
    """
    parsed_url = urllib.parse.urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    path = parsed_url.path
    compiled_pattern = re.compile(pattern)
    page = requests.get(url).text
    soup = BeautifulSoup(page)
    anchors = soup.findAll('a')
    hrefs = [anchor.get('href') for anchor in anchors]
    links = list(filter(lambda href: compiled_pattern.search(href) != None, hrefs))
    scheme_pattern = re.compile(r'[a-z]+://')
    for (index, link) in enumerate(links):
        if link.startswith('/'):
            links[index] = scheme + '://' + netloc + link
        elif link.startswith('#'):
            links[index] = url + link
        elif not scheme_pattern.match(link):
            links[index] = scheme + netloc + os.path.dirname(path) + '/' + link
    return links

def get_matching_links_in_pages_at(urls, pattern):
    """Get all links in pages at URLs with href matching pattern.

    Arguments
    ---------
    urls : list
        list of URLs of pages containing links
    pattern : str
        regular expression to search in each link in each page
        at each url

    Returns
    -------
    links : list
        list of links (URLs) matching pattern
    """
    links = []
    for url in urls:
        links.extend(get_matching_links_in_page_at(url, pattern))
    return links

def follow_matching_links_in_pages_at(urls, patterns):
    """For each pattern, get all links in pages at URLs with href
    matching pattern and update the URLs to search for matching links.

    Arguments
    ---------
    urls : list
        list of URLs of pages containing links
    patterns : list
        regular expressions to search in each link in each page
        at each url

    Returns
    -------
    links : list
        list of links (URLs) matching pattern
    """
    links = urls
    for pattern in patterns:
        links = get_matching_links_in_pages_at(links, pattern)
    return links

def main():
    """Parse commandline arguments & report the addresses of
    linked statistics pages."""
    args = parse_args()
    links = follow_matching_links_in_pages_at([args.start_url], args.patterns)
    for link in links:
        print(link)

if __name__ == '__main__':
    main()


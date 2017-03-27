#!/usr/bin/python

import os
import sys
import urllib2
import urlparse
import re
import itertools

def download(url, user_agent = 'wswp', num_retries = 2):
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers = headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    #down each link:
    for link in links:
        html = download(link)
        print html
def crawl_idtree(url):
    # maximum number of consecutive download errors allowed
    max_errors = 5
    #current number of consecutive download errors
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            num_errors += 1
        if num_errors == max_errors:
            break
        else:
            print 'success'
            num_errors = 0
            
            
def link_crawler(seed_url, link_regex):
    crawl_queue= [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            if re.match(link_regex, link):
                print link
                link = urlparse.urljoin(seed_url, link)
                print link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)
def get_links(html):
    webpage_regex = re.compile('<a href="(.*?)"', re.IGNORECASE)
    return webpage_regex.findall(html)




if __name__ == '__main__':
    #test()
    #crawl_idtree(sys.argv[1])
    #crawl_sitemap(sys.argv[1])
    link_crawler(sys.argv[1], sys.argv[2])
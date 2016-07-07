#!/usr/bin/env python2.7 

import requests
from bs4 import BeautifulSoup
from collections import deque
import httplib
from pybloom import ScalableBloomFilter

host_url = "https://en.wikipedia.org"
url_start = "https://en.wikipedia.org/wiki/Foxing_(band)"
url_finish = "https://en.wikipedia.org/wiki/Rock_music"
master_map={}
master_bloom=ScalableBloomFilter(mode=ScalableBloomFitler.SMALL_SET_GROWTH)
"""Function takes in a URL and returns a list of URLS of next level traversal. Hashing is used in place of lists due to the approx O(1) time for look-up
   compared to list look-up time of O(n). This function uses a dictionary as its hash table and maps URL to traversal level for ease of checking."""
def parse_page_hash(req_page, level):
    level+=1
    url_map={}
    raw_html = requests.get(req_page).content
    parse_data = BeautifulSoup(str(raw_html),"html.parser")
    
    for child in parse_data.find_all('a'):
        child_url = str(child.get('href'))
        if child_url.startswith('/wiki'):
            url_map[host_url+child_url] = level
    return url_map


def find_level_hash(start_url, end_url):
    queue = deque([start_url])
    master_map[start_url] = 0
    while len(queue)!=0:
        cur_url = queue.popleft()

        if cur_url in master_map:
            url_map = parse_page_hash(cur_url,master_map[cur_url])
        else:
            return -1
        
        for key in url_map:
            if key not in master_map:
                master_map[key] = url_map[key]
                queue.append(key)
            if key==end_url:
                return master_map[key]
    return -1

#returns bloom filter containing all links in the page
def parse_page_bloom(req_page):
	local_bloom = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
	raw_html = requests.get(req_page).content
    parse_data = BeautifulSoup(str(raw_html),"html.parser")
    
    for child in parse_data.find_all('a'):
        child_url = str(child.get('href'))
        if child_url.startswith('/wiki'):
			local_bloom.add(host_url+child_url)
	return local_bloom

#processes one level of the tree. If item may be in master bloom filter, then reject to avoid cycles. May cause false negative and will be analyzed 
def process_tree_level_bloom(level_queue):
	next_queue=deque([])
	while len(level_queue)!=0:
		cur_url = level_queue.popleft()
		cur_bloom = parse_page_bloom(cur_url)		
		for x in cur_bloom:
			if x==url_finish:
				return 1
			if x not in master_bloom:
				master_bloom.add(x)
				next_queue.append(x)
	return next_queue
#feeds each level into process_tree_level_bloom. We practice soft modularity here so that it is easier to maintain a counter. 
def find_level_bloom(start_url, end_url):
	counter = 0
	queue = deque([start_url]) 
	while len(queue)!=0:
		counter+=1
		next_queue = process_tree_level_bloom(queue)
		if isInstance(next_queue, (int, long)):
			return counter
		queue = next_queue
	return -1
print url_start, url_finish
print find_level_hash(url_start, url_finish)

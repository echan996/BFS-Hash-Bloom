# BFS-Hash-Bloom

This program runs a breadth first search on Wikipedia pages to determine the distance between two related pages. The project serves two purposes. From the data we gather, we can observe the "6 degrees of separation" phenomenon using Wikipedia pages as our reference material. More importantly, we use the project as a means of comparing the spatial and time efficiency--as well as the risk of false negatives--in hash tables and bloom filters.  
The Python script requires the following library imports to run.   

<pre><code>import requests  
from bs4 import BeautifulSoup  
from collections import deque  
import httplib  
from pybloom import ScalableBloomFilter</code></pre>
---
##TODO
1.  Implement threading for url page parsing for both the hash table and bloom filter BFS implementations. 
2.  Implement random Wikipedia page selection. This is currently not feasible because without threading, the implementation is simply too slow to run a BFS with more than 3 levels as the tree expands far too quickly and the available processing power is limited. 
3.  Gather data and compare runtime/spatial usage ratios between the hash table and bloom filter implementations. Usage ratios will be favored over absolute values because some data was collected prior to threading implementation. If there is significant deviation between the ratios--there shouldn't be--then data from the non-threaded implementation will be discarded. 
4.  May implement option parser for the python script on command line. User may then pass in URLs as start and end points.

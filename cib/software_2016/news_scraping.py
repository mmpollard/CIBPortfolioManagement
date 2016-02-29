
# coding: utf-8

# In[1]:

import scipy
import pandas as pd
import numpy as np
import math
import pymongo
import MySQLdb as sql
import _mysql
import random
import csv
import time
import re
import matplotlib.pyplot as plt; import matplotlib.pylab as pylab
#%matplotlib inline
pd.options.display.mpl_style = 'default'
pylab.rcParams['figure.figsize'] = 12, 6
from dateutil import parser
import Quandl
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib2


# ## Get A BeautifulSoup Object

# In[110]:

class BloombergSearch:
    def __init__(self, search_term):
        self.search_term = search_term
        self.url_page1 = ('http://www.bloomberg.com/search?query=' + str(self.search_term))
        self.curr_soup = BeautifulSoup(urllib2.urlopen(self.url_page1).read())
    
    
    def get_search_soup(self):
        url =  self.url_page1
        soup = self.get_soup(url)
        return soup
    def get_soup(self, url):
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        return soup
    def get_search_page_links(self, num_pages):
        article_list = []
        for i in range(1, num_pages + 1):
            temp_soup = self.get_soup(self.url_page1 + str('&page=') + str(i))
            for result in temp_soup.find_all('h1'):
                try:
                    if 'video' in result.a['href']:
                        continue
                    if 'http' in result.a['href']:
                        #print item.a['href']
                        article_list.append(result.a['href'])
                    else:
                        #print 'http://www.bloomberg.com/' + item.a['href']
                        article_list.append('http://www.bloomberg.com/' + result.a['href'])
                except:
                    continue
            #print 'Added page=' + str(i)
        return article_list
    
    def get_post_body(self, article_soup = self.curr_soup):
        final_text = ""
        self.curr_soup = article_soup
        query = article_soup.find_all('div',  class_="article-body__content")
        for item in query:
            for text in item.find_all('p'):
                final_text = final_text + '\n\n' + str(text.text.encode('utf-8'))
        if final_text == "":
            return 0
        return final_text
    
    def get_post_date(self, article_soup = self.curr_soup):
        final_text = ""
        self.curr_soup = article_soup
        result = article_soup.find('time', class_ = "published-at")
        try:
            return result['datetime']
        except:
            return None
    
    def get_post_author(self, article_soup = self.curr_soup):
        final_text = ""
        self.curr_soup = article_soup
        result = article_soup.find('a', class_ = "author-link")
        try:
            return result.text.lstrip().rstrip()
        except:
            return None
    
    def get_post_title(self, article_soup = scurr_soup):
        final_text = ""
        self.curr_soup = article_soup
        result = article_soup.find('title')
        try:
            return result.text.lstrip().rstrip()
        except:
            return None
    
    def make_info(self, pages = 1):
        final_df = pd.DataFrame()
        for url in self.get_search_page_links(pages):
            body = self.get_post_body(url)
            title = self.get_post_body()
            author = self.get_post_author()
            date = self.get_post_date()
            temp_series = pd.Series([title, author, date, body])
            final_df= final_df.append(temp_series, ignore_index = True)
        final_df.columns = ['title', 'author', 'date', 'text']
        return final_df


# In[ ]:




# In[100]:

bloom_obj = BloombergSearch('apple')


# In[102]:

temp = bloom_obj.make_info(3)
print len(url_list)
temp


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




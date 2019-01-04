from get_page import simple_get
from bs4 import BeautifulSoup
import re
import collections
import os
import time

def get_links(html):
    links = []
    for p in html.select('a'):
        if p['href'].find('view=article&aid') > -1 and p.text != 'read more':
            links.append('http://www.sermonindex.net/modules/articles/' + p['href'])
    return links
    
def get_sermon_from_link(url):
    page = simple_get(url)
    html = BeautifulSoup(page, 'html.parser')
    tables = html.select('table')
    sermon_text = tables[10].text;
    start_sermon = sermon_text.find('Open as PDF')
    body = sermon_text[start_sermon+11:].strip()
    
    title = sermon_text[:start_sermon].split(':')[2].strip()
    title = title.replace(' ', '_')
    title = title.replace('\"', '')
    title = title.replace('?', '')
    title = title.replace(',', '')
    
    sermon = collections.namedtuple('Sermon', ['title', 'body'])
    sermon.title = title
    
    sermon.body = body
    return sermon
    
def get_sermons(speaker, url):
    sermon_index = simple_get(url)
    html = BeautifulSoup(sermon_index, 'html.parser')
    links = get_links(html)
    os.chdir('./' + speaker) 
    for link in links:
        sermon = get_sermon_from_link(link)
        filename = speaker + '_'  + sermon.title + '.txt'
        with open(filename,'w') as f:
            f.write(sermon.body)
        print('Created ', sermon.title)
        time.sleep(.5)
    os.chdir('..')
        
def get_sermons_timed(speaker, url):
    for i in range(16,30):
        get_sermons(speaker, url+str(i))



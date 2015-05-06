# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:04:01 2015

@author: misha
"""

import urllib2, csv
from bs4 import BeautifulSoup
#from unicodedata  import normalize

page = urllib2.urlopen("https://meta.wikimedia.org/wiki/Special:SiteMatrix").read()
soup = BeautifulSoup(page)
lang_table = soup.find('table', id="mw-sitematrix-table")
#print lang_table

out = open('wiki_lang_codes.csv', 'wb')
writer = csv.DictWriter(out, fieldnames = ['language', 'link'], dialect='excel')
writer.writeheader()

for row in lang_table.findAll('tr'):
    try:
        lang = row.findAll('td')[1].text
        link = row.findAll('td')[1].a.get('href')
        print lang, link
        writer.writerow({'language': lang, 'link': link[2:]})
    except IndexError:
        print 'not a language row:', row 
        
out.close()
        

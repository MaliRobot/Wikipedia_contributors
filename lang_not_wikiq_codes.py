# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:04:01 2015

@author: misha
"""

import urllib2, csv
from bs4 import BeautifulSoup
#from unicodedata  import normalize

def get_wiki_langs():
    page = urllib2.urlopen("https://meta.wikimedia.org/wiki/Special:SiteMatrix").read()
    soup = BeautifulSoup(page)
    lang_table = soup.find('table', id="mw-sitematrix-table")
    #print lang_table
    
    wiki = []
    for row in lang_table.findAll('tr'):
        try:
            r = row.contents
    
            lang = r[0].text
            code = r[1].text
            link = r[1].find_all('a')[0]
            print code, link['href'][2:]
            wiki.append((lang, code, link['href'][2:]))
            #writer.writerow({'language': lang, 'link': link[2:]})
        except IndexError:
            print 'not a language row:', row 
    return wiki

def get_wiktio_langs():
    page = urllib2.urlopen("http://stats.wikimedia.org/wiktionary/EN/Sitemap.htm").read()
    soup = BeautifulSoup(page)
    wiktionaries = soup.find('table', id="table1")
    #print str(wiktionaries)
    wiktio_langs = []
    
    for row in wiktionaries.findAll('tr')[1:-1]:
        try:
            lang = row.findAll('td')[2].text
            wiktio_langs.append(lang)
        except IndexError:
            print 'not a language row:', row 
    
    wiktio_langs = wiktio_langs[1:-16]
    print wiktio_langs
    return wiktio_langs

def compare_langs(wiki, wiktio_langs):
    out = open('wiki_wikti_lang_diff.txt', 'wb')
    writer = csv.DictWriter(out, fieldnames = ['language', 'code', 'link'], dialect='excel')
    writer.writeheader()
    
    #wiki_codes = set(wiki)
    wiktio_codes = set(wiktio_langs)
    
    diff = []
    
    for l in wiki[1:-1]:
        if l[1] not in wiktio_codes:
            diff.append(l[1])
            try:
                writer.writerow({'language': l[0].encode('utf-8'), 'code': l[1].encode('utf-8'), 'link': l[2].encode('utf-8')})
            except UnicodeEncodeError:
                print l    
                
    print diff            
            
    out.close()
    return diff

def find_diff():
    wiki = get_wiki_langs()
    wiktio = get_wiktio_langs()
    result = compare_langs(wiki, wiktio)
    return result

if __name__ == "__main__":
    wiki = get_wiki_langs()
    wiktio = get_wiktio_langs()
    result = compare_langs(wiki, wiktio)
        

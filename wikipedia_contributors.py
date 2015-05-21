# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel

Extract users of active wikipedia languages. Save them to csv file.
"""

import urllib2, csv
from sys import argv
from bs4 import BeautifulSoup
import lang_not_wikiq_codes

def get_wiki_languages():
    """
    Find all active languages on Wikipedia and get their language code. 
    """
    page = urllib2.urlopen("http://stats.wikimedia.org/EN/Sitemap.htm").read()
    soup = BeautifulSoup(page, "html.parser")
    wikies = soup.find('table', id="table2")
    #print str(wikies)
    wiki_langs = []
    
    for row in wikies.findAll('tr'):
        try:
            lang = row.findAll('td')[4].text
            wiki_langs.append(lang)
        except IndexError:
            print 'not a language row:', row 
    
    wiki_langs = wiki_langs[3:]
    
    print wiki_langs, len(set(wiki_langs))
    return wiki_langs

def create_links(wiki_langs):
    """
    Using language codes generate wikipedia links for statistics.
    Test generated links.
    """
    baselink = ['http://stats.wikimedia.org/EN/TablesWikipedia', '.htm']
    
    wiki_links = []
    for w in wiki_langs:
        if '-' in w:
            w = w.replace('-','_')
        link = baselink[0] + w.upper() + baselink[1]
        wiki_links.append([link, w])
        
    print wiki_links
    

# check if links are valid (they still could be bad, though)
    for l in wiki_links:
        link = l[0]
        try:
            urllib2.urlopen(link)
        except urllib2.HTTPError, e:
            print e.code, link
        except urllib2.URLError, e:
            print e.args, link
        except HTTPError:
            print link
        
    return wiki_links
    
def get_contributors(wiki_links):
    """
    Using links, find all users from each language page. Save them to csv file.
    """
    #wiki_links = [['http://stats.wikimedia.org/EN/TablesWikipediaEO.htm', 'en', '0']]        
    
    out = open('wiki_contributors.csv', 'wb')
    writer = csv.DictWriter(out, fieldnames = ['username', 'edits, articles, 30 dy', 'edits, other, 30 dy', 'creates, articles, 30 dy', 'creates, other, 30 dy', 'link', 'lang'], dialect='excel')
    writer.writeheader()
    
    errors = []
    
    for l in wiki_links:
        lang_link = l[0]
        try:
            page = urllib2.urlopen(lang_link).read()
            soup = BeautifulSoup(page, "html.parser")  
            user_table = soup.find('table', id="table2")
    
            try:
                rows = user_table.findAll('tr')[3:]
            except AttributeError, e:
                print l[1], e
                continue
            for r in rows:
                name = r.a.text
                name = name.encode('utf-8')
                link = r.a.get('href')
                link = link.encode('utf-8')
                user_data = r.findAll('td', { "class" : "rbg" })
                user_data = [x.text for x in user_data]
                try:
                    writer.writerow({'username': name, 'edits, articles, 30 dy': user_data[0], 'edits, other, 30 dy': user_data[1], 'creates, articles, 30 dy': user_data[2], 'creates, other, 30 dy': user_data[3], 'link': link, 'lang': l[1]})
                except UnicodeEncodeError:
                    errors.append([name, user_data[0], user_data[1], user_data[2], user_data[3], link, l[1]])
                except IndexError:
                    print name, user_data, link
        except Exception as e:
            print e, l, '\n'
                
    out.close()
    
    for e in errors:
        print e[0]
    print '*******************************'
    for e in errors:
        print e[1]
    print '*******************************'
    for e in errors:
        print e[2]
    print '*******************************'
    for e in errors:
        print e[3]
    print '*******************************'
    for e in errors:
        print e[4]
    print '*******************************'
    for e in errors:
        print e[5]
    print '*******************************'
    for e in errors:
        print e[6]
        
    return 'Done.'
    
if __name__ == "__main__":  
    if len(argv) > 1:
        if argv[1] == 'diff':
            codes = lang_not_wikiq_codes.find_diff()
            print "DIFFERENCE:", codes
    else:
        codes = get_wiki_languages()
    links = create_links(codes)
    get_contributors(links)
    

    
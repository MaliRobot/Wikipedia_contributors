# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel

Extract users of active wikipedia languages. Save them to csv file.
"""

import urllib2, csv, filecmp, os
from datetime import datetime
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
    print 'DAAAAATEEEEEEE', datetime.now()
    date = str(datetime.now())[0:10]
    filename = 'wikipedia_contributors_%s.csv' % (date)
    if os.path.exists(filename):
        filename = filename[:-4] + 'D' + '.csv'
       
    out = open(filename, 'wb')
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
        
    return 1
    
def find_csv():
    csv = []
    for f in os.listdir(os.getcwd()):
        if f.startswith("wikipedia_contributors") and f.endswith(".csv"):
            csv.append(f)
    return csv
    
if __name__ == "__main__":  
    """
    Either make a list of Wikipedia languages codes not present on Wiktionary 
    by calling find_diff from lang_not_wikiq_codes file or if no
    argument is given just get all languages codes from Wikipedia stats page and
    make a list of contributors from most active languages on Wikipedia. 
    """
    files = find_csv()
    
    if len(files) == 0:
        print "No wikipedia contributors list was found in the directory."
    else:
        latest = max(files, key=os.path.getctime)
        date = datetime.fromtimestamp(os.path.getctime(latest))
        print 'Most recent list of Wiktionary contributors was generated on:', date
        
    do = ''
    while True:
        do = raw_input('Do you want to get a new list (y/n)? ')
        if do == 'y' or do == 'n':
            break
        
    if do == 'y':
        do = ''
        
        while True:
            do = raw_input('Do you want get only languages not on Wiktionary (y/n)? ')
            if do == 'y' or do == 'n':
                break
            
        if do == 'y':
            codes = lang_not_wikiq_codes.find_diff()
        else:
            codes = get_wiki_languages()
            
        links = create_links(codes)
        if get_contributors(links) == 1:
            updated_files = find_csv()
            
            if len(updated_files) == 0:
                print "No files to compare."
            else:
                latest2 = max(updated_files, key=os.path.getctime)
                res = filecmp.cmp(latest, latest2, shallow = False)
                
                if res == True:
                    print 'No new data.'
                else:
                    print 'New contributors info acquired.'
    else:
        print "Thank you, have a nice and productive day!"
    
    
    
    

    
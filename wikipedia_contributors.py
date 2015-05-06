# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel
"""

import urllib2, csv
from bs4 import BeautifulSoup
#from unicodedata  import normalize

page = urllib2.urlopen("http://stats.wikimedia.org/EN/Sitemap.htm").read()
soup = BeautifulSoup(page)
wikies = soup.find('table', id="table2")
#print str(wikies)
wiki_langs = []
step = 0
for row in wikies.findAll('tr'):
    try:
        lang = row.findAll('td')[4].text
        wiki_langs.append(lang)
    except IndexError:
        print 'not a language row:', row 

wiki_langs = wiki_langs[3:]

print wiki_langs, len(set(wiki_langs))

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

#wiki_links = [['http://stats.wikimedia.org/EN/TablesWikipediaEO.htm', 'en', '0']]        

out = open('wiki_contributors.csv', 'wb')
writer = csv.DictWriter(out, fieldnames = ['username', 'edits, articles, 30 dy', 'edits, other, 30 dy', 'creates, articles, 30 dy', 'creates, other, 30 dy', 'link', 'lang'], dialect='excel')
writer.writeheader()

errors = []

for l in wiki_links:
    lang_link = l[0]   
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
            
out.close()

#for e in errors:
#    print e[0]
#print '*******************************'
#for e in errors:
#    print e[1]
#print '*******************************'
#for e in errors:
#    print e[2]
#print '*******************************'
#for e in errors:
#    print e[3]
#print '*******************************'
#for e in errors:
#    print e[4]
#print '*******************************'
#for e in errors:
#    print e[5]
#print '*******************************'
#for e in errors:
#    print e[6]

    
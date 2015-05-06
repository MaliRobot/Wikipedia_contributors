# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel
"""

import urllib2, csv
from bs4 import BeautifulSoup

page = urllib2.urlopen("http://stats.wikimedia.org/wiktionary/EN/Sitemap.htm").read()
soup = BeautifulSoup(page)
wiktionaries = soup.find('table', id="table1")
#print str(wiktionaries)
wiktio_langs = []
step = 0
for row in wiktionaries.findAll('tr'):
    try:
        lang = row.findAll('td')[2].text
        wiktio_langs.append(lang)
    except IndexError:
        print 'not a language row:', row 
    step += 1
    if step == 128:
        break
wiktio_langs = wiktio_langs[2:]

baselink = ['http://stats.wikimedia.org/wiktionary/EN/TablesWikipedia', '.htm']

wiktio_links = []
for w in wiktio_langs:
    if '-' in w:
        w = w.replace('-','_')
    link = baselink[0] + w.upper() + baselink[1]
    wiktio_links.append([link, w])
    
print wiktio_links

# check if links are valid (they still could be bad, though)
for l in wiktio_links:
    link = l[0]
    try:
        urllib2.urlopen(link)
    except urllib2.HTTPError, e:
        print e.code, link
    except urllib2.URLError, e:
        print e.args, link

#wiktio_links = [['http://stats.wikimedia.org/wiktionary/EN/TablesWikipediaJA.htm', 'en', '0']]        

out = open('C:/Users/Tao Steel/Documents/Python Scripts/contributors.csv', 'wb')
writer = csv.DictWriter(out, fieldnames = ['username', 'edits, articles, 30 dy', 'edits, other, 30 dy', 'creates, articles, 30 dy', 'creates, other, 30 dy', 'link', 'lang'], dialect='excel')
writer.writeheader()
out = open('alahakbar.txt', 'w')

errors = []

for l in wiktio_links:
    lang_link = l[0]
    page = urllib2.urlopen(lang_link).read()
    soup = BeautifulSoup(page)
    user_table = soup.find('table', id="table2")
    rows = user_table.findAll('tr')[3:]
    for r in rows:
        name = r.a.text
        name = name.encode('utf8', 'replace')
        link = r.a.get('href')
        link = link.encode('utf8', 'replace')
        user_data = r.findAll('td', { "class" : "rbg" })
        user_data = [x.text for x in user_data]
        try:
#            writer.writerow({'username': name, 'edits, articles, 30 dy': user_data[0], 'edits, other, 30 dy': user_data[1], 'creates, articles, 30 dy': user_data[2], 'creates, other, 30 dy': user_data[3], 'link': link, 'lang': l[1]})
            out.write(','.join([name, str(user_data[0]), str(user_data[1]), str(user_data[2]), str(user_data[3]), link, l[1]]))
        except UnicodeDecodeError:
            errors.append([name, user_data[0], user_data[1], user_data[2], user_data[3], link, l[1]])
print errors
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
#for e in errors:
#    print e[5]
#for e in errors:
#    print e[6]

    
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel

Wiktionary contributors
"""

import urllib2, csv, os, filecmp
from datetime import datetime
from bs4 import BeautifulSoup

def get_active_languages():
    """
    Open wiktionary statistics page and find languages with active users in the
    last 30 days.
    
    """
    page = urllib2.urlopen("http://stats.wikimedia.org/wiktionary/EN/Sitemap.htm").read()
    soup = BeautifulSoup(page, "html.parser")
    wiktionaries = soup.find('table', id="table2")
    #print str(wiktionaries)
    wiktio_langs = []

    for row in wiktionaries.findAll('tr')[1:-1]:
        try:
            lang = row.findAll('td')[2].text
            wiktio_langs.append(lang)
        except IndexError:
            print 'not a language row:', row, "\n"

    #print wiktio_langs
    
    baselink = ['http://stats.wikimedia.org/wiktionary/EN/TablesWikipedia', '.htm']
    
    # form link for statistics page for each found language
    wiktio_links = []
    for w in wiktio_langs:
        if '-' in w:
            w = w.replace('-','_')
        link = baselink[0] + w.upper() + baselink[1]
        wiktio_links.append([link, w])
    
    #print wiktio_links
    return wiktio_links

def get_contributors(wiktio_links):
    """
    Form links and use them to find lists of most active users for 
    Wiktionaries per each language.
    Save data in csv file.
    """
    # check if links are valid (they still could be bad, though)
    for l in wiktio_links:
        link = l[0]
        try:
            urllib2.urlopen(link)
        except urllib2.HTTPError, e:
            print "HTTP error!"
            print e.code, link, "\n"
        except urllib2.URLError, e:
            print "URL Error"
            print e.args, link, "\n"
    
    #wiktio_links = [['http://stats.wikimedia.org/wiktionary/EN/TablesWikipediaJA.htm', 'en', '0']]        
    
    print 'DAAAAATEEEEEEE', datetime.now()
    date = str(datetime.now())[0:10]
    filename = 'wiktionary_contributors_%s.csv' % (date)
    if os.path.exists(filename):
        filename = filename[:-4] + 'D' + '.csv'
    out = open(filename, 'wb')
    writer = csv.DictWriter(out, fieldnames = ['username', 'edits, articles, 30 dy', 'edits, other, 30 dy', 'creates, articles, 30 dy', 'creates, other, 30 dy', 'link', 'lang'], dialect='excel')
    writer.writeheader()
    
    errors = []
    
    for l in wiktio_links:
        print l
        lang_link = l[0]
        page = urllib2.urlopen(lang_link).read()
        soup = BeautifulSoup(page, "html.parser")
        user_table = soup.find('table', id="table2")
        try:
            rows = user_table.findAll('tr')[3:]
        except AttributeError as e:
            print "Error while exracting data from the table", l
            print e, l[1], "\n"
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
                print "Index Error!"
                print "user_data:", user_data, "user:", name, "language:", l, "\n"
    return 1
#    for e in errors:
#        print e[0]
#    print '*******************************'
#    for e in errors:
#        print e[1]
#    print '*******************************'
#    for e in errors:
#        print e[2]
#    print '*******************************'
#    for e in errors:
#        print e[3]
#    print '*******************************'
#    for e in errors:
#        print e[4]
#    for e in errors:
#        print e[5]
#    for e in errors:
#        print e[6]

def find_csv():
    csv = []
    for f in os.listdir(os.getcwd()):
        if f.startswith("wiktionary_contributors") and f.endswith(".csv"):
            csv.append(f)
    return csv

if __name__ == "__main__":
    files = find_csv()
    if len(files) > 0:
        latest = max(files, key=os.path.getctime)
        date = datetime.fromtimestamp(os.path.getctime(latest))
        print 'Most recent list of Wiktionary contributors was generated on:', date
    else:
        print "no list of wiktionary contributors was found in the directory"
    do = ''
    while True:
        do = raw_input('Do you want to get a new list (y/n)? ')
        if do == 'y' or do == 'n':
            break
    if do == 'y':
        langs = get_active_languages()
        if get_contributors(langs) == 1:
            updated_files = find_csv()
            if len(updated_files) > 0:
                latest2 = max(updated_files, key=os.path.getctime)
                res = filecmp.cmp(latest, latest2, shallow = False)
                if res == True:
                    print 'No new data.'
                else:
                    print 'New contributors info acquired.'
            else:
                print "no files to compare."
    else:
        print "Thank you, have a nice and productive day!"
#    for c in cvs:
#        t = os.path.getctime(c) 
#        print datetime.fromtimestamp(t)
#        print datetime.now() - datetime.fromtimestamp(t)

    
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:29:14 2015

@author: Tao Steel
"""

import urllib2, csv
from bs4 import BeautifulSoup
#from unicodedata  import normalize


wiki_langs = [u'aa', u'ab', u'ace', u'ak', u'als', u'an', u'arc', u'arz', u'as',
              u'av', u'ba', u'bar', u'bat-smg', u'bcl', u'be-x-old', u'bh', u'bi',
              u'bjn', u'bm', u'bo', u'bpy', u'bug', u'bxr', u'cbk-zam', u'cdo',
              u'ce', u'ceb', u'ch', u'cho', u'chy', u'ckb', u'cr', u'crh', u'cu',
              u'cv', u'diq', u'dsb', u'dz', u'ee', u'eml', u'ext', u'ff', u'fiu-vro',
              u'frp', u'frr', u'fur', u'gag', u'gan', u'glk', u'got', u'hak',
              u'haw', u'hif', u'ho', u'hsb', u'ht', u'hz', u'ia', u'ie', u'ig',
              u'ii', u'ik', u'ilo', u'iu', u'kaa', u'kab', u'kbd', u'kg', u'ki',
              u'kj', u'koi', u'kr', u'krc', u'ksh', u'kv', u'kw', u'lad', u'lbe',
              u'lez', u'lg', u'lij', u'lmo', u'ltg', u'mai', u'map-bms', u'mdf',
              u'mh', u'mhr', u'min', u'mo', u'mr', u'mrj', u'mt', u'mus', u'mwl',
              u'myv', u'mzn', u'nap', u'nds-nl', u'ne', u'new', u'ng', u'nov',
              u'nrm', u'nso', u'nv', u'ny', u'om', u'os', u'pa', u'pag', u'pam',
              u'pap', u'pcd', u'pdc', u'pfl', u'pi', u'pih', u'pms', u'pnt',
              u'qu', u'rm', u'rmy', u'rn', u'roa-tara', u'rue', u'rw', u'sah',
              u'sc', u'sco', u'sd', u'se', u'si', u'sn', u'srn', u'ss', u'st',
              u'stq', u'szl', u'tet', u'to', u'ts', u'tum', u'tw', u'ty', u'tyv',
              u'udm', u've', u'vec', u'vep', u'vls', u'war', u'wuu', u'xal', u'xh',
              u'xmf', u'yo', u'za', u'zea', u'zh-classical', u'zh-yue', u'zu']



baselink = ['http://stats.wikimedia.org/EN/TablesWikipedia', '.htm']

wiki_links = []
for w in wiki_langs:
    if '-' in w:
        w = w.replace('-','_')
    link = baselink[0] + w.upper() + baselink[1]
    wiki_links.append([link, w])
    
print wiki_links

good_links = []
# check if links are valid (they still could be bad, though)
for l in wiki_links:
    link = l[0]
    try:
        urllib2.urlopen(link)
        good_links.append(l)
    except urllib2.HTTPError, e:
        print e.code, link
    except urllib2.URLError, e:
        print e.args, link

wiki_links = good_links

#wiki_links = [['http://stats.wikimedia.org/EN/TablesWikipediaEO.htm', 'en', '0']]        

out = open('wiki_contributors.txt', 'wb')
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

    
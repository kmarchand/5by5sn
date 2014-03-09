#!/usr/bin/python
#
# Alfred2 workflow for 5by5 show list (http://5by5.tv/)
#   K. Marchand.  2014
#

import urllib2
import re
import xml.etree.ElementTree as ET
import HTMLParser
import sys
import pickle
import os
from datetime import datetime, timedelta

base = 'http://5by5.tv/broadcasts/'
root = ET.Element('items')

# For better performance, the list of shows is stored in /tmp
# and only refreshed if the local list is over 30 minutes old

shows_p = '/tmp/5by5shows.p'

if os.path.exists(shows_p):
    lastmod = datetime.fromtimestamp(os.stat(shows_p).st_mtime)
else:
    lastmod = datetime.now() - timedelta(minutes=45)

if lastmod < datetime.now() - timedelta(minutes=30):

    shows = []

    try:
        req = urllib2.Request(base)
        html = urllib2.urlopen(req).read()
    except:
        root = ET.Element('items')
        item = ET.SubElement(root, 'item')

        title = ET.SubElement(item, 'title')
        title.text = "5by5 Show Name Lookup"

        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = "Unable to load %s" % base

        icon = ET.SubElement(item, 'icon')
        icon.text = '5by5.png'

        print ET.tostring(root)
        sys.exit(0)

    for match in re.finditer(
        "<div class=\"broadcast\">.*?<h3><a href=\"/(.*?)\">(.*?)</a></h3>",
            html, re.S):
        shortname = unicode(match.group(1), 'utf-8')
        showtitle = unicode(match.group(2), 'utf-8')
        shows.append((showtitle, shortname))

    pickle.dump(shows, open(shows_p, 'wb'))

else:

    shows = pickle.load(open(shows_p, 'rb'))

h = HTMLParser.HTMLParser()

q = str('{query}'.lower())

if len(shows) != 0:

    for showtitle, shortname in shows:

        if not os.path.exists('/tmp/%s.jpg' % shortname):
            try:
                art_url = re.search(
                    '%s.*?src="(.*?.jpg)"' % shortname, html, re.S).group(1)
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                headers = {'User-Agent': user_agent}
                imgreq = urllib2.Request(art_url, headers=headers)
                imgdata = urllib2.urlopen(imgreq).read()
                with open('/tmp/%s.jpg' % shortname, 'wb') as imgfile:
                    imgfile.write(imgdata)
            except:
                pass

            continue

        if q not in shortname.lower() + ' ' + showtitle.lower():
            continue

        item = ET.SubElement(root, 'item')
        item.set('uid', shortname)
        item.set('arg', shortname)

        title = ET.SubElement(item, 'title')
        title.text = h.unescape(showtitle)

        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = 'http://5by5.tv/%s/' % shortname

        icon = ET.SubElement(item, 'icon')
        if os.path.exists('/tmp/%s.jpg' % shortname):
            icon.text = '/tmp/%s.jpg' % shortname
        else:
            icon.text = '5by5.png'

    print ET.tostring(root)

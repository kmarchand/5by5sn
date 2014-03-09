#!/usr/bin/python
#
# Alfred2 workflow for 5by5 podcast show notes (http://5by5.tv/)
#   K. Marchand.  2014
#

import urllib2
import re
import xml.etree.ElementTree as ET
import HTMLParser
import os
import sys

podcast = '{query}'.lower()
base = 'http://5by5.tv/%s/' % podcast
root = ET.Element('items')

try:
    req = urllib2.Request(base)
    html = urllib2.urlopen(req).read()
except:
    item = ET.SubElement(root, 'item')

    title = ET.SubElement(item, 'title')
    title.text = "5by5 Show Notes"

    subtitle = ET.SubElement(item, 'subtitle')
    subtitle.text = "%s not found on 5by5.tv" % podcast

    icon = ET.SubElement(item, 'icon')
    icon.text = '5by5.png'

    print ET.tostring(root)
    sys.exit(0)

ep_nums = []

for match in re.finditer('%s/(\d[0-9]{0,3})' % podcast, html, re.S):
    ep_num = match.group(1)
    if ep_num.isdigit():
        ep_nums.append(int(ep_num))

if len(ep_nums) != 0:

    last_ep = str(max(ep_nums))
    ep_req = urllib2.Request(base + last_ep)
    ep_html = urllib2.urlopen(ep_req).read()
    h = HTMLParser.HTMLParser()

    try:
        ep_title = unicode(re.search(
            '<title>(.*?)</title>', ep_html, re.S).group(1), 'utf-8')
        ep_title = h.unescape(ep_title)
    except:
        ep_title = u''

    if not os.path.exists('/tmp/%s.jpg' % podcast):

        try:
            art_url = re.search(
                'broadcast_art.*?src="(.*?.jpg)"', ep_html, re.S).group(1)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            imgreq = urllib2.Request(art_url, headers=headers)
            imgdata = urllib2.urlopen(imgreq).read()
            with open('/tmp/%s.jpg' % podcast, 'wb') as imgfile:
                imgfile.write(imgdata)
        except:
            pass

    links = []

    try:
        link_html = re.search(
            "<div id=\"episode_links\"(.*?)</div>", ep_html, re.S).group(1)
    except:
        link_html = ''

    for match in re.finditer('<a.*?href="(.*?)".*?>(.*?)</a>', link_html):
        url = unicode(match.group(1), 'utf-8')
        title = unicode(match.group(2), 'utf-8')
        links.append((title, url))

    if len(links) != 0:

        for urltitle, url in links:

            item = ET.SubElement(root, 'item')
            item.set('uid', url)
            item.set('arg', url)

            title = ET.SubElement(item, 'title')
            title.text = h.unescape(urltitle)

            subtitle = ET.SubElement(item, 'subtitle')
            subtitle.text = ep_title

            icon = ET.SubElement(item, 'icon')

            if os.path.exists('/tmp/%s.jpg' % podcast):
                icon.text = '/tmp/%s.jpg' % podcast
            else:
                icon.text = '5by5.png'

        print ET.tostring(root)

    else:

        item = ET.SubElement(root, 'item')

        title = ET.SubElement(item, 'title')
        title.text = "No show notes found"

        subtitle = ET.SubElement(item, 'subtitle')
        subtitle.text = ep_title

        icon = ET.SubElement(item, 'icon')
        icon.text = '5by5.png'

        print ET.tostring(root)

else:

    item = ET.SubElement(root, 'item')

    title = ET.SubElement(item, 'title')
    title.text = "No episodes found for %s" % podcast

    subtitle = ET.SubElement(item, 'subtitle')
    subtitle.text = base

    icon = ET.SubElement(item, 'icon')
    icon.text = '5by5.png'

    print ET.tostring(root)

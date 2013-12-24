'''
    httpStreamer XBMC Plugin
    Copyright (C) 2013 dmdsoftware

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import urllib
import cgi
import re

import xbmc, xbmcgui, xbmcplugin, xbmcaddon


        
def log(msg, err=False):
    if err:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), xbmc.LOGERROR)    
    else:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), xbmc.LOGDEBUG)    

def parse_query(query):
    queries = cgi.parse_qs(query)
    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    q['mode'] = q.get('mode', 'main')
    return q

def addVideo(url, infolabels, img='', fanart='', total_items=0, 
                   cm=[], cm_replace=False):
    infolabels = decode_dict(infolabels)
    log('adding video: %s - %s' % (infolabels['title'].decode('utf-8','ignore'), url))
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty('IsPlayable', 'true')
    listitem.setProperty('fanart_image', fanart)
    if cm:
        listitem.addContextMenuItems(cm, cm_replace)
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, 
                                isFolder=False, totalItems=total_items)


#http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data).strip()

def decode_dict(data):
    for k, v in data.items():
        if type(v) is str or type(v) is unicode:
            data[k] = decode(v)
    return data



plugin_url = sys.argv[0]
plugin_handle = int(sys.argv[1])
plugin_queries = parse_query(sys.argv[2][1:])

addon = xbmcaddon.Addon(id='plugin.video.cacheStreamer')
#plugin_path = addon.getAddonInfo('path')

cache_location = addon.getSetting('cache_location')
cache_file = addon.getSetting('cache_file')
user_agent = addon.getSetting('user_agent')

 
log('plugin google authorization: ' + cacheStreamer.returnHeaders())
log('plugin url: ' + plugin_url)
log('plugin queries: ' + str(plugin_queries))
log('plugin handle: ' + str(plugin_handle))

mode = plugin_queries['mode']

#dump a list of videos available to play
#play a URL that is passed in (presumely requires authorizated session)
if mode == 'play':
    url = plugin_queries['url']
    log('play url: ' + url)


    header = { 'User-Agent' : user_agent}

    log('url = %s header = %s' % (url, header)) 
    req = urllib2.Request(url, None, header)

    log('loading ' + url) 
    chunk = 16 * 1024
    try:
      response = urllib2.urlopen(req)
    except urllib2.URLError, e:
      log(str(e), True)

    count = 0
    item = xbmcgui.ListItem(path=url)

    with open(file, '/tmp/test.mp4') as fp:
      while True:
        if count == 20:
           xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item) 
        chunk = req.read(CHUNK)
        if not chunk: break
        fp.write(chunk)
        count = count + 1
     
xbmcplugin.endOfDirectory(plugin_handle)


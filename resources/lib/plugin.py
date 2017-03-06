# -*- coding: utf-8 -*-

import routing
import sys
import urllib
import urlparse

from resources.data import config
from resources.lib.guide import show_guide
from resources.lib.youtube import get_live_video_id_from_channel_id
from resources.lib.kodiUtilities import kodiJsonRequest
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent

plugin = routing.Plugin()
setContent(plugin.handle, 'videos')


@plugin.route('/')
def index():
    video_id = get_live_video_id_from_channel_id(config.CHANNEL_ID)
    thumbnail = "https://i.ytimg.com/vi/%s/maxresdefault_live.jpg" % video_id

    # Get cached thumb from database to ensure it's removed for the livestream
    response = kodiJsonRequest({'jsonrpc': '2.0', 'id': 0, 'method': 'Textures.GetTextures',
                                'params': {'filter': {'operator': 'contains', 'field': 'url', 'value': 'https://i.ytimg.com/vi/%/maxresdefault_live.jpg'},
                                           'properties': ['imagehash', 'url']}})

    # Remove cached thumb and grab a new one
    if len(response['textures']) > 0:
        kodiJsonRequest({'jsonrpc': '2.0', 'id': 0, "method": "Textures.RemoveTexture",
                         "params": {"textureid": response['textures'][0]['textureid']}})

    url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
    li = ListItem(label='Live',
                  thumbnailImage=thumbnail)
    li.setProperty('isPlayable', 'true')
    addDirectoryItem(plugin.handle, url, li)

    url = "plugin://plugin.video.youtube/user/%s/" % config.CHANNEL_ID
    addDirectoryItem(plugin.handle, url, ListItem('Mediathek'), True)

    url = "plugin://plugin.video.youtube/channel/%s/" % config.LETS_PLAY_CHANNEL_ID
    addDirectoryItem(
        plugin.handle, url, ListItem('Let\'s-Play-Mediathek'), True)

    addDirectoryItem(
        plugin.handle, plugin.url_for(guide), ListItem('Sendeplan'), True)

    endOfDirectory(plugin.handle)


@plugin.route('/guide')
def guide():
    guide_items = show_guide()

    for guide_item in guide_items:
        li = ListItem(guide_item)
        addDirectoryItem(plugin.handle, '', li)
    endOfDirectory(plugin.handle)


def run():
    plugin.run()

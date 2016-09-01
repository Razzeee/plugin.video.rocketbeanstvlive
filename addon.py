import sys
import locale
import urllib
import urlparse

import xbmc
import xbmcgui
import xbmcplugin

from resources.data import config
from resources.lib import guide
from resources.lib import youtube

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

if mode is None:
    li = xbmcgui.ListItem('Live')

    video_id = youtube.get_live_video_id_from_channel_id(config.CHANNEL_ID)
    li.setProperty('isPlayable', 'true')
    url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id

    xbmcplugin.addDirectoryItem(addon_handle, url, li)

    li = xbmcgui.ListItem('Mediathek')
    url = "plugin://plugin.video.youtube/user/%s/" % config.CHANNEL_ID
    xbmcplugin.addDirectoryItem(addon_handle, url, li, True)

    li = xbmcgui.ListItem('Let\'s-Play-Mediathek')
    url = "plugin://plugin.video.youtube/channel/%s/" % config.LETS_PLAY_CHANNEL_ID
    xbmcplugin.addDirectoryItem(addon_handle, url, li, True)

    li = xbmcgui.ListItem('Sendeplan')
    url = build_url({'mode': 'guide'})
    xbmcplugin.addDirectoryItem(addon_handle, url, li, True)

elif mode[0] == 'guide':
    guide_items = guide.show_guide(addon_handle)

    for guide_item in guide_items:
        li = xbmcgui.ListItem(guide_item)
        xbmcplugin.addDirectoryItem(addon_handle, '', li)

xbmcplugin.endOfDirectory(addon_handle)

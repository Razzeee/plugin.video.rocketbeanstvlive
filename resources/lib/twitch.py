import os,re
import xbmc,xbmcaddon,xbmcgui
from resources.lib import simple_requests as requests

addon = xbmcaddon.Addon()
home = addon.getAddonInfo('path').decode('utf-8')
image = xbmc.translatePath(os.path.join(home, 'icon.png'))
q = int(addon.getSetting('quality'))

class RBTV(object):

    def __init__(self):

        self.name    = 'Rocket Beans TV'
        self.channel = 'rocketbeanstv'
        self.access  = 'https://api.twitch.tv/api/channels/%s/access_token' % self.channel
        self.hls     = 'http://usher.twitch.tv/api/channel/hls/%s.m3u8' % self.channel
        self.params  = {'allow_source':'true', 'sig':'', 'token':''}

    def set_params(self):
        try:
            data = requests.get(self.access).json()
            self.params['sig']   = data['sig']
            self.params['token'] = data['token']
        except:
            pass

    def get_index(self):
        result = None
        y = [750000,1500000,3000000,6000000]
        z = y[q]
        list = []
        pattern = 'bandwidth=(\d+).*?\n(http.*?)$'
        try:
            data = requests.get(self.hls, params=self.params).text
            match = re.findall(pattern, data, re.I|re.M)
            if match:
                for b,u in match:
                    list.append({'bandwidth':int(b), 'url':u})
            if list:
                list = sorted(list, key=lambda k:k['bandwidth'])
                xbmc.log(msg=str(list), level=-1)
                for x in list:
                    if x['bandwidth'] < z:
                        index = x['url']
                    else:
                        break
                return index
        except:
            pass
        return result

    def play(self):
        self.set_params()
        index = self.get_index()
        if index:
            item  = xbmcgui.ListItem(self.name, thumbnailImage=image)
            xbmc.Player().play(index, listitem=item)

            xbmc.sleep(2000)
            if addon.getSetting('run_chat') == 'true':
                xbmc.executebuiltin(
                    "RunScript(script.ircchat, run_irc=True&nickname=%s&username=%s&password=%s&host=%s&channel=%s)"
                    %(addon.getSetting('nickname'), addon.getSetting('nickname'),
                    addon.getSetting('password'), 'irc.twitch.tv', self.channel)
                )

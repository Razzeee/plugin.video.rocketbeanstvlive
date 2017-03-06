# -*- coding: utf-8 -*-
#

import xbmc
import sys

if sys.version_info >= (2, 7):
    import json as json
else:
    import simplejson as json


def kodiJsonRequest(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)

    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))

    try:
        if 'result' in response:
            return response['result']
        return None
    except KeyError:
        xbmc.log("[%s] %s" % (params['method'], response['error']['message']))
        return None

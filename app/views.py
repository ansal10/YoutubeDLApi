# TODO: load cached URL for and append to bypass data "https://www.youtube.com/yts/jsbin/player_ias-vflIVQ4xT/en_US/base.js?disable_polymer=true"
import gzip
import json
import time
from StringIO import StringIO

import lzstring
import requests
from django.http import JsonResponse


def proxy_video_config(request):
    try:
        data = json.loads(request.body)
    except Exception as e:  # if content iz gzip enabled
        try:
            s = gzip.GzipFile(fileobj=StringIO(request.body)).read()
            data = json.loads(s)
        except Exception as e:
            data = lzstring.LZString.decompressFromBase64(request.body)
            data = json.loads(data)
    headers = {'content-type': "application/json"}
    res = requests.post("http://localhost:5005/api/v1/urls/proxy_config", data=json.dumps(data), headers=headers)
    return JsonResponse(json.loads(res.text))

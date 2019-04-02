import json
import zlib
from _ast import Dict
from urlparse import urlparse
import lzstring
import pytz
import requests
from django.http import JsonResponse

from YoutubeDLApi.settings import youtubedl_logger
from app.models import Video
from libs import youtube_dl
from datetime import datetime, timedelta
import time
from django.shortcuts import render
import yaml
import gzip
from StringIO import StringIO

expired_hours_dict = {
    'www.youtube.com': 6,
    'youtube.com': 6
}

url_dict = {}

# Create your views here.




def load_video_config(video_url) :
    video = Video.objects.filter(video_url=video_url).first()
    site = urlparse(video_url).netloc
    expire_hours = expired_hours_dict[site.lower()]
    if video and video.updated_at + timedelta(hours=expire_hours) > datetime.now(pytz.UTC):
        pass
    else:
        if video:
            video.delete()
        config = youtube_dl._real_main([video_url, "-F", "--no-check-certificate"])[0]
        config = json.dumps(config)
        video = Video.objects.create(video_url=video_url, video_config=config)

    expired_in = (video.updated_at + timedelta(hours=expire_hours) - datetime.now(pytz.UTC))
    expired_in = expired_in.seconds + expired_in.days*60*60*24
    return video, expired_in


def video_config(request):
    data = json.loads(request.body)
    video_url = data['video_url']
    video, expired_in = load_video_config(video_url)
    data = json.loads(video.video_config)
    data['expired_in'] = expired_in
    return JsonResponse({'data': data})


def video_format(request):
    data = json.loads(request.body)
    video_url = data['video_url']
    video, expired_in = load_video_config(video_url)
    config = json.loads(video.video_config)
    formats = config.get('format') or config.get('formats')
    for f in formats:
        f['expired_in'] = expired_in

    return JsonResponse({'data': formats})


# TODO: load cached URL for and append to bypass data "https://www.youtube.com/yts/jsbin/player_ias-vflIVQ4xT/en_US/base.js?disable_polymer=true"
def proxy_video_config(request):
    start_time = int(time.time() * 1000)

    try:
        data = json.loads(request.body)
    except Exception as e:  # if content iz gzip enabled
        try:
            s = gzip.GzipFile(fileobj=StringIO(request.body)).read()
            data = json.loads(s)
        except Exception as e:
            data = lzstring.LZString.decompressFromBase64(request.body)
            data = json.loads(data)


    video_id = data.get('video_id')
    video_url = "https://www.youtube.com/watch?v={}".format(video_id)
    bypass_data = data.get('bypass_data', {})
    urls = get_urls_dict()
    for url, data in urls.items():
        bypass_data[url] = data

    config = youtube_dl._real_main([video_url, "-F", "--no-check-certificate", "--bypass-content", json.dumps(bypass_data)])[0]
    end_time = int(time.time() * 1000)
    youtubedl_logger.info("Millis took: {}, video_url: {}".format((end_time-start_time), video_url))
    return JsonResponse({"data": config})

def get_urls_dict():
    url1 = "https://www.youtube.com/yts/jsbin/player_ias-vflIVQ4xT/en_US/base.js?disable_polymer=true"
    if not url_dict.get(url1):
        url_dict[url1] = requests.get(url1).text
        youtubedl_logger.info("Fetching JS player")

    return url_dict


#Changed files are YoutubeDL.py, youtube_dl.__init__.py
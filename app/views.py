import json
from _ast import Dict
from urlparse import urlparse

import pytz
from django.http import JsonResponse

from app.models import Video
from libs import youtube_dl
from datetime import datetime, time, timedelta
from django.shortcuts import render
import yaml

expired_hours_dict = {
    'www.youtube.com': 6,
    'youtube.com': 6
}

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


def proxy_video_config(request):
    data = json.loads(request.body)
    video_id = data.get('video_id')
    video_url = "https://www.youtube.com/watch?v={}".format(video_id)
    bypass_data = data.get('bypass_data')
    config = youtube_dl._real_main([video_url, "-F", "--no-check-certificate", "--bypass-content", json.dumps(bypass_data)])[0]
    return JsonResponse({"data": config})
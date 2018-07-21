import json
from _ast import Dict
from urllib.parse import urlparse

import pytz
from django.http import JsonResponse

from libs import youtube_dl
from datetime import datetime, time, timedelta
from django.shortcuts import render
from app.models import Video

expired_hours_dict = {
    'www.youtube.com': 6,
    'youtube.com': 6
}

# Create your views here.


def load_video_config(video_url: str) -> Video:
    video: Video = Video.objects.filter(video_url=video_url).first()
    site = urlparse(video_url).netloc
    expire_hours = expired_hours_dict[site.lower()]
    if video and video.updated_at + timedelta(hours=expire_hours) > datetime.now(pytz.UTC):
        return video
    else:
        if video:
            video.delete()
        config = youtube_dl._real_main([video_url, "-F", "--no-check-certificate"])[0]
        config = json.dumps(config)
        video: Video = Video.objects.create(video_url=video_url, video_config=config)

    return video


def video_config(request):
    data: Dict[str, str] = json.loads(request.body)
    video_url: str = data['video_url']
    video: Video = load_video_config(video_url)
    return JsonResponse({'data': json.loads(video.video_config)})


def video_format(request):
    data: Dict[str, str] = json.loads(request.body)
    video_url: str = data['video_url']
    video: Video = load_video_config(video_url)
    config: Dict[str, str] = json.loads(video.video_config)
    formats = config.get('format') or config.get('formats')
    return JsonResponse({'data': formats})

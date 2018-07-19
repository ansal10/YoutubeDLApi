import json
from _ast import Dict, Tuple

import pytz
from django.http import JsonResponse
from pip._vendor.urllib3.contrib._securetransport.bindings import Boolean

from libs import youtube_dl
from datetime import datetime, time, timedelta
from django.shortcuts import render

expired_days = 30

# Create your views here.
from app.models import Video


def load_video_config(video_url: str) -> (Boolean, Video):
    video: Video = Video.objects.filter(video_url=video_url).first()
    if video and video.updated_at + timedelta(days=expired_days) > datetime.now(pytz.UTC):
        return False, video
    else:
        config = youtube_dl._real_main([video_url, "-F", "--no-check-certificate"])[0]
        config = json.dumps(config)
        video: Video = Video.objects.create(video_url=video_url, video_config=config)
        return True, video


def video_config(request):
    data: Dict[str, str] = json.loads(request.body)
    video_url: str = data['video_url']
    (modified, video) = load_video_config(video_url)
    if modified:
        return JsonResponse({'data': json.loads(video.video_config)}, status=200)
    else:
        return JsonResponse({'data': json.loads(video.video_config)}, status=304)


def video_format(request):
    data: Dict[str, str] = json.loads(request.body)
    video_url: str = data['video_url']
    modified, video = load_video_config(video_url)
    config: Dict[str, str] = json.loads(video.video_config)
    formats = config.get('format') or config.get('formats')
    if modified:
        return JsonResponse({'data': formats})
    else:
        return JsonResponse({'data': formats}, status=304)

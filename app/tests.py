from django.test import TestCase

# Create your tests here.
from app.models import Video
from app.views import load_video_config


class TestLoadConfig(TestCase):

    def test_load_config_for_youtube(self):
        url = "https://youtube.com/watch?v=n2rr1P8rHig"
        video: Video = load_video_config(url)
        self.assertIsNotNone(video)
from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=255, db_index=True, unique=True, null=True)
    video_site = models.CharField(max_length=255, db_index=True, null=True)
    video_config = models.TextField(default='{}')
    video_url = models.CharField(max_length=1023, db_index=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


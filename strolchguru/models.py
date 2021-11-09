from django.db import models


class Clip(models.Model):
    title = models.CharField(max_length=100)
    custom_title = models.CharField(max_length=100, null=True)
    clip_id = models.IntegerField(unique=True)
    url = models.URLField()
    embed_url = models.URLField()
    slug = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    curator = models.CharField(max_length=25)
    clip_url = models.URLField()
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    is_downloaded = models.BooleanField(default=False)

from django.db import models


class Clip(models.Model):
    title = models.CharField(max_length=100)
    clip_id = models.IntegerField(unique=True)
    url = models.URLField()
    embed_url = models.URLField()
    slug = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    curator = models.CharField(max_length=25)
    clip_url = models.URLField()
    is_published = models.BooleanField(default=True)

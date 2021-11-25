from django.db import models


class Clip(models.Model):
    title = models.CharField(max_length=100)
    custom_title = models.CharField(max_length=100, null=True, blank=True)
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
    tags = models.ManyToManyField("Tag")

    @property
    def display_title(self):
        if self.custom_title:
            return self.custom_title

        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

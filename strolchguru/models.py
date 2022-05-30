from django.db import models


class Clip(models.Model):
    title = models.CharField(max_length=100)
    custom_title = models.CharField(max_length=100, null=True, blank=True)
    clip_id = models.IntegerField(unique=True)
    url = models.URLField()
    embed_url = models.URLField()
    slug = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    category = models.CharField(max_length=100, null=True)
    curator = models.CharField(max_length=25)
    clip_url = models.URLField()
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    is_downloaded = models.BooleanField(default=False)
    is_in_loop = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tag", blank=True)
    last_played = models.DateTimeField(null=True)

    @property
    def display_title(self):
        if self.custom_title:
            return self.custom_title

        return self.title

    def show(self):
        self.is_published = True
        self.save()

    def hide(self):
        self.is_in_loop = False
        self.is_published = False
        self.save()

    def add_to_loop(self):
        self.is_in_loop = True
        self.save()

    def remove_from_loop(self):
        if self.is_published:
            self.is_in_loop = False
            self.save()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

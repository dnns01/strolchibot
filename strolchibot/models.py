from django.db import models
from .managers import TwitchUserManager
from strolchibot import twitch_api
import os


class TextCommand(models.Model):
    command = models.CharField(max_length=20)
    text = models.TextField(max_length=500)
    active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.command[0] == "!":
            self.command = self.command[1:]
        super().save(force_insert, force_update, using, update_fields)


class Klassenbuch(models.Model):
    name = models.CharField(max_length=50)
    sticker = models.IntegerField(default=0)


class Timer(models.Model):
    text = models.TextField(max_length=500)
    active = models.BooleanField(default=True)


class LinkPermit(models.Model):
    nick = models.CharField(max_length=25)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nick = self.nick.lower()
        super().save(force_insert, force_update, using, update_fields)


class LinkWhitelist(models.Model):
    url = models.URLField()


class LinkBlacklist(models.Model):
    url = models.URLField()


class Config(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)


class TwitchUser(models.Model):
    objects = TwitchUserManager()

    id = models.BigIntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)

    def update_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.save()

    @property
    def is_authenticated(self):
        broadcaster_id = int(os.getenv("BROADCASTER_ID"))
        if self.id == broadcaster_id or self.admin:
            return True
        try:
            broadcaster = TwitchUser.objects.get(pk=broadcaster_id)
            return twitch_api.is_mod(self, broadcaster)
        except TwitchUser.DoesNotExist:
            return False

from django.db import models
from .managers import TwitchUserManager
from strolchibot import twitch_api
import os


class TextCommand(models.Model):
    command = models.CharField(max_length=20)
    text = models.TextField(max_length=500)
    active = models.BooleanField(default=True)


class Klassenbuch(models.Model):
    name = models.CharField(max_length=50)
    sticker = models.IntegerField(default=0)


class Timer(models.Model):
    text = models.TextField(max_length=500)
    active = models.BooleanField(default=True)


class LinkPermit(models.Model):
    nick = models.CharField(max_length=25)


class Config(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)


class TwitchUser(models.Model):
    objects = TwitchUserManager()

    id = models.BigIntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    last_login = models.DateTimeField(null=True)

    def update_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.save()

    def is_authenticated(self):
        broadcaster_id = os.getenv("BROADCASTER_ID")
        try:
            broadcaster = TwitchUser.objects.get(pk=broadcaster_id)
            return twitch_api.is_mod(self, broadcaster)
        except TwitchUser.DoesNotExist:
            return False

    def is_admin(self):
        return self.login.lower() == "strolchibot"

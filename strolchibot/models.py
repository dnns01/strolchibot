import os

from django.db import models

from strolchibot import twitch_api
from .managers import TwitchUserManager


class Command(models.Model):
    PERMISSION_CHOICES = (("EO", "Everyone"), ("SUB", "Subscriber"), ("MOD", "Moderator"))

    command = models.CharField(max_length=20)
    text = models.TextField(max_length=500)
    permissions = models.CharField(max_length=5, choices=PERMISSION_CHOICES, default="EO")
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
    link_protection_active = models.BooleanField(default=True, verbose_name="Active")
    link_protection_permit_subs = models.BooleanField(default=True, verbose_name="Permit Subs")
    streamer = models.TextField(max_length=20, null=True)


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
        return self.is_broadcaster or self.is_admin or self.is_mod

    @property
    def is_broadcaster(self):
        return self.id == int(os.getenv("BROADCASTER_ID"))

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_mod(self):
        if self.is_broadcaster:
            return True
        try:
            broadcaster = TwitchUser.objects.get(pk=int(os.getenv("BROADCASTER_ID")))
            return twitch_api.is_mod(self, broadcaster)
        except TwitchUser.DoesNotExist:
            return False


class Counter(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()


class Spotify(models.Model):
    streamer = models.TextField(max_length=50, unique=True)
    access_token = models.TextField(max_length=200)
    token_type = models.TextField(max_length=20)
    expires_in = models.IntegerField()
    refresh_token = models.TextField(max_length=200)
    scope = models.TextField(max_length=100)
    user_id = models.TextField(max_length=50)

import os

import requests
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import BaseModelForm, LinkProtectionConfigForm
from .models import Command, Klassenbuch, Timer, Config, LinkPermit, LinkWhitelist, LinkBlacklist


def home(request):
    return render(request, "home.html", {"title": "Strolchibot"})


@login_required(login_url="/login")
def commands(request):
    CommandsFormSet = modelformset_factory(Command, form=BaseModelForm, fields=("command", "text", "active"))
    if request.method == "POST":
        formset = CommandsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    forms = {
        "Basic Configuration": {
            "display": "card",
            "type": "formset",
            "name": "commands",
            "formset": CommandsFormSet(),
            "remove_url": "commands_remove",
            "activate_url": "commands_activate",
            "collapsible": True,

        },
    }

    return render(request, "form.html", {"title": "Commands", "forms": forms, "active": "commands"})


@login_required(login_url="/login")
def commands_remove(request, id):
    Command.objects.filter(pk=id).delete()

    return redirect("/commands")


@login_required(login_url="/login")
def commands_activate(request, id):
    command = Command.objects.get(pk=id)
    command.active = not command.active
    command.save()

    return redirect("/commands")


@login_required(login_url="/login")
def klassenbuch(request):
    KlassenbuchFormSet = modelformset_factory(Klassenbuch, form=BaseModelForm, fields=("name", "sticker"))
    if request.method == "POST":
        formset = KlassenbuchFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    forms = {
        "Basic Configuration": {
            "display": "card",
            "type": "formset",
            "name": "klassenbuch",
            "formset": KlassenbuchFormSet(),
            "remove_url": "klassenbuch_remove",
        },
    }

    return render(request, "form.html", {"title": "Klassenbuch", "forms": forms, "active": "klassenbuch"})


@login_required(login_url="/login")
def klassenbuch_remove(request, id):
    Klassenbuch.objects.filter(pk=id).delete()

    return redirect("/klassenbuch")


@login_required(login_url="/login")
def timers(request):
    TimerFormSet = modelformset_factory(Timer, form=BaseModelForm, fields=("text", "active"))
    if request.method == "POST":
        formset = TimerFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    forms = {
        "Basic Configuration": {
            "display": "card",
            "type": "formset",
            "name": "timers",
            "formset": TimerFormSet(),
            "remove_url": "timers_remove",
            "activate_url": "timers_activate",
        },
    }

    return render(request, "form.html", {"title": "Timers", "forms": forms, "active": "timers"})


@login_required(login_url="/login")
def timers_remove(request, id):
    Timer.objects.filter(pk=id).delete()

    return redirect("/timers")


@login_required(login_url="/login")
def timers_activate(request, id):
    timer = Timer.objects.get(pk=id)
    timer.active = not timer.active
    timer.save()

    return redirect("/timers")


@login_required(login_url="/login")
def config(request):
    if request.user.admin:
        ConfigFormSet = modelformset_factory(Config, form=BaseModelForm, fields=("key", "value"))
        if request.method == "POST":
            formset = ConfigFormSet(request.POST, request.FILES)
            if formset.is_valid():
                formset.save()

        forms = {
            "Basic Configuration": {
                "display": "card",
                "type": "formset",
                "name": "config",
                "formset": ConfigFormSet(),
                "remove_url": "config_remove", },
        }

        return render(request, "form.html", {"title": "Config", "forms": forms, "active": "config", })

    raise Http404


@login_required(login_url="/login")
def config_remove(request, id):
    if request.user.admin:
        Config.objects.filter(pk=id).delete()

        return redirect("/config")

    raise Http404


@login_required(login_url="/login")
def link_protection(request):
    LinkPermitFormSet = modelformset_factory(LinkPermit, form=BaseModelForm, fields=("nick",))
    LinkWhitelistFormSet = modelformset_factory(LinkWhitelist, form=BaseModelForm, fields=("url",))
    LinkBlacklistFormSet = modelformset_factory(LinkBlacklist, form=BaseModelForm, fields=("url",))
    active = "config"
    form = None

    if request.method == "POST":
        active = request.POST["form-active"]

        if active == "config":
            form = LinkProtectionConfigForm(request.POST)
        elif active == "permit":
            form = LinkPermitFormSet(request.POST, request.FILES)
        elif active == "whitelist":
            form = LinkWhitelistFormSet(request.POST, request.FILES)
        elif active == "blacklist":
            form = LinkBlacklistFormSet(request.POST, request.FILES)

        if form and form.is_valid():
            form.save()

    forms = {
        "Basic Configuration": {
            "display": "card",
            "type": "form",
            "name": "config",
            "form": LinkProtectionConfigForm()},
        "Permits": {
            "display": "list",
            "type": "formset",
            "name": "permit",
            "formset": LinkPermitFormSet(),
            "remove_url": "link_protection_permit_remove",
        },
        "Whitelist": {
            "display": "list",
            "type": "formset",
            "name": "whitelist",
            "formset": LinkWhitelistFormSet(),
            "remove_url": "link_protection_whitelist_remove",
        },
        "Blacklist": {
            "display": "list",
            "type": "formset",
            "name": "blacklist",
            "formset": LinkBlacklistFormSet(),
            "remove_url": "link_protection_blacklist_remove",
        },
    }

    return render(request, "form.html", {"title": "Link Protection", "forms": forms, "active": active})


@login_required(login_url="/login")
def link_protection_permit_remove(request, id):
    LinkPermit.objects.filter(pk=id).delete()

    return redirect("/link_protection")


@login_required(login_url="/login")
def link_protection_whitelist_remove(request, id):
    LinkWhitelist.objects.filter(pk=id).delete()

    return redirect("/link_protection")


@login_required(login_url="/login")
def link_protection_blacklist_remove(request, id):
    LinkBlacklist.objects.filter(pk=id).delete()

    return redirect("/link_protection")


def login(request):
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=moderation:read"
    return redirect(url)


def logout(request):
    django_logout(request)
    return redirect("/")


def login_redirect(request):
    code = request.GET.get("code")
    user = exchange_code(code)
    if user:
        twitch_user = authenticate(request, user=user)
        twitch_user = list(twitch_user).pop()
        django_login(request, twitch_user)

    return redirect("/")


def exchange_code(code):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}"
    response = requests.post(url)
    if response.status_code == 200:
        credentials = response.json()

        response = requests.get("https://api.twitch.tv/helix/users", headers={
            "Authorization": f"Bearer {credentials['access_token']}",
            "Client-Id": client_id
        })

        user = response.json()["data"][0]

        return {"id": user["id"], "login": user["login"], "access_token": credentials["access_token"],
                "refresh_token": credentials["refresh_token"]}

    return None

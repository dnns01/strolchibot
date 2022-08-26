import json
import os

import requests
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, modelform_factory
from django.http import Http404, JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BaseModelForm, LinkProtectionConfigForm, CommandForm, SpotifyForm, CounterForm
from .models import Command, Klassenbuch, Timer, Config, LinkPermit, LinkWhitelist, LinkBlacklist, Spotify, Counter


def home(request):
    return render(request, "home.html", {"title": "Strolchibot"})


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


# <editor-fold desc="Commands">
@login_required(login_url="/login")
def commands(request: HttpRequest) -> HttpResponse:
    return render(request, "commands/list.html",
                  {"title": "Commands", "commands": Command.objects.all().order_by("command"), "active": "commands"})


@login_required(login_url="/login")
def commands_new(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CommandForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/commands")

    form = CommandForm()

    return render(request, "commands/edit.html",
                  {"title": "Commands", "form": {"form": form}})


@login_required(login_url="/login")
def commands_remove(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            command = get_object_or_404(Command, pk=payload["id"])
            command.delete()
        except (json.decoder.JSONDecodeError, KeyError):
            pass

        return JsonResponse({})

    raise Http404


@login_required(login_url="/login")
def commands_edit(request: HttpRequest, command_id: int) -> HttpResponse:
    command = get_object_or_404(Command, pk=command_id)

    if request.method == "POST":
        form = CommandForm(request.POST, instance=command)

        if form.is_valid():
            form.save()
            return redirect("/commands")

    form = CommandForm(instance=command)

    return render(request, "commands/edit.html",
                  {"title": "Commands", "form": {"form": form}})


@login_required(login_url="/login")
def commands_set_active(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            command = get_object_or_404(Command, command=payload["command"])
            command.active = payload["active"]
            command.save()

            return JsonResponse({"active": command.active})
        except (json.decoder.JSONDecodeError, KeyError):
            pass

    raise Http404


# </editor-fold>


# <editor-fold desc="Spotify">
@login_required(login_url="/login")
def spotify(request: HttpRequest) -> HttpResponse:
    spotify_logins = Spotify.objects.all()

    return render(request, "spotify/list.html",
                  {"title": "Spotify", "spotify_logins": spotify_logins})


def spotify_edit(request: HttpRequest, streamer: str) -> HttpResponse:
    user = get_object_or_404(Spotify, streamer=streamer)

    if request.method == "POST":
        form = SpotifyForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("/spotify")

    form = SpotifyForm(instance=user)

    return render(request, "spotify/edit.html",
                  {"title": "Spotify", "form": {"form": form}})


@login_required(login_url="/login")
def spotify_login(request: HttpRequest) -> HttpResponse:
    url = os.getenv("SPOTIFY_AUTH_URL")
    return redirect(url)


@login_required(login_url="/login")
def spotify_login_redirect(request: HttpRequest) -> JsonResponse:
    code = request.GET.get('code')
    data = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    token_type = credentials['token_type']
    expires_in = credentials['expires_in']
    refresh_token = credentials['refresh_token']
    scope = credentials['scope']

    response = requests.get("https://api.spotify.com/v1/me", headers={
        'Authorization': f'Bearer {access_token}'
    })

    user_id = response.json()['id']
    streamer = response.json()['display_name'].replace(' ', '').lower()
    users = Spotify.objects.filter(user_id=user_id)

    if len(list(users)) == 1:
        for user in users:
            user.access_token = access_token
            user.token_type = token_type
            user.expires_in = expires_in
            user.refresh_token = refresh_token
            user.scope = scope
            user.save()
            return redirect(f"/spotify")
    else:
        user = Spotify(streamer=streamer, access_token=access_token, token_type=token_type,
                       expires_in=expires_in, refresh_token=refresh_token, scope=scope, user_id=user_id)
        user.save()
        return redirect(f"/spotify/edit/{user_id}")


# </editor-fold>


# <editor-fold desc="Counter">
@login_required(login_url="/login")
def counters(request: HttpRequest) -> HttpResponse:
    return render(request, "counters/list.html",
                  {"title": "Counter", "counters": Counter.objects.all(), "active": "counters"})


@login_required(login_url="/login")
def counters_new(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CounterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/counters")

    form = CounterForm()

    return render(request, "counters/edit.html",
                  {"title": "Counters", "form": {"form": form}})


@login_required(login_url="/login")
def counters_remove(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            counter = get_object_or_404(Counter, pk=payload["id"])
            counter.delete()
        except (json.decoder.JSONDecodeError, KeyError):
            pass

        return JsonResponse({})

    raise Http404


@login_required(login_url="/login")
def counters_edit(request: HttpRequest, counter_id: int) -> HttpResponse:
    counter = get_object_or_404(Counter, pk=counter_id)

    if request.method == "POST":
        form = CounterForm(request.POST, instance=counter)

        if form.is_valid():
            form.save()
            return redirect("/counters")

    form = CounterForm(instance=counter)

    return render(request, "counters/edit.html",
                  {"title": "Counters", "form": {"form": form}})
# </editor-fold>

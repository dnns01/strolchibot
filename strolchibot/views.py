from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from .models import TextCommand, Klassenbuch, Timer
import os
import requests


def home(request):
    return render(request, "home.html", {'title': 'Strolchibot'})


@login_required(login_url="/login")
def text_commands(request):
    TextCommandsFormSet = modelformset_factory(TextCommand, fields=('command', 'text'))
    if request.method == "POST":
        formset = TextCommandsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    formset = TextCommandsFormSet()

    return render(request, "form.html", {'title': 'Text Commands', 'formset': formset})


@login_required(login_url="/login")
def klassenbuch(request):
    KlassenbuchFormSet = modelformset_factory(Klassenbuch, fields=('name', 'sticker'))
    if request.method == "POST":
        formset = KlassenbuchFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    formset = KlassenbuchFormSet()

    return render(request, "form.html", {'title': 'Klassenbuch', 'formset': formset})


@login_required(login_url="/login")
def timers(request):
    TimerFormSet = modelformset_factory(Timer, fields=('text',))
    if request.method == "POST":
        formset = TimerFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

    formset = TimerFormSet()

    return render(request, "form.html", {'title': 'Timers', 'formset': formset})


def login(request):
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=moderation:read"
    return redirect(url)


def logout(request):
    django_logout(request)
    return redirect("/")


def login_redirect(request):
    code = request.GET.get('code')
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
            'Authorization': f'Bearer {credentials["access_token"]}',
            'Client-Id': client_id
        })

        user = response.json()["data"][0]

        return {'id': user['id'], 'login': user['login'], 'access_token': credentials['access_token'],
                'refresh_token': credentials['refresh_token']}

    return None

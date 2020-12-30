from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from strolchibot import twitch_api
import os


def home(request) -> HttpResponse:
    clips = twitch_api.get_clips()
    return render(request, 'strolchguru_home.html', context={'clips': clips, 'url_name': "clips"})


def clips_all(request) -> JsonResponse:
    clips = twitch_api.get_clips(all_clips=True)
    return JsonResponse(clips, safe=False)


def clips_today(request) -> HttpResponse:
    clips = twitch_api.get_clips(today=True)
    return render(request, 'strolchguru_home.html', context={'clips': clips, 'url_name': "clips_today"})


def clips_all_today(request) -> JsonResponse:
    clips = twitch_api.get_clips(all_clips=True, today=True)
    return JsonResponse(clips, safe=False)

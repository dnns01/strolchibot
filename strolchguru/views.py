import random

from django.http import HttpResponse
from django.shortcuts import render

from .models import Clip


def home(request) -> HttpResponse:
    clips = list(Clip.objects.all())
    clip = random.choice(clips)
    return render(request, 'strolchguru_home.html', context={'clip': clip, 'mode': "random_clips"})


def clip(request, id) -> HttpResponse:
    clip = Clip.objects.get(pk=id)
    return render(request, 'strolchguru_home.html', context={'clip': clip, 'mode': "loop"})

# def clips_today(request) -> HttpResponse:
#     clips = twitch_api.get_clips(today=True)
#     return render(request, 'strolchguru_home.html', context={'clip': clip, 'url_name': "clips_today"})

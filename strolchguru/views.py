import random

from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Clip


def home(request) -> HttpResponse:
    clips = list(Clip.objects.filter(is_published=True, is_downloaded=True))
    clip = random.choice(clips)
    return render(request, 'strolchguru_home.html', context={'clip': clip, 'mode': "random_clips"})


def clip(request, id) -> HttpResponse:
    clip = get_object_or_404(Clip, pk=id)
    return render(request, 'strolchguru_home.html', context={'clip': clip, 'mode': "loop"})


def clip_json(request, id) -> JsonResponse:
    try:
        clip = Clip.objects.get(pk=id)
        json = model_to_dict(clip)
        return JsonResponse(json)
    except Clip.DoesNotExist:
        return JsonResponse({"error": "Clip with this id does not exist"})

# def clips_today(request) -> HttpResponse:
#     clips = twitch_api.get_clips(today=True)
#     return render(request, 'strolchguru_home.html', context={'clip': clip, 'url_name': "clips_today"})

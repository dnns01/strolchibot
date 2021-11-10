import random

from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Clip


def home(request) -> HttpResponse:
    controls = True if request.GET.get("controls") == "1" else False
    clips = list(Clip.objects.filter(is_published=True, is_downloaded=True))
    clip = random.choice(clips)
    return render(request, 'strolchguru_home.html',
                  context={'clip': clip, 'mode': "random_clips", 'controls': controls})


def clip(request, id) -> HttpResponse:
    controls = True if request.GET.get("controls") == "1" else False
    clip = get_object_or_404(Clip, pk=id)

    if not clip.is_published:
        raise Http404()

    return render(request, 'strolchguru_home.html', context={'clip': clip, 'mode': "loop", 'controls': controls})


def clip_json(request, id) -> JsonResponse:
    try:
        clip = Clip.objects.get(pk=id)
        json = model_to_dict(clip)
        return JsonResponse(json)
    except Clip.DoesNotExist:
        return JsonResponse({"error": "Clip with this id does not exist"})

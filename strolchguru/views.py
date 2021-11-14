import random

from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from strolchibot.models import TwitchUser
from .forms import ClipSearchForm
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


def clips(request) -> HttpResponse:
    clips = Clip.objects.filter(is_downloaded=True).order_by("-created_at")
    if not (isinstance(request.user, TwitchUser) and request.user.is_mod and request.user.is_admin):
        clips = clips.filter(is_published=True)

    form = ClipSearchForm(request.GET)
    # check whether it's valid:
    if form.is_valid():
        search = form.cleaned_data["search"]
        clips = clips.filter(
            Q(title__icontains=search) | Q(curator__icontains=search) | Q(tags__name__icontains=search))

    else:
        clips = None

    paginator = Paginator(clips, 50)
    page_obj = paginator.get_page(1)

    return render(request, "clips.html", context={"title": "Clips", "clips": page_obj, "search_form": form})

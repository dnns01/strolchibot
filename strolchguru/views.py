import random
import re

from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from strolchibot.models import TwitchUser
from .forms import ClipSearchForm
from .models import Clip


def get_pages(page, num_pages):
    if page > num_pages:
        raise Http404

    if num_pages <= 5:
        return range(1, num_pages + 1)
    else:
        start_page = page - 2 if page >= 3 else 1
        end_page = page + 2 if page <= num_pages - 2 else num_pages

        if end_page - start_page < 4:
            if start_page < 3:
                end_page = start_page + 4
            elif end_page > num_pages - 2:
                start_page = end_page - 4
        return range(start_page, end_page + 1)


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
    page = request.GET.get("page", "1")
    clips = Clip.objects.filter(is_downloaded=True).order_by("-created_at")
    if not (isinstance(request.user, TwitchUser) and request.user.is_mod and request.user.is_admin):
        clips = clips.filter(is_published=True)

    form = ClipSearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data["search"]
        clips = clips.filter(
            Q(title__icontains=search) | Q(curator__icontains=search) | Q(tags__name__icontains=search)).distinct()

    else:
        clips = None

    if re.match("^[0-9]+$", page):
        page = int(page)
    else:
        raise Http404

    paginator = Paginator(clips, 50)
    pages = get_pages(page, paginator.num_pages)
    page_obj = paginator.get_page(page)

    return render(request, "clips.html",
                  context={"title": "Clips", "clips": page_obj, "search_form": form, "page": page, "pages": pages})

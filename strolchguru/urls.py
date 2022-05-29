"""strolchibot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from strolchguru import views

urlpatterns = [
    path('', views.home, name="strolchguru"),
    path('tag/<str:tag>', views.home_tag, name="home_tag"),
    path('<int:id>', views.clip, name="clip"),
    path('<int:id>/json', views.clip_json, name="clip_json"),
    path('clips', views.clips, name="clips"),
    path('clips/edit/<int:clip_id>', views.clip_edit, name="clip_edit"),
    path('clips/visible', views.clip_set_visible, name="clip_set_visible"),
    path('clips/in_loop', views.clip_set_in_loop, name="clip_set_in_loop"),
    path('tags', views.tags, name="tags"),
    path('tags/remove/<int:id>', views.tags_remove, name="tags_remove"),
]

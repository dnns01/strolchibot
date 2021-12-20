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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('login/redirect/', views.login_redirect, name="login_redirect"),
    path('commands/', views.commands, name="commands"),
    path('commands/new', views.commands_new, name="commands_new"),
    path('commands/remove', views.commands_remove, name="commands_remove"),
    path('commands/edit/<int:command_id>', views.commands_edit, name="commands_edit"),
    path('commands/active', views.commands_set_active, name="commands_set_activate"),
    path('counters', views.counters, name="counters"),
    path('counters/new', views.counters_new, name="counters_new"),
    path('counters/remove', views.counters_remove, name="counters_remove"),
    path('counters/edit/<int:counter_id>', views.counters_edit, name="counters_edit"),
    path('klassenbuch/', views.klassenbuch, name="klassenbuch"),
    path('klassenbuch/remove/<int:id>', views.klassenbuch_remove, name="klassenbuch_remove"),
    path('timers/', views.timers, name="timers"),
    path('timers/remove/<int:id>', views.timers_remove, name="timers_remove"),
    path('timers/activate/<int:id>', views.timers_activate, name="timers_activate"),
    path('link_protection/', views.link_protection, name="link_protection"),
    path('link_protection/permit/remove/<int:id>', views.link_protection_permit_remove,
         name="link_protection_permit_remove"),
    path('link_protection/whitelist/remove/<int:id>', views.link_protection_whitelist_remove,
         name="link_protection_whitelist_remove"),
    path('link_protection/blacklist/remove/<int:id>', views.link_protection_blacklist_remove,
         name="link_protection_blacklist_remove"),
    path('strolchguru/', include('strolchguru.urls')),
    path('twitter/', include('twitter.urls')),
    path('spotify', views.spotify, name="spotify"),
    path('spotify/edit/<str:streamer>', views.spotify_edit, name="spotify_edit"),
    path('spotify/login', views.spotify_login, name="spotify_login"),
    path('spotify/login/redirect', views.spotify_login_redirect, name="spotify_login_redirect"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

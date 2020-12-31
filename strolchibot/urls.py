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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('login/redirect/', views.login_redirect, name="login_redirect"),
    path('text_commands/', views.text_commands, name="text_commands"),
    path('text_commands/remove/<int:id>', views.text_commands_remove, name="text_commands_remove"),
    path('klassenbuch/', views.klassenbuch, name="klassenbuch"),
    path('klassenbuch/remove/<int:id>', views.klassenbuch_remove, name="klassenbuch_remove"),
    path('timers/', views.timers, name="timers"),
    path('timers/remove/<int:id>', views.timers_remove, name="timers_remove"),
    path('strolchguru/', include('strolchguru.urls')),
]

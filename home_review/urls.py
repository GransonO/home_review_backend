"""home_review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .apps.authentication import urls as auth_urls
from .apps.text_process import urls as process_urls
from .apps.support import urls as support_urls
from .apps.reviews import urls as reviews_urls
from .apps.homes import urls as homes_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'auth/',
        include(auth_urls),
        name="authUrls"),

    path(
        'text_process/',
        include(process_urls),
        name='process'),

    path(
        'support/',
        include(support_urls),
        name='support'),

    path(
        'reviews/',
        include(reviews_urls),
        name='reviews'),

    path(
        'homes/',
        include(homes_urls),
        name='homes'),

]

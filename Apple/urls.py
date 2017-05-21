"""Apple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.views import login
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from mainsite.views import set_language

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^lan/(?P<language>en|jp|zh-hant)$', set_language),
    url(r'^invoice/', include('invoice.urls')),
    url(r'^accounts/login/$', login)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mainsite.urls')),
)

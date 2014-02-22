from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# define a catch all
def index(request):
    return render_to_response('index.html')

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^.*/$', index),
)

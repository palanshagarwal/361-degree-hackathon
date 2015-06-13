from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bot.views.home', name='home'),
    # url(r'^ping/', include('blog.urls')),
    url(r'^ping', views.ping, name='ping'),
    url(r'^start', views.start, name='start'),
    url(r'^play', views.play, name='play'),
    # url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url

from iseteam.buddies.views import post

urlpatterns = patterns('iseteam.buddies.views',

        url(r'^request/$','post', name ="request buddy"),
) 
from django.conf.urls import patterns, include, url

from iseteam.parties.views import post, view

urlpatterns = patterns('iseteam.pictures.views',

	url(r'^upload/$','upload', name ="upload"),

) 
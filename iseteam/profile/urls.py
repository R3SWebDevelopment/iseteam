from django.conf.urls import patterns, include, url

from iseteam.profile.views import post, view

urlpatterns = patterns('iseteam.profile.views',

	url(r'^post/$','post', name ="upload profile by user"),
	url(r'^(?P<username>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'view profile'),

) 
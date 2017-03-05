from django.conf.urls import patterns, include, url

from iseteam.local.views import post, view

urlpatterns = patterns('iseteam.local.views',

	url(r'^$', 'local' , name = 'local list'),
	url(r'^post/$','post', name ="post local by staff"),
	url(r'^(?P<localID>\d+)/(?P<name_url>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'view local'),

) 

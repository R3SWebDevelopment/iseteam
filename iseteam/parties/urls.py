from django.conf.urls import patterns, include, url

from iseteam.parties.views import post, view

urlpatterns = patterns('iseteam.parties.views',

	url(r'^$', 'parties' , name = 'parties list'),
	url(r'^post/$','post', name ="post party by staff"),
	url(r'^(?P<partyID>\d+)/(?P<name_url>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'view party'),

) 
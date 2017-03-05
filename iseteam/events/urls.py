from django.conf.urls import patterns, include, url

from iseteam.events.views import view

urlpatterns = patterns('iseteam.events.views', 

		url(r'^$', 'events' , name = 'events_list'),
        url(r'^(?P<slug>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'view_event'),

) 
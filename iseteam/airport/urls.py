from django.conf.urls import patterns, include, url

urlpatterns = patterns('iseteam.airport.views',

        url(r'^$','pickup', name ="pickup"),
        url(r'^attendant/(?P<airportID>\d+)/$', 'set_attendant', name='set_attendant'),


) 
from django.conf.urls import patterns, include, url

from iseteam.contact.views import post

urlpatterns = patterns('iseteam.contact.views', 

		url(r'^$', 'post' , name = 'contact'),

) 
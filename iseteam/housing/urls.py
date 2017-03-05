from django.conf.urls import patterns, include, url


urlpatterns = patterns('iseteam.housing.views', 

		url(r'^$', 'request' , name = 'request_housing'),

) 
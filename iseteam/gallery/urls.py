from django.conf.urls import patterns, include, url

urlpatterns = patterns('iseteam.gallery.views', 

	url(r'^$', 'galleries' , name = 'galleries_list'),
    url(r'^(?P<slug>[a-zA-Z0-9_+-]+)/$', 'view_album' , name = 'view_album'),

) 
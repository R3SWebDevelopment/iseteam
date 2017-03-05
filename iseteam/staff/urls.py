from django.conf.urls import patterns, include, url

from iseteam.staff.views import *

urlpatterns = patterns('iseteam.staff.views',

	url(r'^$', 'staff' , name = 'staff list'),
	url(r'^post/$','post', name ="post_staff"),
	url(r'^records/$','joinus3_records', name ="join3"),
	url(r'^records2/$','joinus2_records', name ="join2"),
	url(r'^records1/$','joinus_records', name ="jpin"),


) 
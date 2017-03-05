from django.conf.urls import patterns, include, url

from iseteam.trips.views import (
        PictureDeleteView,PictureListView
       )

urlpatterns = patterns('iseteam.trips.views', 

	   url(r'^$', 'trips' , name = 'trips_list'),

        url(r'^qro/$', 'trips_queretaro' , name = 'trips_list_queretaro'),
        url(r'^toluca/$', 'trips_toluca' , name = 'trips_list_toluca'),


        url(r'^login/(?P<tripID>\d+)/$', 'login_trip', name='login_trip'),

        url(r'^pay/(?P<trip>[a-zA-Z0-9_+-]+)/$','pay', name ="pay_trip"),
        url(r'^cardpayment/(?P<paytripID>\d+)/$','card_payment', name ="card_payment"),

        url(r'^html/$','trips_html', name ="trips_html"),

        url(r'^(?P<tripID>\d+)/uploadgallery/$', 'upload_gallery', name='upload-gallery'),


        #url(r'^new/$', 'picture_create', name='upload-new'),
        #url(r'^new2/$', 'picture_create2', name='upload-basic-plus'),

        url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
        
        url(r'^view/$', PictureListView.as_view(), name='upload-view'),

        url(r'^buses/(?P<tripID>[a-zA-Z0-9_+-]+)/$','buses_html', name ="buses_html"),
        url(r'^rooms/(?P<tripID>[a-zA-Z0-9_+-]+)/$','rooms_html', name ="rooms_html"),
        url(r'^staffhistory/(?P<paytripID>\d+)/$','see_history', name ="see_history_staff"),


        url(r'^hotel/(?P<tripID>\d+)/(?P<confirmation>[a-zA-Z0-9]+)/(?P<roomID>\d+)/$','hotel', name ="hotel"),

        url(r'^bus/$','bus', name ="bus"),

        url(r'^(?P<tripID>\d+)/buses/$','bus_records', name ="bus_records"),

        url(r'^buses/$','bus_records2', name ="bus_records2"),

        url(r'^(?P<tripID>\d+)/hotel/$','hotel_records', name ="bus_records"),
        url(r'^(?P<tripID>\d+)/payments/$','payment_records', name ="payment_records"),
        url(r'^assignstaff/(?P<paymentID>\d+)/(?P<staffID>\d+)/$','assign_staff', name ="assign_staff"),
        url(r'^paytrip/(?P<paymentID>\d+)/$','pay_trip', name ="mark as paid"),
        url(r'^delivered/(?P<paymentID>\d+)/$','delivered_trip', name ="delivered_trip_confirmation"),

        url(r'^deletepayment/(?P<paymentID>\d+)','delete_payment', name ="delete_payment"),
        url(r'^edit/(?P<paymentID>\d+)','edit_payment', name ="edit_payment"),
        url(r'^markasunpaid/(?P<paymentID>\d+)','mark_as_unpaid', name ="mark_as_unpaid"),
        url(r'^markasundelivered/(?P<paymentID>\d+)','mark_as_undelivered', name ="mark_as_delivered"),


        url(r'^sendfirstmail/(?P<paymentID>\d+)','send_first_mail', name ="send_first_mail"),
        url(r'^sendconfirmationmail/(?P<paymentID>\d+)','send_confirmation_mail', name ="send_confirmation_mail"),

        url(r'^(?P<tripID>\d+)/paymentsexcel/$','payment_records_excel', name ="payments_records_excel"),
        url(r'^(?P<tripID>\d+)/busesexcel/$','buses_records_excel', name ="buses_records_excel"),
        url(r'^(?P<tripID>\d+)/hotelexcel/$','hotel_records_excel', name ="hotel_records_excel"),

        url(r'^(?P<slug>[a-zA-Z0-9_+-]+)/$', 'view' , name = 'view_trip'),

        url(r'^qro/(?P<slug>[a-zA-Z0-9_+-]+)/$', 'view_queretaro' , name = 'view_trip_queretaro'),
        url(r'^toluca/(?P<slug>[a-zA-Z0-9_+-]+)/$', 'view_toluca' , name = 'view_trip_toluca'),



) 
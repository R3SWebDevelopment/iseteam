from django.conf.urls import patterns, include, url

from iseteam.trips.views import (
        PictureDeleteView,PictureListView
       )

from iseteam.trips.views import post as new_trip, admin_all_trips, payment_records, hotel_records
from iseteam.trips.views import bus_records, edit_trip, delete_trip
from iseteam.events.views import admin_all_events, new_event, edit_event, delete_event
from iseteam.housing.views import housing_records
from iseteam.airport.views import pickup_records, pickup_records_mty, pickup_records_qro
from iseteam.admin.views import admin_all_staff
from iseteam.staff.views import new_member, edit_member, delete_member

urlpatterns = patterns('', 

        url(r'^trips/new-trip/$', new_trip , name ="admin_new_trip"),
        url(r'^events/new-event/$', new_event , name ="admin_new_event"),
        url(r'^staff/new-staff/$', new_member , name ="admin_new_member"),


        url(r'^trips/all-trips/$', admin_all_trips , name ="admin_all_trips"),
        url(r'^events/all-events/$', admin_all_events , name ="admin_all_events"),
        url(r'^staff/all-staff/$', admin_all_staff , name ="admin_all_staff"),


        url(r'^trips/payments/(?P<tripID>\d+)/$', payment_records, name ="admin_payment_records"),
        url(r'^trips/rooms/(?P<tripID>\d+)/$', hotel_records, name ="admin_hotel_records"),
        url(r'^trips/buses/(?P<tripID>\d+)/$', bus_records, name ="admin_bus_records"),

        url(r'^trips/edit-trip/(?P<tripID>\d+)/$', edit_trip, name ="admin_edit_trip"),
        url(r'^events/edit-event/(?P<eventID>\d+)/$', edit_event, name ="admin_edit_event"),
        url(r'^staff/edit-member/(?P<memberID>\d+)/$', edit_member, name ="admin_edit_member"),

        url(r'^staff/delete-member/(?P<memberID>\d+)/$', delete_member, name ="admin_delete_member"),
        url(r'^trips/delete-trip/(?P<tripID>\d+)/$', delete_trip, name ="admin_delete_trip"),
        url(r'^events/delete-event/(?P<eventID>\d+)/$', delete_event, name ="admin_delete_event"),


        url(r'^housing/records/$', housing_records , name ="admin_housing_records"),
        url(r'^pickup/records/$', pickup_records , name ="admin_pickup_records"),

        url(r'^pickup/mtyrecords/$', pickup_records_mty , name ="admin_pickup_records_mty"),
        url(r'^pickup/qrorecords/$', pickup_records_qro , name ="admin_pickup_records_qro"),










) 
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout


from iseteam.trips.views import bus_records2, signup
from iseteam.staff.views import joinus, joinus2
from iseteam.airport.views import pickup

from django.views.generic import TemplateView


urlpatterns = patterns('django.views.generic.simple',
    #Homepage
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^qro/$', TemplateView.as_view(template_name="index_queretaro.html")),
    url(r'^toluca/$', TemplateView.as_view(template_name="index_toluca.html")),



    url(r'^terms/$', TemplateView.as_view(template_name="terms.html")),

    #Login and Logout
    url(r'^login/$',  login ),
    url(r'^logout/$', logout, {'next_page' : '/'}),

    url(r'^signup/(?P<tripID>\d+)/$',signup, name ="signup"),

    #Admin
    url(r'^admin/', include('iseteam.admin.urls')),


    #Facebook 
    url(r'^facebook/', include('django_facebook.urls')),

    #JoinUs
    url(r'^joinus/$',  joinus2),

    #Apps
    url(r'^airport/', include('iseteam.airport.urls')),
    url(r'^contact/', include('iseteam.contact.urls')),
    url(r'^events/', include('iseteam.events.urls')),
    url(r'^gallery/', include('iseteam.gallery.urls')),
    url(r'^pictures/', include('iseteam.pictures.urls')),
    url(r'^profile/', include('iseteam.profile.urls')),
    url(r'^housing/', include('iseteam.housing.urls')),
    url(r'^staff/', include('iseteam.staff.urls')),
    url(r'^trips/', include('iseteam.trips.urls')),



    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

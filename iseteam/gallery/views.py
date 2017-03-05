from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from iseteam.trips.decorators import login_required_staff
from iseteam.trips.models import GalleryTrip

def galleries(request):
	"""
	Return all galeries 
	"""
	galleries = GalleryTrip.objects.all().order_by('-year')
	return render_to_response('gallery/galleries.html', 
		{'galleries':galleries}, context_instance=RequestContext(request))


def view_album(request, slug):
	"""
	Return list of images by specific slug
	"""
	gallery = GalleryTrip.objects.get(trip__slug=slug)
	return render_to_response('gallery/view.html',{'gallery':gallery}, 
		context_instance=RequestContext(request))





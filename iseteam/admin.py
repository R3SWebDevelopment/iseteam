from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import json
from django.db.models import Count
from django.contrib.auth.models import User
from django.conf import settings

from iseteam.trips.models import Trip

@login_required(login_url='/login/')
def admin(request):
	trips = Trip.objects.all().order_by('date')
	return render_to_response('admin/index.html', 
		{'trips':trips}, 
		context_instance=RequestContext(request))


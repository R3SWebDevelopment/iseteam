from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from iseteam.pictures.forms import PictureForm
from iseteam.pictures.models import Picture

def upload(request):
	if request.method == 'POST':
		form = PictureForm(request.POST, request.FILES)
		if form.is_valid():
			picture = form.save()
			return HttpResponseRedirect('/pickup/done/')
	else:
		form = PictureForm()
	return render_to_response('pictures/picture.html', 
		{'form':form,'pictures':Picture.objects.all()}, context_instance=RequestContext(request))

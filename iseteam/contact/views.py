from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import json

from iseteam.contact.forms import ContactForm
from iseteam.contact.models import Contact

#staff permissions
#@login_required(login_url='/login/')
def post(request):
	if request.method == 'POST':
		form = ContactForm(request.POST, request.FILES)
		if form.is_valid():
			contact = form.save(commit=False)
			#other options before save
			contact.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponse(json.dumps({'done':'yes'}), mimetype='application/json')
	else:
		form = ContactForm()
	return render_to_response('contact/post.html', 
		{'form':form}, context_instance=RequestContext(request))



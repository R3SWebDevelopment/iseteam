from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from iseteam.local.forms import LocalForm
from iseteam.local.models import Local

#staff permissions
@login_required(login_url='/login/')
def post(request):
	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			local = form.save(commit=False)
			#other options before save
			local.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('/local/done/')
	else:
		form = LocalForm()
	return render_to_response('local/post.html', 
		{'form':form}, context_instance=RequestContext(request))


#View template local	
def view(request,localID):
	local = get_object_or_404(Local, pk=localID)
	return render_to_response('local/view.html', 
		{'local':local}, context_instance=RequestContext(request))


#View all local events
def local(request):
	local = Local.objects.all()
	return render_to_response('local/local.html',
		{'local':local}, context_instance=RequestContext(request))


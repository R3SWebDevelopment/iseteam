from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from iseteam.buddies.forms import BuddyForm

@login_required(login_url='/login/')
def post(request):
	if request.method == 'POST':
		form = BuddyForm(request.POST)
		if form.is_valid():
			buddy = form.save(commit=False)
			buddy.owner = request.user
			buddy.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('/buddies/done/')
	else:
		form = BuddyForm()
	return render_to_response('buddies/post.html', 
		{'form':form}, context_instance=RequestContext(request))


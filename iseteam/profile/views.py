from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from iseteam.profile.forms import ProfileForm
from iseteam.profile.models import Profile

#staff permissions
@login_required(login_url='/login/')
def post(request):
	current = get_object_or_404(Profile, user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=current)
		if form.is_valid():
			profile = form.save(commit=False)
			#other options before save
			profile.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('/profile/done/')
	else:
		form = ProfileForm(instance=current)
	return render_to_response('profile/post.html', 
		{'form':form}, context_instance=RequestContext(request))


def view(request, username):
	profile = get_object_or_404(User, username=username)
	return render_to_response('profile/view.html', 
		{'profile':profile}, context_instance=RequestContext(request))



from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from iseteam.parties.forms import PartyForm
from iseteam.parties.models import Party

#staff permissions
@login_required(login_url='/login/')
def post(request):
	if request.method == 'POST':
		form = PartyForm(request.POST, request.FILES)
		if form.is_valid():
			party = form.save(commit=False)
			#other options before save
			party.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('/parties/done/')
	else:
		form = PartyForm()
	return render_to_response('parties/post.html', 
		{'form':form}, context_instance=RequestContext(request))


#view template party 
def view(request,partyID,name_url):
	party = get_object_or_404(Party, pk=partyID)
	return render_to_response('parties/view.html', 
		{'party':party}, context_instance=RequestContext(request))


#View all parties
def parties(request):
	parties = Party.objects.all()
	return render_to_response('parties/parties.html',
		{'parties':parties}, context_instance=RequestContext(request))





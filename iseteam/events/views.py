from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from iseteam.events.forms import EventForm
from iseteam.events.models import Event
from iseteam.trips.decorators import login_required_staff


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def new_event(request):
	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			event = form.save(commit=False)
			#other options before save
			event.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('%s' % event.get_absolute_url())
	else:
		form = EventForm()
	return render_to_response('admin/events/new_event.html', 
		{'form':form}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def edit_event(request, eventID):
	event = get_object_or_404(Event, pk=eventID)
	if request.method == 'POST':
		form = EventForm(request.POST, request.FILES, instance=event)
		if form.is_valid():
			event = form.save(commit=False)
			#other options before save
			event.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('%s' % event.get_absolute_url())
	else:
		form = EventForm(instance=event)
	return render_to_response('admin/events/edit_event.html', 
		{'form':form, 'event':event}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def delete_event(request,eventID):
	event = get_object_or_404(Event, pk=eventID)
	event.delete()
	return HttpResponseRedirect('/admin/events/all-events/')


#view template event
def view(request,slug):
	event = get_object_or_404(Event, slug=slug)
	return render_to_response('events/view.html', 
		{'event':event}, context_instance=RequestContext(request))


#View all events
def events(request):
	events = Event.objects.all().order_by('-date')
	return render_to_response('events/events.html',
		{'events':events}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def admin_all_events(request):
	events = Event.objects.all().order_by('-date')
	return render_to_response('admin/events/all_events.html',
		{'events':events}, context_instance=RequestContext(request))



from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from iseteam.airport.forms import PickUpForm
from iseteam.airport.models import PickUp
from iseteam.email import Email


def pickup(request):
	done = False
	if request.method == 'POST':
		form = PickUpForm(request.POST)
		if form.is_valid():
			pickup = form.save()
			#Send Mail to airport user
			to=pickup.email
			subject='ISE | We have received your request to airport pickup.'
			context_render = {'pickup':pickup}
			template = 'emails/pickup.html'
			Email([to],subject,context_render,template).send()
			#Send Mail to staff
			to1 = settings.STAFF_EMAIL
			subject1 ='ISE | New request to airport pickup.'
			template1 = 'emails/pickup_staff.html'
			Email(to1,subject1,context_render,template1).send()
			return HttpResponseRedirect('/airport/?done=yes')
	else:
		if request.GET.__contains__('done'):
			if request.GET['done'] == 'yes':
				done = True
		form = PickUpForm()
	return render_to_response('airport/pickup.html', 
			{'form':form, 'done':done}, context_instance=RequestContext(request))

#staff permissions
@login_required(login_url='/login/')
def pickup_records(request):
	records = PickUp.objects.all().order_by('-timestamp')
	return render_to_response('admin/pickup/records.html', 
		{'records':records}, context_instance=RequestContext(request))



#staff permissions
@login_required(login_url='/login/')
def pickup_records_mty(request):
	records = PickUp.objects.exclude(city='Qro').order_by('-timestamp')
	return render_to_response('admin/pickup/records.html', 
		{'records':records}, context_instance=RequestContext(request))



#staff permissions
@login_required(login_url='/login/')
def pickup_records_qro(request):
	records = PickUp.objects.filter(city='Qro').order_by('-timestamp')
	return render_to_response('admin/pickup/records.html', 
		{'records':records}, context_instance=RequestContext(request))


#staff permissions
@login_required(login_url='/login/')
def set_attendant(request,airportID):
	airport = get_object_or_404(PickUp, pk=airportID)
	airport.attendant = request.user
	airport.save()
	#Send Mail to airport user
	to=airport.email
	subject='ISE | Confirmation Airport Pickup.'
	context_render = {'airport':airport}
	template = 'emails/confirm_pickup.html'
	Email([to],subject,context_render,template).send()
	return HttpResponseRedirect('/admin/pickup/records/')




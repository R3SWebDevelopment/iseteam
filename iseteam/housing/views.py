from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required


from iseteam.housing.forms import HousingForm
from iseteam.housing.models import Housing

from iseteam.email import Email

def request(request):
	done = False
	if request.method == 'POST':
		form = HousingForm(request.POST)
		if form.is_valid():
			housing = form.save()
			#Send Mail to housing user
			to=housing.email
			subject='ISE | We have received your request.'
			context_render = {'housing':housing}
			template = 'emails/housing.html'
			Email([to],subject,context_render,template).send()
			#Send Mail to staff
			to1 = settings.STAFF_EMAIL
			subject1 ='ISE | New request to housing.'
			template1 = 'emails/housing_staff.html'
			Email(to1,subject1,context_render,template1).send()

			return HttpResponseRedirect('/housing/?done=yes')
	else:
		if request.GET.__contains__('done'):
			if request.GET['done'] == 'yes':
				done = True
		form = HousingForm()
	return render_to_response('housing/request.html',
		{'form':form, 'done':done}, context_instance=RequestContext(request))


#staff permissions
@login_required(login_url='/login/')
def housing_records(request):
	records = Housing.objects.all().order_by('-timestamp')
	return render_to_response('admin/housing/records.html', 
		{'records':records}, context_instance=RequestContext(request))

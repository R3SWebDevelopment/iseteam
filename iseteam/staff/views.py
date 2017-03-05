from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User

from iseteam.staff.models import Staff, JoinUs, JoinUs2
from iseteam.staff.forms import StaffForm, JoinUsForm, JoinUs2Form, NewMemberForm
from iseteam.trips.decorators import login_required_staff

import datetime
import json

#staff permissions
@login_required(login_url='/login/')
def post(request):
	if request.method == 'POST':
		form = StaffForm(request.POST, request.FILES)
		if form.is_valid():
			staff = form.save(commit=False)
			#other options before save
			staff.save()
			#Send mail to all staff
			#Publish in dashboard staff
			return HttpResponseRedirect('/staff/')
	else:
		form = StaffForm()
	return render_to_response('staff/post.html', 
		{'form':form}, context_instance=RequestContext(request))



def staff(request):
	members = Staff.objects.all().order_by('name')
	return render_to_response('staff/staff.html', 
		{'members':members}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def new_member(request):
	if request.method == 'POST':
		form = NewMemberForm(request.POST)
		if form.is_valid():
			new = User.objects.create(
				username=form.cleaned_data['username'],
				first_name=form.cleaned_data['first_name'],
				last_name=form.cleaned_data['last_name'],
				password=form.cleaned_data['password'],
				last_login=datetime.datetime.now(),
				is_superuser=form.cleaned_data['is_superuser'],
			)
			new.set_password(form.cleaned_data['password']) 
			new.is_staff = True
			new.save()
			return HttpResponseRedirect('/admin/staff/all-staff/')
	else:
		form = NewMemberForm()
	return render_to_response('admin/staff/new_staff.html', 
		{'form':form}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def edit_member(request, memberID):
	member = get_object_or_404(User, pk=memberID)
	if request.method == 'POST':
		form = NewMemberForm(request.POST)
		if form.is_valid():
			member.username = form.cleaned_data['username']
			member.first_name = form.cleaned_data['first_name']
			member.last_name = form.cleaned_data['last_name']
			member.set_password(form.cleaned_data['password']) 
			member.is_superuser = form.cleaned_data['is_superuser']
			member.is_staff = True
			member.save()
			return HttpResponseRedirect('/admin/staff/all-staff/')
	else:
		form = NewMemberForm(initial={
			'username':member.username,
			'first_name':member.first_name,
			'last_name':member.last_name,
			'password':member.password,
			'is_superuser':member.is_superuser,
			})
	return render_to_response('admin/staff/edit_staff.html', 
		{'form':form,'member':member}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def delete_member(request,memberID):
	member = get_object_or_404(User, pk=memberID)
	member.delete()
	return HttpResponseRedirect('/admin/staff/all-staff/')





def get_points(member):
	points = 0
	if member.question2 == 'Giver':
		points += 1
	if member.question3 == 'He who does not live to serve does not deserve to live':
		points += 1
	if member.question5 == 'One round world ticket':
		points += 1
	if member.question6 == 'Always':
		points += 1
	if member.question7 == 'Adventure is out there':
		points += 1
	if member.question8 == 'Not taking no for an answer, going above and beyond your duty in order to best benefit your team':
		points += 1
	if member.question9 == 'If you do not ask the question, the answer will always be no':
		points += 1
	if member.question10 == 'I wonder what troubles him/her?':
		points += 1
	return points

def get_points2(member):
	points = 0
	if member.question12 == 'He who does not live to serve does not deserve to live':
		points += 1
	if member.question14 == 'Adventure is out there':
		points += 1
	if member.question15 == 'Not taking no for an answer, going above and beyond your duty in order to best benefit your team':
		points += 1
	if member.question16 == 'If you do not ask the question, the answer will always be no':
		points += 1
	if member.question17 == 'I wonder what troubles him/her?':
		points += 1
	if member.question24 == 'YES':
		points += 1
	return points


def joinus(request):
	done = False
	if request.method == 'POST':
		form = JoinUsForm(request.POST)
		if form.is_valid():
			member = form.save(commit=False)
			member.points = get_points(member)
			member.save()
			#Send Mail to staff
			#to = settings.STAFF_EMAIL
			#context_render = {'member':member}
			#subject ='ISE | We have a guy who wants be staff.'
			#template = 'emails/joinus.html'
			#Email(to,subject,context_render,template).send()					
			return HttpResponseRedirect('/joinus/?done=yes')
	else:
		if request.GET.__contains__('done'):
			if request.GET['done'] == 'yes':
				done = True
		form = JoinUsForm()
	return render_to_response('staff/join.html', 
		{'form':form,'done':done}, context_instance=RequestContext(request))


def joinus2(request):
	done = False
	if request.method == 'POST':
		form = JoinUs2Form(request.POST)
		if form.is_valid():
			member = form.save(commit=False)
			member.points = get_points2(member)
			member.save()
			#Send Mail to staff
			#to = settings.STAFF_EMAIL
			#context_render = {'member':member}
			#subject ='ISE | We have a guy who wants be staff.'
			#template = 'emails/joinus.html'
			#Email(to,subject,context_render,template).send()					
			return HttpResponseRedirect('/joinus/?done=yes')
	else:
		if request.GET.__contains__('done'):
			if request.GET['done'] == 'yes':
				done = True
		form = JoinUs2Form()
	return render_to_response('staff/join2.html', 
		{'form':form,'done':done}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
def joinus_records(request):
	records = JoinUs.objects.all().order_by('-points')
	return render_to_response('staff/joinrecords.html', 
		{'records':records}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
def joinus2_records(request):
	records = JoinUs2.objects.all().order_by('-points')
	return render_to_response('staff/join2records.html', 
		{'records':records}, context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
def joinus3_records(request):
	records = JoinUs2.objects.filter(timestamp__gte=datetime.date(2015, 4, 20)).order_by('-points')
	return render_to_response('staff/join2records.html', 
		{'records':records}, context_instance=RequestContext(request))






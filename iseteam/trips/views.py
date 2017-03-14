from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from django.db.models import Count
from django.contrib.auth.models import User
from django.conf import settings
from django.views.generic import DeleteView, ListView

from django.contrib.auth import authenticate, login

from iseteam.trips.forms import TripForm, BusCheckInForm, PayTripForm, ImageTripForm, SignUpForm
from iseteam.trips.forms import LogInForm, RoomForm, MultipleRoomForm, BusForm, MultipleBusForm
from iseteam.trips.models import Trip, BusCheckIn, PayTrip, Confirmation, Room, ImageTrip, GalleryTrip,\
    PaymentAssignment
from iseteam.trips.models import CardPayment
from iseteam.email import Email

from iseteam.response import JSONResponse, response_mimetype
from iseteam.serialize import serialize

from iseteam.trips.decorators import login_required_staff

import datetime
import json
import stripe


def login_trip(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/trips/pay/%s/' % trip.pk)
            else:
                return HttpResponse('Invalid username or password, please try again.')


def signup(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create User
            now = datetime.datetime.now()
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                last_login=now,  # Why is this happening
            )
            password = form.cleaned_data['password1']
            new_user.set_password(password)
            new_user.save()
            # Associate user's info to perfil user extension
            new_user.userextension.university = form.cleaned_data['university']
            new_user.userextension.age = form.cleaned_data['age']
            new_user.userextension.gender = form.cleaned_data['gender']
            new_user.userextension.country = form.cleaned_data['country']
            new_user.userextension.save()
            # Login and redirect directly to pay trip
            user = authenticate(username=new_user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                return HttpResponse('Something went wrong, please try again')
            return HttpResponseRedirect('/trips/pay/%s/' % trip.pk)
    else:
        form = SignUpForm()
    return render_to_response('trips/signup.html',
                              {'form': form}, context_instance=RequestContext(request))


def card_payment(request, paytripID):
    paytrip = get_object_or_404(PayTrip, pk=paytripID)
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_LIVE_SECRET
        token = request.POST['stripeToken']
        amount = paytrip.trip.get_price_zeros()
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="mxn",
                source=token,
                description="Viaje %s" % paytrip.trip.name,
            )
        except stripe.error.CardError as e:
            new_card_payment = CardPayment.objects.create(  # If not used it, created but not assigned
                paytrip=paytrip,
                amount=amount,
                token=token,
                status=str(e),
            )
            # Return Error Message
            error_message = e
            return render_to_response('trips/cardpayment.html',
                                      {'error_message': e, 'trip': paytrip.trip},
                                      context_instance=RequestContext(request))

        # Save CardPayment Reference
        new_card_payment = CardPayment.objects.create(  # If not used it, created but not assigned
            paytrip=paytrip,
            amount=amount,
            token=token,
            status='paid',
        )
        # Changing paytrip to paid and delivered it sends automatically email of confirmation
        paytrip.is_paid = True
        paytrip.is_delivered = True
        paytrip.save()
        confirmation = generate_confirmation(paytrip)  #  Look into it
        # Return Successfully payment page with your confirmation number
        return render_to_response('trips/cardsuccessful.html',
                                  {'confirmation': paytrip.confirmation},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('trips/cardpayment.html',
                                  {'trip': paytrip.trip},
                                  context_instance=RequestContext(request))
    return HttpResponse(charge.status)


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def admin_all_trips(request):
    trips = Trip.objects.all().order_by('-date')
    return render_to_response('admin/trips/all_trips.html',
                              {'trips': trips},
                              context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def post(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            # other options before save
            trip.save()
            # Send mail to all staff
            # Publish in dashboard staff
            return HttpResponseRedirect('%s' % trip.get_absolute_url())
    else:
        form = TripForm()
    return render_to_response('admin/trips/new_trip.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def edit_trip(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            edited_trip = form.save()
            return HttpResponseRedirect('/trips/%s' % trip.slug)
    else:
        form = TripForm(instance=trip)
    return render_to_response('admin/trips/edit-trip.html',
                              {'form': form, 'trip': trip},
                              context_instance=RequestContext(request))


@login_required_staff(login_url='/login/')
@login_required(login_url='/login/')
def delete_trip(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    trip.delete()
    return HttpResponseRedirect('/admin/trips/all-trips/')


# staff permissions
# @login_required(login_url='/login/')
def pay(request, trip):
    trip = get_object_or_404(Trip, pk=trip)
    if request.method == 'POST':
        form = PayTripForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.trip = trip
            payment.save()
            # Saving membership if it existed
            try:
                user = User.objects.get(email=payment.email)
            except User.DoesNotExist:
                pass
            else:
                if payment.membership == 'yes':
                    user.userextension.membership = True
                    user.userextension.save()
            # Send Mail to staff
            to = settings.STAFF_EMAIL
            context_render = {'pay': payment}
            subject = 'ISE | Someone has purchased a trip.'
            template = 'emails/paytrip_staff.html'
            Email(to,subject,context_render,template).send()

            # Redirect to view where they can pay
            if payment.method == 'card':
                return HttpResponseRedirect('%s/trips/cardpayment/%s/' % (settings.SITE_URL, payment.pk))

            # Send mail to buyer or called first mail
            first_mail(payment)

            return render_to_response('trips/pay.html',
                                      {'form': form, 'trip': trip, 'successfully': True},
                                      context_instance=RequestContext(request))

    else:
        form = PayTripForm()
    return render_to_response('trips/pay.html',
                              {'form': form, 'trip': trip},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def edit_payment(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    if request.method == 'POST':
        form = PayTripForm(request.POST, instance=payment)
        if form.is_valid():
            edited_payment = form.save(commit=False)
            edited_payment.staff = None
            edited_payment.save()
            return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)
    else:
        form = PayTripForm(instance=payment)
    return render_to_response('trips/edit_payment.html',
                              {'form': form, 'payment': payment},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def mark_as_unpaid(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    payment.is_paid = False
    payment.save()
    return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)


@staff_member_required
@login_required(login_url='/login/')
def mark_as_undelivered(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    payment.is_delivered = False
    payment.confirmation.delete()
    payment.save()
    return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)


@staff_member_required
@login_required(login_url='/login/')
def send_first_mail(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    first_mail(payment)
    return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)


@staff_member_required
@login_required(login_url='/login/')	
def send_confirmation_mail(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    if payment.is_paid:
        confirmation_mail(payment, payment.confirmation)
    return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)


@staff_member_required
@login_required(login_url='/login/')
def delete_payment(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    payment.delete()
    return HttpResponseRedirect('/trips/%s/payments/' % payment.trip.pk)


def view(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    return render_to_response('trips/view.html',
                              {'trip': trip},
                              context_instance=RequestContext(request))


def view_queretaro(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    return render_to_response('trips/view_queretaro.html',
                              {'trip': trip},
                              context_instance=RequestContext(request))


def view_toluca(request, slug):
    trip = get_object_or_404(Trip, slug=slug)
    return render_to_response('trips/view_toluca.html',
                              {'trip': trip},
                              context_instance=RequestContext(request))


# View all trips mty
def trips(request):
    trips = Trip.objects.filter(city="Mty").order_by('-date')[:5]
    return render_to_response('trips/trips.html',
                              {'trips': trips},
                              context_instance=RequestContext(request))


# View all events
def trips_queretaro(request):
    trips = Trip.objects.filter(city="Qro").order_by('-date')[:5]
    return render_to_response('trips/trips_queretaro.html',
                              {'trips': trips},
                              context_instance=RequestContext(request))


def trips_toluca(request):
    trips = Trip.objects.filter(city="Toluca").order_by('-date')[:5]
    return render_to_response('trips/trips_toluca.html',
                              {'trips': trips},
                              context_instance=RequestContext(request))


# View of hotel checkin
def hotel(request, tripID, confirmation, roomID):
    trip = get_object_or_404(Trip, pk=tripID)

    try:
        confirmation = Confirmation.objects.get(code=confirmation)
        room = Room.objects.get(pk=roomID)
    except:  # Why naked exceptions
        return HttpResponse(json.dumps({'done': 'no'}), content_type='application/json')

    if not confirmation.has_room and confirmation.payment.is_paid:
        room.roomates.add(confirmation)
        room.available_rooms -= 1
        confirmation.has_room = True
        room.save()
        confirmation.save()
        if room.available_rooms <= 0:
            room.is_full = True
            room.save()
            hotel_mail(roomID)
        return HttpResponse(json.dumps({'done': 'yes', 'room': room.name,
                                        'fullname': '%s %s' % (confirmation.payment.name,
                                                               confirmation.payment.last_name)}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'done': 'no'}), content_type='application/json')


# View of bus checkin
def bus(request):
    if request.method == 'POST':
        form = BusCheckInForm(request.POST)
        if form.is_valid():
            buscheckin = form.save(commit=False)
            # other options before save
            if code_is_valid(buscheckin.confirmation):
                buscheckin.save()
                buscheckin.bus.available_seats -= 1
                if buscheckin.bus.available_seats <= 0:
                    buscheckin.bus.is_full = True
                buscheckin.bus.save()
                # Send mail to client
                bus = buscheckin.bus.name
                confirmation = Confirmation.objects.get(code=buscheckin.confirmation)
                bus_mail(confirmation, bus)
                return HttpResponse(json.dumps({'done': 'yes'}), content_type='application/json')

            else:
                return HttpResponse(json.dumps({'done': 'no'}), content_type='application/json')


@staff_member_required
@login_required(login_url='/login/')
def hotel_records(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    rooms = Room.objects.filter(trip=trip)
    add_room_form = RoomForm(initial={'trip': trip})
    add_multiple_room_form = MultipleRoomForm(initial={'trip': trip})
    return render_to_response('admin/trips/rooms.html',
                              {'rooms': rooms, 'trip': trip, 'add_room_form': add_room_form,
                               'add_multiple_room_form': add_multiple_room_form},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_add_one_room(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    form = RoomForm(request.POST, initial={'trip': trip})
    if form.is_valid():
        room = form.save(commit=False)
        room.save()
        action_url = reverse('admin_hotel_records_add_one_room', kwargs={'tripID': tripID})
        create_label = 'Add Room'
        title = 'Add One Room'
        return render_to_response('admin/modal-inner-form.html',
                                  {'form': form, 'action_url': action_url, 'create_label': create_label,
                                   'mode': 'create', 'title': title, 'reload_when_submit_success': True},
                                  context_instance=RequestContext(request))
    raise Http404("Invalid data provided")


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_add_multiple_room(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    form = MultipleRoomForm(request.POST, initial={'trip': trip})
    if form.is_valid():
        rooms = form.save()
        action_url = reverse('admin_hotel_records_add_multiple_room', kwargs={'tripID': tripID})
        create_label = 'Add Rooms'
        title = 'Add Multiple Room'
        return render_to_response('admin/modal-inner-form.html',
                                  {'form': form, 'action_url': action_url, 'create_label': create_label,
                                   'mode': 'create', 'title': title, 'reload_when_submit_success': True},
                                  context_instance=RequestContext(request))
    raise Http404("Invalid data provided")


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_edit_room(request, tripID, roomID):
    trip = get_object_or_404(Trip, pk=tripID)
    rooms = trip.rooms
    room = rooms.filter(pk=roomID).first() if rooms.exists() else None

    if room is None:
        raise Http404("Room does not exists")

    form = RoomForm(request.POST, instance=room) if request.method == 'POST' else RoomForm(instance=room)
    if request.method == 'POST' and form.is_valid():
        form.save()
    update_label = 'Save Changes'
    title = 'Edit Room'
    action_url = reverse('admin_hotel_records_edit_room', kwargs={'tripID': tripID, 'roomID': roomID})
    return render_to_response('admin/modal-inner-form.html',
                              {'form': form, 'action_url': action_url, 'update_label': update_label,
                               'mode': 'update', 'title': title, 'reload_when_submit_success': True},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_remove_room(request, tripID, roomID):
    trip = get_object_or_404(Trip, pk=tripID)
    rooms = trip.rooms
    room = rooms.filter(pk=roomID).first() if rooms.exists() else None

    if room is None:
        raise Http404("Room does not exists")

    if not room.can_remove:
        raise Http404("Room can not be removed")

    room.delete()
    url = reverse('admin_hotel_records', kwargs={'tripID': tripID})
    return redirect(url)


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_move_to(self, tripID, confirmation, roomID):
    trip = get_object_or_404(Trip, pk=tripID)
    rooms = trip.rooms
    room = rooms.filter(pk=roomID).first() if rooms.exists() else None

    if room is None:
        raise Http404("Room does not exists")

    confirmations = trip.confirmations

    confirmation = confirmations.filter(id=confirmation).first() if confirmations.exists() else None

    if confirmation is None:
        raise Http404("Confirmation does not exists")

    original_room = confirmation.room_set.first()
    if original_room is None:
        raise Http404("Original Room does not exists")
    original_room.move_to(confirmation, room)
    url = reverse('admin_hotel_records', kwargs={'tripID': tripID})
    return redirect(url)


@staff_member_required
@login_required(login_url='/login/')
def bus_records(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    buses = trip.get_buses_grouped()
    add_bus_form = BusForm(initial={'trip': trip})
    add_multiple_bus_form = MultipleBusForm(initial={'trip': trip})
    return render_to_response('admin/trips/buses.html',
                              {'buses': buses, 'trip': trip, 'add_bus_form': add_bus_form,
                               'add_multiple_bus_form': add_multiple_bus_form},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def admin_bus_records_add_one_bus(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    form = BusForm(request.POST, initial={'trip': trip})
    if form.is_valid():
        room = form.save()
        action_url = reverse('admin_bus_records_add_one_bus', kwargs={'tripID': tripID})
        create_label = 'Add Bus'
        title = 'Add One Bus'
        return render_to_response('admin/modal-inner-form.html',
                                  {'form': form, 'action_url': action_url, 'create_label': create_label,
                                   'mode': 'create', 'title': title, 'reload_when_submit_success': True},
                                  context_instance=RequestContext(request))
    raise Http404("Invalid data provided")


@staff_member_required
@login_required(login_url='/login/')
def admin_hotel_records_add_multiple_bus(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    form = MultipleBusForm(request.POST, initial={'trip': trip})
    if form.is_valid():
        buses = form.save()
        action_url = reverse('admin_hotel_records_add_multiple_bus', kwargs={'tripID': tripID})
        create_label = 'Add Buses'
        title = 'Add Multiple Buses'
        return render_to_response('admin/modal-inner-form.html',
                                  {'form': form, 'action_url': action_url, 'create_label': create_label,
                                   'mode': 'create', 'title': title, 'reload_when_submit_success': True},
                                  context_instance=RequestContext(request))
    raise Http404("Invalid data provided")


@staff_member_required
@login_required(login_url='/login/')
def manage_buses(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    buses = trip.buses.all()
    return render_to_response('admin/trips/manage_buses.html',
                              {'buses': buses, 'trip': trip},
                              context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def add_bus(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    if request.method == 'POST':
        form = BusForm(request.POST)  # Where is the BusForm
        if form.is_valid():
            new_bus = form.save()
            trips.buses.add(new_bus)
    else:
        form = BusForm()  # Where is the BusForm
    return render_to_response('admin/trips/add_bus.html',
                              {'form': form},
                              context_instance=RequestContext(request))



@staff_member_required
@login_required(login_url='/login/')
def bus_records2(request):
    trip = get_object_or_404(Trip, pk=7)
    buses = trip.get_buses_grouped()
    return render_to_response('trips/bus_records.html',
                              {'buses': buses, 'trip': trip},
                              context_instance=RequestContext(request))


@staff_member_required	
@login_required(login_url='/login/')
def payment_records(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)

    order = 'timestamp'

    if request.GET.__contains__('order_by'):
        if request.GET['order_by'] == 'date':
            records = PayTrip.objects.filter(trip=trip).order_by('-timestamp')
        if request.GET['order_by'] == 'status':
            records = PayTrip.objects.filter(trip=trip).order_by('-is_paid', '-is_delivered')
    else:
        records = PayTrip.objects.filter(trip=trip)

    staff_list = PayTrip.objects.filter(trip=trip, is_paid=True).values('staff').\
        annotate(Count('staff')).order_by('staff')
    sales = []
    for v in staff_list:
        if not v['staff'] == None:  # Wrong comparison
            sales.append({'staff': User.objects.get(pk=v['staff']).get_full_name(), 'quantity': v['staff__count']})

    genders = PayTrip.objects.filter(trip=trip, is_paid=True).values('gender').annotate(Count('gender'))

    mexicans = PayTrip.objects.filter(country='Mexico', trip=trip, is_paid=True).count()
    foreigners = PayTrip.objects.filter(trip=trip, is_paid=True).count() - mexicans

    itesm = PayTrip.objects.filter(university='ITESM', trip=trip, is_paid=True).count()
    udem = PayTrip.objects.filter(university='UDEM', trip=trip, is_paid=True).count()
    uanl = PayTrip.objects.filter(university='UANL', trip=trip, is_paid=True).count()
    ur = PayTrip.objects.filter(university='UR', trip=trip, is_paid=True).count()
    cedim = PayTrip.objects.filter(university='CEDIM', trip=trip, is_paid=True).count()
    egade = PayTrip.objects.filter(university='EGADE', trip=trip, is_paid=True).count()
    working	= PayTrip.objects.filter(university='WORKING', trip=trip, is_paid=True).count()
    other = PayTrip.objects.filter(university='OTHER', trip=trip, is_paid=True).count()

    delivered = PayTrip.objects.filter(is_delivered=True, trip=trip).count()
    paid = PayTrip.objects.filter(is_paid=True, trip=trip).count()
    still = PayTrip.objects.filter(is_paid=False, trip=trip).count()

    staff = User.objects.filter(is_staff=True, is_active=True).order_by('-first_name')

    return render_to_response('admin/trips/payments.html',
                              {'records': records, 'trip': trip, 'sales': sales, 'genders': genders,
                               'mexicans': mexicans, 'foreigners': foreigners, 'itesm': itesm, 'udem': udem,
                               'uanl': uanl, 'ur': ur, 'cedim': cedim, 'egade': egade, 'working': working,
                               ' other': other, 'paid': paid, 'still': still, 'staff': staff, 'fullsize': True,
                               'delivered': delivered}, context_instance=RequestContext(request))


@staff_member_required
@login_required(login_url='/login/')
def payment_records_excel(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    records = PayTrip.objects.filter(trip=trip).order_by('timestamp')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-payments.csv"' % trip.name
    csv_data = []
    count = 1
    for record in records:  # Why don't create a method on the trip to do this and could be reused
        if record.is_paid:
            status = "Paid."
            confirmation = record.confirmation.code
        else:
            status = "Pending."
            confirmation = "No code yet."

        if record.staff:
            staff = record.staff.get_full_name()
        else:
            staff = "No Staff yet."
        csv_data.append((
            count,
            record.name,
            record.last_name,
            record.email,
            record.university,
            record.age,
            record.gender,
            record.country,
            record.method,
            record.timestamp,
            status,
            staff,
            confirmation,
            ))
        count += 1
    t = loader.get_template('payments_excel.txt')
    c = Context({
        'data': csv_data,
                })
    response.write(t.render(c))
    return response


@staff_member_required	
@login_required(login_url='/login/')
def buses_records_excel(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    records = BusCheckIn.objects.filter(trip=trip).order_by('bus')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-buses.csv"' % trip.name
    csv_data = []
    count = 1
    for record in records:  # Why don't create a method on the trip to do this and could be reused
        csv_data.append((
            count,
            record.name,
            record.last_name,
            record.confirmation,
            record.timestamp,
            record.bus,
            ))
        count += 1
    t = loader.get_template('buses_excel.txt')  # Should be a parameter not hard coded
    c = Context({
        'data': csv_data,
                })
    response.write(t.render(c))
    return response


@staff_member_required	
@login_required(login_url='/login/')
def see_history(request, paytripID):
    payment = get_object_or_404(PayTrip, pk=paytripID)
    records = PaymentAssignment.objects.filter(paytrip=payment)
    tr_content = ""
    for record in records:
        tr_content += "<tr><td>%s</td><td>%s</td></tr>" % (record.staff.get_full_name(), record.timestamp)
    html = "<table class='table'><thead><tr><th>Last change made by...</th><th>Date</th></tr></thead><tbody class='text-left'><tr>%s</tr></tbody></table>" % tr_content  # Why don't use a template
    return HttpResponse(html)


@staff_member_required	
@login_required(login_url='/login/')
def hotel_records_excel(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    rooms = Room.objects.filter(trip=trip)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-rooms.csv"' % trip.name
    csv_data = []

    for room in rooms:  # Why don't create a method on the trip to do this and could be reused
        count = 1
        for roomate in room.roomates.all():
            csv_data.append((
                count,
                roomate.payment.name,
                roomate.payment.last_name,
                room,
                ))
            count += 1
    t = loader.get_template('hotel_excel.txt')
    c = Context({
        'data': csv_data,
                })
    response.write(t.render(c))
    return response


@staff_member_required
@login_required(login_url='/login/')
def assign_staff(request, paymentID, staffID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    staff = User.objects.get(pk=staffID)
    payment.staff = staff
    payment.save()
    assignment = PaymentAssignment.objects.create(paytrip=payment, staff=staff)

    response_json = json.dumps({'success': 'true', 'staff': '%s' % staff.get_full_name()})  # Why does it use old string formatting when it's a simple value asignment
    return HttpResponse(response_json)


@staff_member_required
@login_required(login_url='/login/')
def pay_trip(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    payment.is_paid = True
    payment.save()
    confirmation = generate_confirmation(payment)

    response = {'success': 'true', 'confirmation': payment.confirmation.code, 'client': payment.get_full_name()}

    return HttpResponse(json.dumps(response))

@staff_member_required
@login_required(login_url='/login/')
def delivered_trip(request, paymentID):
    payment = get_object_or_404(PayTrip, pk=paymentID)
    payment.is_delivered = True
    payment.save()
    confirmation = generate_confirmation(payment)

    response = {'success': 'true', 'client': payment.get_full_name()}

    return HttpResponse(json.dumps(response))


# Return html of trips
def trips_html(request):
    trips = Trip.objects.filter(date__gte=datetime.datetime.now()).order_by('-date')
    html = "<option value='' selected='selected'>Select Trip</option>"
    for trip in trips:
        html += ("<option value=" + str(trip.pk) + ">" + trip.name + "</option>")
    return HttpResponse(html)


def buses_html(request, tripID):
    trip = Trip.objects.get(pk=tripID)
    html = "<option value='' selected='selected'>Select a Bus</option>"
    for bus in trip.buses.filter(is_full=False):
        html += ("<option value=" + str(bus.pk) + ">" + bus.name + ":::::" + str(bus.available_seats) + " Left" + "</option>")  # What????????? Use string format
    return HttpResponse(html)


def rooms_html(request, tripID):
    trip = Trip.objects.get(pk=tripID)
    rooms = Room.objects.filter(trip=trip, is_full=False)
    html = "<option value='' selected='selected'>Select a Room</option>"
    for room in rooms:
        html += ("<option value=" + str(room.pk) + ">" + room.name + ":::::" + str(room.available_rooms) + " Left" + "</option>")  # What????????? Use string format
    return HttpResponse(html)




# Why don't you put this on separated file?
'''
Some functions used   # Wrong use of comments
'''
import hashlib


def first_mail(payment):
    # Send mail to buyer
    to1 = payment.email
    subject1 = 'ISE | TRIP ORDER CONFIRMATION.'
    context_render = {'pay': payment}
    template1 = 'emails/paytrip.html'
    if payment.method == "bankdeposit":
        template1 = 'emails/paytripbank.html'
    if payment.method == "banktransfer":
        template1 = 'emails/paytriptransfer.html'
    if payment.method == "staff":
        template1 = 'emails/paytripstaff.html'
    if payment.method == "paypal":
        template1 = 'emails/paytrippaypal.html'
    Email([to1], subject1, context_render, template1).send()


def confirmation_mail(payment, code):
    to1 = payment.email
    subject1 = 'ISE | CONFIRMATION NUMBER OF %s' % payment.trip.name.upper()
    context_render = {'confirmation': code}
    template1 = 'emails/payconfirmation.html'
    Email([to1, ], subject1, context_render, template1).send()


def bus_mail(confirmation, bus):
    to = confirmation.payment.email
    subject = 'ISE | BUS CHECK-IN IS DONE TO %s' % confirmation.payment.trip.name.upper()
    context_render = {'confirmation': confirmation, 'bus': bus}
    template = 'emails/busconfirmation.html'
    Email([to], subject, context_render, template).send()


def hotel_mail(roomID):
    room = Room.objects.get(pk=roomID)
    to = []
    for r in room.roomates.all():
        to.append(r.payment.email)
    subject = 'ISE | YOUR ROOMMATES ARE READY FOR YOU'
    context_render = {'room': room}
    template = 'emails/hotelconfirmation.html'
    Email(to, subject, context_render, template).send()


def generate_confirmation(payment):
    import random

    code = hashlib.sha224('%s%s%s' % (payment.pk, str(payment.age), str(random.random()))).hexdigest()[10:18]  # Break into small code and user string format
    code = code.upper()
    try:
        Confirmation.objects.get(payment=payment)
    except Confirmation.DoesNotExist:
        c = Confirmation.objects.create(payment=payment, code=code)
        # Send Mail Send Mail Send Mail Send Mail Send Mail
        confirmation_mail(payment, c)
    else:
        pass


def code_is_valid(code):
    try:
        confirmation = Confirmation.objects.get(code=code)
    except Confirmation.DoesNotExist:
        return False
    if not confirmation.is_used and confirmation.payment.is_paid:
        confirmation.is_used = True
        confirmation.save()
        return True
    else:
        return False


# Gallery Functions
def upload_gallery(request, tripID):
    trip = get_object_or_404(Trip, pk=tripID)
    # Get or create new gallery
    gallery = GalleryTrip.objects.get_or_create(trip=trip)

    if request.method == 'POST':
        form = ImageTripForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save()
            # Add image to gallery
            gallery[0].images.add(picture)
            # Serialize image
            files = [serialize(picture)]
            data = {'files': files}
            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            print response  # Why a print here?
            return response
        else:
            print form.errors
    else:
        form = ImageTripForm()
    return render_to_response('trips/picture_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def picture_create2(request):
    if request.method == 'POST':
        form = ImageTripForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save()
            files = [serialize(picture)]
            data = {'files': files}
            response = JSONResponse(data, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
    else:
        form = ImageTripForm()
    return render_to_response('trips/picture_basicplus_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))


class PictureDeleteView(DeleteView):
    model = ImageTrip

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()  # Look into this
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = ImageTrip
    template_name_suffix = '_jquery_form'

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(p) for p in self.get_queryset()]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

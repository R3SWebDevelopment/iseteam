from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
import datetime

from autoslug import AutoSlugField

from iseteam.pictures.models import make_upload_path

import calendar

from django.db.models.signals import post_save

CITY_CHOICES = (
    ('Mty', 'Monterrey'),
    ('Qro', 'Queretaro'),
    ('Toluca', 'Toluca'),
)


class UserExtension(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=255, choices=CITY_CHOICES, default='Mty', blank=True, null=True)

    # PROFILE INFO
    university = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True,null=True)
    country = models.CharField(max_length=255, blank=True,null=True)
    membership = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.user

    # Create profile when new user
    def create_user_extension(sender, instance, created, **kwargs):  # Why sender and not self?
        if created:
            UserExtension.objects.create(user=instance)

    # Signal to create user profile
    post_save.connect(create_user_extension, sender=User)


class Bus(models.Model):
    name = models.CharField(max_length=255)
    total_seats = models.IntegerField(default=42)
    available_seats = models.IntegerField(default=42)
    is_full = models.BooleanField(default=False)

    def is_seat_number_available(self, seat_number):
        if seat_number <= self.total_seats and not self.is_full:
            for seat in self.seat_list:
                if seat['number'] == seat_number:
                    return not seat['occupied']
        return False

    @property
    def available_seat_list(self):
        seats = self.seat_list
        available_seats = []
        for seat in seats:
            if not seat['occupied']:
                available_seats.append(seat)
        return available_seats

    @property
    def seat_list(self):
        seat_list = []
        seats = self.seats
        for seat_number in range(1, self.total_seats+1):
            seat = seats.filter(seat_number=seat_number).first() if seats.exists() else None
            occupied = True if seat is not None else False
            occupant = seat.full_name if seat is not None else None
            seat_list.append({
                'number': seat_number,
                'occupied': occupied,
                'occupant': occupant,
            })
        return seat_list

    @property
    def first_available_seat_number(self):
        if self.is_full:
            return None
        for seat_number in self.seat_list:
            if not seat_number['occupied']:
                return seat_number['number']

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_seats = self.total_seats
        super(Bus, self).save(*args, **kwargs)

    @property
    def edit_is_allow(self):
        trip = self.trips.first()
        return trip.edit_is_allow if trip is not None else False

    def figure_bus_availability(self):
        if self.available_seats <= 0:
            self.is_full = True
        else:
            self.is_full = False
        self.save()

    @property
    def has_occupants(self):
        if self.is_full or self.available_seats < self.total_seats:
            return True
        return False

    @property
    def can_remove(self):
        if self.edit_is_allow and not self.has_occupants:
            return True
        return False

    @property
    def trips(self):
        return self.trip_set.all()

    @property
    def seats(self):
        return self.buscheckin_set.all()

    @property
    def can_change_roomate(self):
        if self.edit_is_allow:
            return True
        return False

    def add_occupant(self):
        self.available_seats -= 1
        self.save()
        self.figure_bus_availability()

    def remove_occupant(self):
        self.available_seats += 1
        self.save()
        self.figure_bus_availability()


class Trip(models.Model):
    city = models.CharField(max_length=255, choices=CITY_CHOICES, default='Mty')
    name = models.CharField(max_length=1024)
    date = models.DateField()
    price_presale = models.IntegerField(blank=True, null=True)
    price_sale = models.IntegerField(blank=True, null=True)
    tickets = models.URLField(max_length=124, blank=True, null=True)
    facebook = models.URLField(max_length=124, blank=True, null=True)
    video = models.URLField(max_length=256, blank=True, null=True)
    cover = models.ImageField(upload_to=make_upload_path)
    brief = models.CharField(max_length=1024)
    description = models.CharField(max_length=10240)
    buses = models.ManyToManyField(Bus)
    slug = AutoSlugField(populate_from='name', max_length=255, unique_with='date')
    is_full = models.BooleanField(default=False)

    @property
    def edit_is_allow(self):
        now = datetime.datetime.now()
        if self.date >= now.date():
            return True
        return False

    def __unicode__(self):
        return u'%s' % self.name

    def get_price_zeros(self):
        return int(self.price_sale * 100)  # Might need casting of type

    def get_youtube_id(self):
        return self.video.split("v=")[1]

    def get_vimeo_id(self):
        return self.video.split('com/')[1]

    def is_youtube(self):
        if 'youtube' in str(self.video):
            return True
        return False

    def is_vimeo(self):
        if 'vimeo' in str(self.video):
            return True
        return False

    @models.permalink
    def get_absolute_url(self):
        if self.slug:
            return ('view_trip', (self.slug,))  # What it's this for?
        return ('view_trip', (self.id,))  # What it's this for?

    @models.permalink
    def get_queretaro_url(self):
        if self.slug:
            return ('view_trip_queretaro', (self.slug,))  # What it's this for?
        return ('view_trip_queretaro', (self.id,))  # What it's this for?

    def get_cover_url(self):
        return str(self.cover.url).split("?")[0]

    @property
    def get_buses(self):
        return self.buses.all().order_by('name')

    @property
    def buses_with_available_seat(self):
        buses = self.get_buses
        buses = buses.filter(available_seats__gte=1) if buses.exists() else buses
        return buses

    def remove_bus(self, bus):
        self.buses.remove(bus)
        if not bus.trips.exists():
            bus.delete()

    def get_buses_grouped(self):
        from iseteam.trips.models import BusCheckIn  # Why not in the head of the file as all imports?

        all_seats = BusCheckIn.objects.filter(trip=self)

        seats = []

        for bus in self.buses.all():
            bus_container = []
            for seat in all_seats:
                if seat.bus == bus:
                    bus_container.append(seat)
            seats.append({'bus': bus.name, 'seats': bus_container})

        return seats

    @property
    def rooms(self):
        return self.room_set.all()

    @property
    def rooms_with_available_capacity(self):
        rooms = self.rooms
        rooms = rooms.filter(available_rooms__gte=1) if rooms.exists() else rooms
        return rooms

    @property
    def confirmations(self):
        return Confirmation.objects.filter(id__in=[c.get('roomates__id') for c in self.rooms.values('roomates__id')])

    def add_bus(self, bus):
        self.buses.add(bus)

    @property
    def seats_confirmed(self):
        return self.buscheckin_set.all()


class ImageTrip(models.Model):
    file = models.ImageField(upload_to=make_upload_path)

    def __unicode__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        super(ImageTrip, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(ImageTrip, self).delete(*args, **kwargs)

    def get_url(self):
        return str(self.file.url).split("?")[0]


class GalleryTrip(models.Model):
    trip = models.OneToOneField(Trip)
    name = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField()
    month = models.CharField(max_length=255)
    images = models.ManyToManyField(ImageTrip)

    def __unicode__(self):
        return u'%s' % self.trip

    def save(self, *args, **kwargs):
        self.name = self.trip.name
        self.year = self.trip.date.year
        self.month = calendar.month_name[self.trip.date.month]
        super(GalleryTrip, self).save(*args, **kwargs)

    def get_thumbs(self):
        return self.images.all()[:4]

    @models.permalink
    def get_absolute_url(self):
        if self.trip.slug:
            return ('view_album', (self.trip.slug,))  # What it's this for?
        return ('view_trip', (self.trip.id,))  # What it's this for?


class HotelCheckIn(models.Model):
    trip = models.ForeignKey(Trip)
    timestamp = models.DateTimeField(auto_now_add=True)
    name1 = models.CharField(max_length=255)
    last_name1 = models.CharField(max_length=255)
    confirmation1 = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255)
    last_name2 = models.CharField(max_length=255)
    confirmation2 = models.CharField(max_length=255)
    name3 = models.CharField(max_length=255)
    last_name3 = models.CharField(max_length=255)
    confirmation3 = models.CharField(max_length=255)
    name4 = models.CharField(max_length=255)
    last_name4 = models.CharField(max_length=255)
    confirmation4 = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s,%s,%s,%s' % (self.name1, self.name2, self.name3, self.name4)


class BusCheckIn(models.Model):
    trip = models.ForeignKey(Trip)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    confirmation = models.CharField(max_length=255)
    bus = models.ForeignKey(Bus)
    seat_number = models.IntegerField(null=True)

    class Meta:
        ordering = ['seat_number']

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        if self.seat_number is None and self.bus is not None:
            self.seat_number = self.bus.first_available_seat_number
        super(BusCheckIn, self).save(*args, **kwargs)

    def move_to(self, bus):
        if bus.edit_is_allow:
            if bus.available_seats >= 1:
                self.bus.remove_occupant()
                self.bus = bus
                self.seat_number = bus.first_available_seat_number
                self.save()
                bus.add_occupant()
            else:
                raise ValidationError('This Bus does not have available seats')
        else:
            raise ValidationError('This Bus can be Edit')

    @property
    def full_name(self):
        if self.name is not None and self.last_name is not None:
            return '{}, {}'.format(self.last_name, self.name)
        return self.name if self.name else self.last_name

    def assign_number(self, seat_number):
        if self.bus is None:
            raise ValidationError('This Check-In does not have bus')
        if not self.bus.is_seat_number_available(seat_number):
            raise ValidationError('This seat number is not available')
        self.seat_number = seat_number
        self.save()


class PayTrip(models.Model):
    trip = models.ForeignKey(Trip)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    staff = models.ForeignKey(User, blank=True, null=True)
    refered_by = models.CharField(max_length=255, blank=True, null=True)
    membership = models.CharField(max_length=255, default='no')

    def __unicode__(self):
        return u'%s' % self.name

    def get_payment_records(self):
        return 'http://isefamily.com/trips/%s/payments/' % self.trip.pk  # Why hard coded url?

    def get_full_name(self):
        return '%s %s' % (self.name, self.last_name)


class PaymentAssignment(models.Model):
    paytrip = models.ForeignKey(PayTrip)
    timestamp = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(User, blank=True, null=True)
    comments = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return u'%s' % self.staff


class Confirmation(models.Model):
    payment = models.OneToOneField(PayTrip)
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)
    has_room = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.code


class Room(models.Model):
    trip = models.ForeignKey(Trip)
    name = models.CharField(max_length=1024)
    capacity = models.IntegerField(default=1)
    available_rooms = models.IntegerField(default=1)
    is_full = models.BooleanField(default=False)
    roomates = models.ManyToManyField(Confirmation)

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_rooms = self.capacity
        super(Room, self).save(*args, **kwargs)

    @property
    def edit_is_allow(self):
        return self.trip.edit_is_allow if self.trip is not None else False

    @property
    def can_change_roomate(self):
        if self.edit_is_allow:
            return True
        return False

    @property
    def has_occupants(self):
        if self.is_full or self.available_rooms < self.capacity:
            return True
        return False

    @property
    def can_remove(self):
        if self.edit_is_allow and not self.has_occupants:
            return True
        return False

    def add_roomate(self, confirmation):
        if self.is_full:
            raise ValidationError('The room is full')
        self.roomates.add(confirmation)
        self.available_rooms -= 1
        self.save()
        confirmation.has_room = True
        confirmation.save()
        self.figure_room_availability()

    def figure_room_availability(self):
        if self.available_rooms <= 0:
            self.is_full = True
        else:
            self.is_full = False
        self.save()

    def move_to(self, confirmation, room):
        if self.edit_is_allow:
            try:
                with transaction.atomic():
                    self.roomates.remove(confirmation)
                    self.available_rooms += 1
                    self.save()
                    self.figure_room_availability()
                    confirmation.has_room = False
                    confirmation.save()
                    self.figure_room_availability()
                    room.add_roomate(confirmation)
            except ValidationError, ve:
                raise ve
        else:
            raise ValidationError('This Room can be Edit')


class CardPayment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    paytrip = models.ForeignKey(PayTrip)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    token = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.paytrip

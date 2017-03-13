from django import forms
from django.forms import ModelForm, Textarea, TextInput, SelectMultiple, FileInput, Select, HiddenInput

from iseteam.trips.models import Trip, HotelCheckIn, BusCheckIn, PayTrip, ImageTrip, Room

from django.utils.translation import ugettext_lazy as _  # Are you using Translation on the entire project?
from django.contrib.auth.models import User

attrs_dict = {'class': 'required form-control', }


class LogInForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={
                                    'invalid': _("This value must contain only letters, numbers and underscores.")
                                })
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                               label=_("Password"))


class SignUpForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))

    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={
                                    'invalid': _("This value must contain only letters, numbers and underscores.")
                                })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,  # Look into this
                                                               maxlength=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)")),

    # Normal Info
    university = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))  # Look into this
    age = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))  # Look into this
    gender = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))  # Look into this
    country = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))  # Look into this

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address.")
            )
        return self.cleaned_data['email']


class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ('slug', 'is_full')
        widgets = {
            'city': Select(attrs={'placeholder': '', 'class': 'form-control'}),
            'name': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'date': TextInput(attrs={'placeholder': '', 'class': 'datepicker form-control'}),
            'price_presale': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'price_sale': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'buses': SelectMultiple(attrs={'placeholder': '', 'class': 'form-control'}),
            'tickets': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'facebook': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'video': TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'cover': FileInput(attrs={'placeholder': '', 'class': 'form-control'}),
            'brief': Textarea(attrs={'placeholder': '', 'class': 'form-control', 'style': 'height:100px'}),
            'description': Textarea(attrs={'placeholder': 'Type here...', 'class': 'wysiwyg demo-form-wysiwyg'}),
        }


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('available_rooms', 'is_full', 'roomates',)
        widgets = {
            'name': TextInput(attrs={'placeholder': '', 'class': 'form-control', 'required': True}),
            'capacity': TextInput(attrs={'placeholder': '', 'class': 'form-control', 'type': 'number', 'min': '1',
                                         'required': True}),
            'trip': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            self.fields['capacity'].widget = HiddenInput()


ROOMS_CAPACITY_CHOICE = (('{}'.format(i), i) for i in range(1, 11))


class MultipleRoomForm(ModelForm):
    qty = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': '', 'class': 'form-control',
                                                                 'type': 'number', 'min': '1', 'required': True}))
    capacity_choice = forms.ChoiceField(choices=ROOMS_CAPACITY_CHOICE, label='Capacity',
                                        widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Room
        exclude = ('name', 'capacity', 'available_rooms', 'is_full', 'roomates',)
        widgets = {
            'trip': HiddenInput(),
        }

    def save(self, force_insert=False, force_update=False):
        ids = []
        data = self.cleaned_data
        print "DATA: {}".format(data)
        capacity = data.get('capacity_choice')
        qty = int(data.get('qty'))
        trip = data.get('trip')
        for index in range(qty):
            name = "Room {} ({})".format(index+1, capacity)
            room = Room.objects.create(trip=trip, capacity=capacity, name=name)
            ids.append(room.id)
        rooms = Room.objects.none() if len(ids) == 0 else Room.objects.filter(id__in=ids)
        return rooms


class HotelCheckInForm(ModelForm):
    class Meta:
        model = HotelCheckIn
        fields = "__all__"


class BusCheckInForm(ModelForm):
    class Meta:
        model = BusCheckIn
        fields = "__all__"


class PayTripForm(ModelForm):
    class Meta:
        model = PayTrip
        exclude = ('trip', 'is_paid', 'is_delivered', 'staff')


class ImageTripForm(ModelForm):
    class Meta:
        model = ImageTrip
        fields = "__all__"

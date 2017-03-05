from django import forms
from django.forms import ModelForm

from iseteam.airport.models import PEOPLE_CHOICES, PickUp


class PickUpForm(ModelForm):
	class Meta:
		model = PickUp
		widgets = {
			'city' : forms.Select(attrs={'class':'form-control'}),
			'name' : forms.TextInput(attrs={'class':'form-control'}),
			'last_name' : forms.TextInput(attrs={'class':'form-control'}),
			'country' : forms.TextInput(attrs={'class':'form-control'}),
			'email' : forms.TextInput(attrs={'class':'form-control'}),
			'flight_number' : forms.TextInput(attrs={'class':'form-control'}),
			'airline' : forms.TextInput(attrs={'class':'form-control'}),
			'terminal' : forms.TextInput(attrs={'class':'form-control'}),
			'people' : forms.Select(attrs={'class':'form-control'}),
			'date' : forms.TextInput(attrs={'class':'form-control datepicker'}),
			'time' : forms.TextInput(attrs={'class':'form-control timepicker'}),
			'comments' : forms.Textarea(attrs = {'class' : 'form-control', 'rows':'3'}),
		}
		exclude = ('attendant',)







